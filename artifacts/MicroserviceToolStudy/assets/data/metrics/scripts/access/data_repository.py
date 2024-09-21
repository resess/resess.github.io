import json
import os
import pandas as pd

class DataRepository:
    def __init__(self, decompositions_path):
        application_src_base = os.path.abspath("./casestudies")
        
        self.data_base = os.path.abspath("./data")
        
        self.base_file_path = os.path.abspath("./data")

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

        # self.config_path = "./config.json"

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
        return f"{self.base_file_path}/relationship_graphs/{application}/class_level/commits.csv"

    def get_contributor_graph_path(self, application):
        return f"{self.base_file_path}/relationship_graphs/{application}/class_level/contributors.csv"

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
        data = []
        for row in rows:
            if row["tool"] == "mem":
                partition_count = row["partition"].split("_")[0] + "_partitions"
                variant = row["partition"][2:].replace("_partitions", "")
                row_data = {
                    "Application": row["application"],
                    "Tool": row["tool"],
                    "Partition Count": partition_count,
                    "Decomposition Type": variant,
                    "Commits": "X",
                    "Contributors": "X",
                    "Class Names": "X",
                    "Static Structural": row["structural_static"],
                    "Granularity": row["granularity"],
                    "SMQ": row["structural_static-fosci"],
                    "CMQ": "X",
                    "CDP": row["CDP"],
                    "TurboMQ_commits": row["commits"],
                    "TurbomMQ_contributors": row["contributors"],
                }
            else:
                row_data ={
                    "Application": row['application'],
                    "Tool": row['tool'],
                    "Partition Count": row['partition'],
                    "Decomposition Type": row['decomposition_type'],
                    "Commits": "X",
                    "Contributors": "X",
                    "Class Names": "X",
                    "Static Structural": row['structural_static'],
                    "Granularity": row['granularity'],
                    "SMQ": row['structural_static-fosci'],
                    "CMQ": "X",
                    "CDP": row['CDP'],
                    "TurboMQ_commits": row['commits'],
                    "TurbomMQ_contributors": row['contributors']
                }  
            data.append(row_data)
        df = pd.DataFrame(data)
        df = df.sort_values(by=['Decomposition Type', 'Tool', 'Application'])
        df.to_csv(self.metrics_output_path, index=False)

    def write_entropy_to_csv(self, rows):
        data = []
        for row in rows:
            if row["tool"] == "mem":
                partition_count = row["long_partition"].split("_")[0]
                variant = row["long_partition"][2:].replace("_partitions", "")
                row_data ={
                    "Application": row['application'],  
                    "Tool": row['tool'],
                    "Partition Count": partition_count,
                    "Variant": variant,
                    "Granularity": row['granularity'],
                    "Database Entropy": row['database_entropy'],
                    "Use Case Entropy": row['use_case_entropy'], 
                    "M2M Use Case Entropy": row['m2m_use_case_entropy'], 
                    "Sarah BCP": row['sarah_bcp']
                }
            else:
                row_data ={
                    "Application": row['application'],  
                    "Tool": row['tool'],
                    "Partition Count": row['partition_count'],
                    "Variant": row['variant'],
                    "Granularity": row['granularity'],
                    "Database Entropy": row['database_entropy'],
                    "Use Case Entropy": row['use_case_entropy'], 
                    "M2M Use Case Entropy": row['m2m_use_case_entropy'], 
                    "Sarah BCP": row['sarah_bcp']
                }
            data.append(row_data)
        df = pd.DataFrame(data)
        df = df.sort_values(by=['Variant', 'Tool', 'Application'])
        df.to_csv(self.entropy_output_path, index=False)

    def write_statistics_to_csv(self, rows):
        data = []
        for row in rows:
            if row["tool"] == "mem":
                partition_count = row["long_partition"].split("_")[0]
                variant = row["long_partition"][2:].replace("_partitions", "")
                row_data = {
                    "Application": row['application'],
                    "Tool": row['tool'],
                    "Partition Count": partition_count,
                    "Variant": variant,
                    "Granularity": row['granularity'],
                    "NED": row['ned'],
                    "Completeness": row['completeness'],
                    "Actual Partition Count": row['actual_partition_count'],
                    "Min": row['min'],
                    "Max": row['max'],
                    "Mean": row['mean'],
                    "Stdev": row['stdev'],
                    "Median": row['median']
                }
            else:
                row_data = {
                    "Application": row['application'],
                    "Tool": row['tool'],
                    "Partition Count": row['partition_count'],
                    "Variant": row['variant'],
                    "Granularity": row['granularity'],
                    "NED": row['ned'],
                    "Completeness": row['completeness'],
                    "Actual Partition Count": row['actual_partition_count'],
                    "Min": row['min'],
                    "Max": row['max'],
                    "Mean": row['mean'],
                    "Stdev": row['stdev'],
                    "Median": row['median']
                }
            data.append(row_data)
        df = pd.DataFrame(data)
        df = df.sort_values(by=['Variant', 'Tool', 'Application'])
        df.to_csv(self.statistics_output_path, index=False)
        
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
