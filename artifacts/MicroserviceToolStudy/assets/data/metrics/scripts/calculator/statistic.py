from access.applications import ApplicationRepository
from access.data_repository import DataRepository
from access.decompositions import DecompositionRepository
from access.manifest import Manifest
from calculator.calculator import Calculator
from models.decomposition_identifier import DecompositionIdentifier
from utils.utils import Utils
import numpy as np
import statistics


class StatisticCalculator():

    def __init__(self, data_repository: DataRepository, manifest: Manifest,
                 decomposition_repository: DecompositionRepository, application_repository: ApplicationRepository,
                 utils: Utils):
        self.data_repository = data_repository
        self.manifest = manifest
        self.decomposition_repository = decomposition_repository
        self.application_repository = application_repository
        self.utils = utils

    def _calculate_ned(self, decomp_id):
        decomposition = self.decomposition_repository.get_decomposition_by_id(decomp_id)
        total_node_count = self.utils.get_decomposition_size(decomposition)

        if len(decomposition.keys()) <= 2:
            print(f"WARNING: Decomposition for tool {decomp_id.get_tool()} on application {decomp_id.get_application()} of variant {decomp_id.get_variant()} with granularity {decomp_id.get_granularity()} has 0 or 1 partitions")
            return 0

        e = 0.68

        expected_partition_size = total_node_count / len(decomposition.keys())
        low = (1 - e) * expected_partition_size
        high = (1 + e) * expected_partition_size

        extreme_nodes = []
        for partition_name in decomposition.keys():
            if partition_name == "UNOBSERVED":
                # We do not consider the unobserved partition in the NED calculation
                continue
            partition = decomposition[partition_name]
            if len(partition) < low or len(partition) > high:
                extreme_nodes += partition

        if total_node_count > 0:
            ned = (1 - (1.0 * len(extreme_nodes)) / total_node_count) * 100
        else:
            ned = 0
        if ned < 0:
            seen = []
            for extreme_node in extreme_nodes:
                if extreme_node not in seen:
                    seen += [extreme_node]
                else:
                    print(f"Duplicate: {extreme_node}")
            print(f"ned: {ned}, partitions: {len(decomposition.keys())}, expected partition size: {expected_partition_size}, extreme nodes: {len(extreme_nodes)}, total nodes: {total_node_count}")

        if total_node_count == 0:
            return 0
        return (1 - (1.0 * len(extreme_nodes)) / total_node_count) * 100

    def _calculate_completeness(self, decomp_id):
        if decomp_id.get_application() == "spring-petclinic" and (decomp_id.get_tool() in ["ground_truth"]):
            x = 1

        decomposition = self.decomposition_repository.get_decomposition_by_id(decomp_id)
        if "UNOBSERVED" in decomposition.keys():
            decomposition.pop("UNOBSERVED")

        ob_partition_assignments = self.utils.get_node_partition_assignments(decomposition)
        decomp_nodes = set(
            map(lambda n: self.utils.shorten_name(n, decomp_id.get_granularity()), ob_partition_assignments.keys()))

        if "method" in decomp_id.get_granularity():
            nodes = self.application_repository.get_methods(decomp_id.get_application())
        else:
            nodes = self.application_repository.get_classes(decomp_id.get_application())

        mono_nodes = set(map(lambda n: self.utils.shorten_name(n, decomp_id.get_granularity()), set(nodes)))

        included_nodes = mono_nodes.intersection(decomp_nodes)
        excluded_nodes = mono_nodes.difference(decomp_nodes)

        percent = len(included_nodes) / (len(excluded_nodes) + len(included_nodes)) * 100
        return f"{len(included_nodes)} ({percent:.1f}%)"

    def _count_partitions(self, decomp_id):
        decomposition = self.decomposition_repository.get_decomposition_by_id(decomp_id)
        if "UNOBSERVED" in decomposition.keys():
            decomposition.pop("UNOBSERVED")
        if "uncounted" in decomposition.keys():
            decomposition.pop("uncounted")
        return self.utils.get_partition_count(decomposition)

    def _get_stats(self, decomp_id):
        decomposition = self.decomposition_repository.get_decomposition_by_id(decomp_id)
        if "UNOBSERVED" in decomposition.keys():
            decomposition.pop("UNOBSERVED")
        if "uncounted" in decomposition.keys():
            decomposition.pop("uncounted")
        partition_sizes = list(map(lambda partition: len(partition), decomposition.values()))

        return {
            "min": min(partition_sizes) if len(partition_sizes) > 0 else 0,
            "max": max(partition_sizes) if len(partition_sizes) > 0 else 0,
            "mean": statistics.mean(partition_sizes) if len(partition_sizes) > 0 else 0,
            "stdev": statistics.stdev(partition_sizes) if len(partition_sizes) > 1 else 0,
            "median": statistics.median(partition_sizes) if len(partition_sizes) > 0 else 0
        }

    def calculate_statistics(self, applications):
        table = []
        for application in applications:
            print(f"Generating for application: {application}")
            for tool in self.manifest.get_available_tools(application):
                print(f"-> Generating for tool: {tool}")
                for partition_count in self.manifest.get_partition_count_options(
                        application, tool
                ):
                    for variant in self.manifest.get_decomposition_variants(tool):
                        for granularity in self.manifest.get_granularities(tool):
                            decomp_id = DecompositionIdentifier(tool=tool,
                                                                application=application,
                                                                partition_count=partition_count,
                                                                variant=variant,
                                                                granularity=granularity)
                            if application == "demo" and tool == "ground_truth":
                                x = 1

                            ned = self._calculate_ned(decomp_id)
                            completeness = self._calculate_completeness(decomp_id)
                            acutal_partition_count = self._count_partitions(decomp_id)

                            row = {
                                "tool": tool,
                                "application": application,
                                "partition_count": partition_count.split("_")[0],
                                "long_partition": partition_count,
                                "variant": variant,
                                "granularity": granularity,
                                "ned": ned,
                                "completeness": completeness,
                                "actual_partition_count": acutal_partition_count
                            }
                            row.update(self._get_stats(decomp_id))
                            table.append(row)

        self.data_repository.write_statistics_to_csv(table)
