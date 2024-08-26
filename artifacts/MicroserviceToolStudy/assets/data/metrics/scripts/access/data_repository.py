import json
import os

class DataRepository:
    def __init__(self, decompositions_path):
        application_src_base = os.path.abspath("../../../code/scripts/metrics/casestudies")
        
        self.data_base = os.path.abspath("../../../code/scripts/metrics/data")
        
        self.base_file_path = os.path.abspath("../../../code/scripts/metrics/data")

        self.application_src_paths = {
            "demo": f"{application_src_base}/demo/src/main/java",
            "jpetstore": f"{application_src_base}/jpetstore-6/src/main/java",
            "partsunlimited": f"{application_src_base}/PartsUnlimitedMRP/src/Backend/OrderService/src/main/java",
            "spring-petclinic": f"{application_src_base}/spring-petclinic/src/main/java",
        }

        self.decompositions_path = decompositions_path
        self.metrics_output_path = f"{self.data_base}/metrics/metrics.csv"
        self.entropy_output_path = f"{self.data_base}/metrics/entropy.csv"
        self.statistics_output_path = f"{self.data_base}/metrics/statistics.csv"

        self.config_path = "./config.json"

    def get_method_list(self, application):
        with open(
            f"{self.base_file_path}/relationships/{application}/method-level/methods.txt",
            "r",
        ) as file:
            return list(map(lambda line: line.strip(), file.readlines()))

    def get_application_src_path(self, application):
        return self.application_src_paths[application]

    def get_git_log_path(self, application):
        return f"{self.base_file_path}/relationship_graphs/{application}/method_level/history.log"

    def get_commit_graph_path(self, application):
        return f"{self.base_file_path}/relationship_graphs/{application}/method_level/commit_graph.csv"

    def get_contributor_graph_path(self, application):
        return f"{self.base_file_path}/relationship_graphs/{application}/method_level/contributor_graph.csv"

    def get_decompositions_manifest(self):
        manifest_file = open(f"{self.decompositions_path}/manifest.json", "r")
        manifest = json.load(manifest_file)
        manifest_file.close()
        return manifest

    def get_visualization_path(
        self, application, tool, partition, decomposition_type, granularity
    ):
        folder_path = f"{self.decompositions_path}/{application}/{tool}/{partition}"
        if decomposition_type != "default":
            folder_path += f"/{decomposition_type}"
        return f"{folder_path}/{granularity.split('_')[0]}_visualization.json"

    def write_metrics_to_csv(self, rows):
        csv_data = (
            "Application,Tool,Partition Count,Decomposition Type,Commits,Contributors,Class Names,"
            "Static Structural,Granularity,SMQ,CMQ,CDP,TurboMQ_commits,TurbomMQ_contributors\n"
        )
        for row in rows:
            if row["tool"] == "mem":
                partition_count = row["partition"].split("_")[0] + "_partitions"
                variant = row["partition"][2:].replace("_partitions", "")
                csv_data += (
                    f"{row['application']},{row['tool']},{partition_count},{variant},"
                    f"X,X,X,"
                    f"{row['structural_static']},{row['granularity']},{row['structural_static-fosci']},X,{row['CDP']},{row['commits']},{row['contributors']}\n"
                )
            else:
                csv_data += (
                    f"{row['application']},{row['tool']},{row['partition']},{row['decomposition_type']},"
                    f"X,X,X,"
                    f"{row['structural_static']},{row['granularity']},{row['structural_static-fosci']},X,{row['CDP']},{row['commits']},{row['contributors']}\n"
                )

        out_file = open(self.metrics_output_path, "w")
        out_file.write(csv_data)
        out_file.close()

    def write_entropy_to_csv(self, rows):
        csv_data = "Application,Tool,Partition Count,Variant,Granularity,Database Entropy,Use Case Entropy, M2M Use Case Entropy, Sarah BCP\n"
        for row in rows:
            if row["tool"] == "mem":
                partition_count = row["long_partition"].split("_")[0]
                variant = row["long_partition"][2:].replace("_partitions", "")
                csv_data += (
                    f"{row['application']},{row['tool']},{partition_count},{variant},"
                    f"{row['granularity']},"
                    f"{row['database_entropy']},{row['use_case_entropy']},{row['m2m_use_case_entropy']},{row['sarah_bcp']}\n"
                )
            else:
                csv_data += (
                    f"{row['application']},{row['tool']},{row['partition_count']},{row['variant']},"
                    f"{row['granularity']},"
                    f"{row['database_entropy']},{row['use_case_entropy']},{row['m2m_use_case_entropy']},{row['sarah_bcp']}\n"
                )

        out_file = open(self.entropy_output_path, "w")
        out_file.write(csv_data)
        out_file.close()

    def write_statistics_to_csv(self, rows):
        csv_data = "Application,Tool,Partition Count,Variant,Granularity,NED,Completeness,Actual Partition Count,Min,Max,Mean,Stdev,Median\n"
        for row in rows:
            if row["tool"] == "mem":
                partition_count = row["long_partition"].split("_")[0]
                variant = row["long_partition"][2:].replace("_partitions", "")
                csv_data += (
                    f"{row['application']},{row['tool']},{partition_count},{variant},"
                    f"{row['granularity']},{row['ned']},"
                    f"{row['completeness']},{row['actual_partition_count']},"
                    f"{row['min']},{row['max']},{row['mean']},{row['stdev']},{row['median']}\n"
                )
            else:
                csv_data += (
                    f"{row['application']},{row['tool']},{row['partition_count']},{row['variant']},"
                    f"{row['granularity']},{row['ned']},"
                    f"{row['completeness']},{row['actual_partition_count']},"
                    f"{row['min']},{row['max']},{row['mean']},{row['stdev']},{row['median']}\n"
                )

        out_file = open(self.statistics_output_path, "w")
        out_file.write(csv_data)
        out_file.close()

    def get_dependency_path(self, application):
        return f"{self.data_base}/applications/{application}/dependencies.xml"

    def get_method_static_structural_graph_path(self, application):
        return f"{self.data_base}/relationship_graphs/{application}/method_level/structural_static.csv"

    def get_class_static_structural_graph_path(self, application):
        return f"{self.data_base}/relationship_graphs/{application}/class_level/structural_static.csv"

    def get_relationship_path(self, application, relationship, granularity):
        return f"{self.data_base}/relationship_graphs/{application}/{granularity}/{relationship}.csv"

    def get_node_list_path(self, application, granularity):
        return f"{self.data_base}/relationship_graphs/{application}/{granularity}/nodes.csv"
