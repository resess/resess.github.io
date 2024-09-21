import json
import csv
import os
import subprocess
import pandas as pd 

from access.decompositions import DecompositionRepository
from access.manifest import Manifest
from calculator.c2c import C2CCalculator


class MojofmCalculator:
    def __init__(self, applications_path, decomposition_repository: DecompositionRepository):
        self.applications_path = applications_path
        self.DECOMPOSITIONS_PATH = "./data/decompositions"
        self.RELATIONSHIPS_PATH = "./data/relationships"
        self.OUTPUT_PATH = "./data/metrics/mojofm.csv"
        self.table = []
        self.decomposition_repository = decomposition_repository

    def write_table(self):
        data = []
        for row in self.table:
            row_data = {
                "Application": row['application'],
                "Tool": row['tool'],
                "Partition Count": row['partition'],
                "Decomposition Type": row['decomposition_type'],
                "Granularity": row['granularity'],
                "Mojo-D": "X",
                "Mojo": row['mojo'],
                "C2C 50": row['c2c_50'],
                "C2C 33": row['c2c_33'],
                "C2C 10": row['c2c_10']
            }
            data.append(row_data)
        df = pd.DataFrame(data)
        df = df.sort_values(by=['Decomposition Type', 'Tool', 'Application'])
        df.to_csv(self.OUTPUT_PATH, index=False)

    def compute_mojo(self, json_graph, ground_truth_rsf_file, row):
        if ".json" in json_graph:
            self.convert_json_to_rsf(json_graph)
        json_names, rsf_graph = self.get_class_names_from_rsf(json_graph.replace(".json", ".rsf"))
        ground_truth_names, g_rsf_graph = self.get_class_names_from_rsf(ground_truth_rsf_file)
        self.add_unobserved_cluster(
            ground_truth_names,
            json_names,
            rsf_graph,
            json_graph.replace(".json", ".rsf"),
        )
        cmd = [
            "java",
            "-cp",
            os.path.abspath("./resources/MoJo-1.0-SNAPSHOT.jar"),
            "mojo.MoJo",
            os.path.abspath(json_graph.replace(".json", ".rsf")),
            os.path.abspath(ground_truth_rsf_file),
            "-fm",
            "0",
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        print("MoJo: " + result.stdout.decode("utf-8").strip())
        row["mojo"] = result.stdout.decode("utf-8").strip()
        self.table.append(row)


        # cmd = [
        #     "python3",
        #     "c2c_cvg.py",
        #     "--tgtfile",
        #     ground_truth_rsf_file,
        #     "--sourcefile",
        #     json_graph.replace(".json", ".rsf"),
        # ]
        # result = subprocess.run(cmd, stdout=subprocess.PIPE)
        # print("c2c: " + result.stdout.decode("utf-8"))

    def calculate_number_of_differences(self, json_graph_file_rsf, ground_truth_rsf_file):
        json_graph = []
        with open(json_graph_file_rsf, "r") as f:
            csv_reader = csv.reader(f, delimiter=" ")
            for place in csv_reader:
                json_graph.append(place[1])

        ground_truth_graph = []
        with open(ground_truth_rsf_file, "r") as f:
            csv_reader = csv.reader(f, delimiter=" ")
            for place in csv_reader:
                ground_truth_graph.append(place[1])

        return str(abs(len(ground_truth_graph) - len(json_graph)))

    def convert_json_to_rsf(self, json_graph_name):
        json_file = open(json_graph_name, "r")
        graph = json.load(json_file)
        if "tool" in graph.keys():
            graph = graph["tool"]["decomposition"]
        elif "MEM" in graph.keys():
            graph = graph["MEM"]["decomposition"]
        entityRelations = []
        for cluster_name in graph.keys():
            for node in graph[cluster_name]:
                node_name = node["id"]
                entityRelations.append("contain " + cluster_name + " " + node_name)

        rsfFilename = json_graph_name.replace(".json", "") + ".rsf"
        # write the cluster relationships into the rsf file
        with open(rsfFilename, "w", newline='\n') as rsfFile:
            rsfFile.write(("\n").join(entityRelations))

    def get_class_names_from_rsf(self, rsf_file):
        names = []
        rsf_graph = []

        with open(rsf_file, "r") as f:
            csv_reader = csv.reader(f, delimiter=" ")
            for name in csv_reader:
                names.append(name[2])
                rsf_graph.append(name)

        return names, rsf_graph

    def add_unobserved_cluster(self, class_names, rsf_class_names, rsf_graph, file_name):
        unobserved_classes = []
        matches = []

        g = {}
        for name in rsf_graph:
            g[name[2]] = name[1]

        class_names = list(dict.fromkeys(class_names).keys())

        graph = []
        for name in class_names:
            if name in g:
                graph.append(["contain", g[name], name])
            else:
                graph.append(["contain", "unobserved", name])

        clusters = []
        for cluster in graph:
            clusters.append(cluster[1])

        print("Number of Clusters: " + str(len(list(set(clusters)))))

        graph.sort()
        with open(file_name, "w", newline='') as f:
            csv_writer = csv.writer(f, delimiter=" ")
            for n in graph:
                csv_writer.writerow(n)

    def calculate(self, applications, manifest: Manifest):
        manifest_file = open(os.path.abspath(f"{self.DECOMPOSITIONS_PATH}/manifest.json"), "r")
        manifest2 = json.load(manifest_file)
        manifest_file.close()

        for application in applications:
            print(f"Calculating MoJoFM for application: {application}")
            for tool in manifest.get_available_tools(application):
                print(f"-> Calculating MoJoFM for tool: {tool}")
                for partition in manifest.get_partition_count_options(application, tool):
                    # Check if the partition is ready for analysis
                    print(f"---> Generating for partition: {partition}")
                    for decomposition_type in manifest.get_decomposition_variants(tool):
                        granularity = manifest.get_granularity(tool)

                        if granularity == "class":
                            folder_path = f"{self.DECOMPOSITIONS_PATH}/{application}/{tool}/{partition}"
                            if decomposition_type != "default":
                                folder_path += f"/{decomposition_type}"
                                folder_path = os.path.abspath(folder_path)
                            decomposition_path = f"{folder_path}/class_decomposition.json"
                            decomposition_path = os.path.abspath(decomposition_path)

                            ground_truth_rsf_file = os.path.abspath(f"{self.applications_path}/{application}/ground_truth/ground_truth.rsf")
                            c2c_50 = C2CCalculator(self.decomposition_repository).calculate(tool,
                                                                                            application,
                                                                                            "class_level",
                                                                                            decomposition_type,
                                                                                            partition,
                                                                                            0.5)
                            c2c_33 = C2CCalculator(self.decomposition_repository).calculate(tool,
                                                                                            application,
                                                                                            "class_level",
                                                                                            decomposition_type,
                                                                                            partition,
                                                                                            0.33)
                            c2c_10 = C2CCalculator(self.decomposition_repository).calculate(tool,
                                                                                            application,
                                                                                            "class_level",
                                                                                            decomposition_type,
                                                                                            partition,
                                                                                            0.1)
                            row = {
                                "tool": tool,
                                "application": application,
                                "partition": partition,
                                "decomposition_type": decomposition_type,
                                "granularity": "class",
                                "c2c_50": c2c_50,
                                "c2c_33": c2c_33,
                                "c2c_10": c2c_10
                            }

                            if tool == "mem":
                                partition_count = partition.split("_")[0] + "_partitions"
                                variant = partition[2:].replace("_partitions", "")
                                row["partition"] = partition_count
                                row["decomposition_type"] = variant

                            if application == "jpetstore" and tool in ["mono2micro", "hydec"]:
                                x = 1

                            self.compute_mojo(
                                decomposition_path, ground_truth_rsf_file, row
                            )


                        folder_path = (
                            f"{self.DECOMPOSITIONS_PATH}/{application}/{tool}/{partition}"
                        )
                        if decomposition_type != "default":
                            folder_path += f"/{decomposition_type}"

                        decomposition_path = (
                            f"{folder_path}/method_decomposition.json"
                        )

                        ground_truth_rsf_file = f"{self.applications_path}/{application}/ground_truth/method_ground_truth.rsf"

                        c2c_50 = C2CCalculator(self.decomposition_repository).calculate(tool,
                                                                                        application,
                                                                                        "method_level",
                                                                                        decomposition_type,
                                                                                        partition,
                                                                                        0.5)
                        c2c_33 = C2CCalculator(self.decomposition_repository).calculate(tool,
                                                                                        application,
                                                                                        "method_level",
                                                                                        decomposition_type,
                                                                                        partition,
                                                                                        0.33)
                        c2c_10 = C2CCalculator(self.decomposition_repository).calculate(tool,
                                                                                        application,
                                                                                        "method_level",
                                                                                        decomposition_type,
                                                                                        partition,
                                                                                        0.1)


                        row = {
                            "tool": tool,
                            "application": application,
                            "partition": partition,
                            "decomposition_type": decomposition_type,
                            "granularity": "method",
                            "c2c_50": c2c_50,
                            "c2c_33": c2c_33,
                            "c2c_10": c2c_10
                        }

                        if tool == "mem":
                            partition_count = partition.split("_")[0] + "_partitions"
                            variant = partition[2:].replace("_partitions", "")
                            row["partition"] = partition_count
                            row["decomposition_type"] = variant

                        self.compute_mojo(
                            decomposition_path, ground_truth_rsf_file, row
                        )

        self.write_table()
