import math

from access.decompositions import DecompositionRepository


class C2CCalculator:
    def __init__(self, decomposition_repository: DecompositionRepository):
        self.decomposition_repository = decomposition_repository

    def calculate(self, tool, application_name, granularity, variant, partition_count, threshold):
        ground_truth_decomposition = self.decomposition_repository.get_decomposition("ground_truth",
                                                                                     application_name,
                                                                                     "n_partitions",
                                                                                     granularity,
                                                                                     filtered=True)
        tool_decomposition = self.decomposition_repository.get_decomposition(tool,
                                                                             application_name,
                                                                             partition_count,
                                                                             granularity,
                                                                             variant,
                                                                             filtered=True)

        similar_partitions = 0

        if len(ground_truth_decomposition["UNOBSERVED"]) == 0:
            ground_truth_decomposition.pop("UNOBSERVED")

        if len(tool_decomposition["UNOBSERVED"]) == 0:
            tool_decomposition.pop("UNOBSERVED")

        for tool_partition_name in tool_decomposition.keys():
            tool_partition = tool_decomposition[tool_partition_name]
            for ground_truth_partition_name in ground_truth_decomposition.keys():
                ground_truth_partition = ground_truth_decomposition[ground_truth_partition_name]

                if self.calculate_similarity(tool_partition, ground_truth_partition) > threshold:
                    similar_partitions += 1
                    break

        return similar_partitions * 1.0 / len(tool_decomposition.keys()) * 100

    def calculate_similarity(self, cluster_a, cluster_b):
        # if max(len(cluster_a), len(cluster_b)) == 0:
        #     return 0
        return len(set(cluster_a).intersection(set(cluster_b))) * 1.0 / max(len(cluster_a), len(cluster_b))
