from access.application import Application
from access.applications import ApplicationRepository
from access.data_repository import DataRepository
from access.decompositions import DecompositionRepository
from access.manifest import Manifest
from calculator.data_access import DataAccess
from calculator.dependency_graph import DependencyGraph
from models.decomposition_identifier import DecompositionIdentifier
from utils.utils import Utils
import numpy as np
from scipy.stats import entropy


class EntropyCalculator:
    def __init__(
        self,
        application_repository: ApplicationRepository,
        decomposition_repository: DecompositionRepository,
        utils: Utils,
        manifest: Manifest,
        data_repository: DataRepository,
    ):
        self.application_repository = application_repository
        self.decomposition_repository = decomposition_repository
        self.utils = utils
        self.manifest = manifest
        self.data_repository = data_repository

    def calculate(self, applications):
        table = []
        for application in applications:
            print(f"Generating for application: {application}")
            app = Application(application, self.application_repository)
            data_access = DataAccess(app, DependencyGraph(app, self.data_repository))
            table_accesses = data_access.get_table_accesses()
            for tool in self.manifest.get_available_tools(application):
                print(f"-> Generating for tool: {tool}")
                for partition_count in self.manifest.get_partition_count_options(
                    application, tool
                ):
                    for variant in self.manifest.get_decomposition_variants(tool):
                        granularities = ["method_level"]
                        if self.manifest.get_granularity(tool) == "class":
                            granularities.append("class_level")
                        for granularity in granularities:
                            decomposition_id = DecompositionIdentifier(
                                application=application,
                                tool=tool,
                                partition_count=partition_count,
                                granularity=granularity,
                                variant=variant,
                            )
                            database_entropy = self.calculate_database_entropy(
                                application=application,
                                tool=tool,
                                partition_count=partition_count,
                                granularity=granularity,
                                variant=variant,
                                table_accesses=table_accesses,
                            )
                            use_case_entropy = self.calculate_use_case_entropy(
                                decomposition_id
                            )
                            m2m_use_case_entropy = self.calculate_m2m_use_case_entropy(
                                decomposition_id
                            )
                            sarah_bcp = self.calculate_sarah_bcp(decomposition_id)
                            row = {
                                "tool": tool,
                                "application": application,
                                "partition_count": partition_count.split("_")[0],
                                "long_partition": partition_count,
                                "variant": variant,
                                "granularity": granularity,
                                "database_entropy": database_entropy,
                                "use_case_entropy": use_case_entropy,
                                "m2m_use_case_entropy": m2m_use_case_entropy,
                                "sarah_bcp": sarah_bcp,
                            }
                            table.append(row)

        self.data_repository.write_entropy_to_csv(table)

    def calculate_database_entropy(
        self, application, tool, partition_count, variant, granularity, table_accesses
    ):
        return self._calculate_entropy(
            labels=table_accesses,
            application=application,
            tool=tool,
            partition_count=partition_count,
            variant=variant,
            granularity=granularity,
            is_method_name=True,
        )

    def calculate_use_case_entropy(self, decomposition_id):
        use_cases = self.application_repository.get_use_cases(
            decomposition_id.get_application()
        )
        return self._calculate_entropy(
            labels=use_cases,
            application=decomposition_id.get_application(),
            tool=decomposition_id.get_tool(),
            partition_count=decomposition_id.get_partition_count(),
            variant=decomposition_id.get_variant(),
            granularity=decomposition_id.get_granularity(),
        )

    def calculate_m2m_use_case_entropy(self, decomposition_id):
        use_cases = self.application_repository.get_use_cases(
            decomposition_id.get_application()
        )
        return self._calculate_m2m_bcp(
            labels=use_cases,
            application=decomposition_id.get_application(),
            tool=decomposition_id.get_tool(),
            partition_count=decomposition_id.get_partition_count(),
            variant=decomposition_id.get_variant(),
        )

    def calculate_sarah_bcp(self, decomposition_id):
        use_cases = self.application_repository.get_use_cases(
            decomposition_id.get_application()
        )
        return self._calculate_bcp_prime_version(
            labels=use_cases,
            application=decomposition_id.get_application(),
            tool=decomposition_id.get_tool(),
            partition_count=decomposition_id.get_partition_count(),
            variant=decomposition_id.get_variant(),
        )

    def _calculate_entropy(
        self,
        labels,
        application,
        tool,
        partition_count,
        variant,
        granularity,
        is_method_name=True,
    ):
        decomposition = self.decomposition_repository.get_decomposition(
            tool=tool,
            application=application,
            partition_count=partition_count,
            granularity=granularity,
            variant=variant,
        )
        partition_assignments = self.utils.get_node_partition_assignments(decomposition)
        entropies = []
        duplicates = [
            node
            for node in partition_assignments
            if len(partition_assignments[node]) > 1
        ]

        for label in labels.keys():
            seen_nodes = []  # Don't count the same node more than once
            partitions = []

            # Handle non-duplicate nodes
            for node in list(set(labels[label])):
                node_name = self.utils.shorten_name(
                    node, granularity, is_method_name=is_method_name
                )
                if node_name not in duplicates:
                    if (
                        node_name in partition_assignments.keys()
                        and node_name not in seen_nodes
                    ):
                        for partition in partition_assignments[node_name]:
                            if partition != "UNOBSERVED":
                                partitions.append(partition)
                                seen_nodes.append(node_name)

            # Handle duplicate nodes
            for node in list(set(labels[label])):
                node_name = self.utils.shorten_name(
                    node, granularity, is_method_name=is_method_name
                )
                if node_name in duplicates:
                    if (
                        node_name in partition_assignments.keys()
                        and node_name not in seen_nodes
                    ):
                        # Make an optimisitic assumption about which duplicate is accessing the table
                        max_match = -1
                        closest_match = None
                        for partition in partition_assignments[node_name]:
                            if partition != "UNOBSERVED":
                                partition_match = len(
                                    list(filter(lambda p: p == partition, partitions))
                                )
                                if partition_match > max_match:
                                    max_match = partition_match
                                    closest_match = partition
                        partitions += [closest_match]
                        seen_nodes.append(node_name)

            partition_counts = np.unique(partitions, return_counts=True)[1]
            ent = entropy(partition_counts)
            if ent > 1:
                ent = 1
            entropies.append(ent)

        return (1 - np.sum(entropies) / len(entropies)) * 100

    # Calculate entropy of business use cases per partition as defined by Mono2Micro
    def _calculate_m2m_bcp(
        self,
        labels,
        application,
        tool,
        partition_count,
        variant,
        is_method_name=True,
        ignore_dups=True,
    ):
        granularity = "method_level"
        decomposition = self.decomposition_repository.get_decomposition(
            tool=tool,
            application=application,
            partition_count=partition_count,
            granularity=granularity,
            variant=variant,
        )

        if tool == "ground_truth" and application == "spring-petclinic":
            x = 1

        node_label_map = {}
        for label in labels.keys():
            for method in list(set(labels[label])):
                node_name = self.utils.shorten_name(
                    method, granularity, is_method_name=is_method_name
                )
                if node_name not in node_label_map.keys():
                    node_label_map[node_name] = []
                node_label_map[node_name].append(label)

        node_assignments = Utils().get_node_partition_assignments(decomposition)
        duplicates = [
            node for node in node_assignments if len(node_assignments[node]) > 1
        ]

        entropies = []

        for partition_name in decomposition.keys():
            use_cases = []

            for node in decomposition[partition_name]:
                if node in node_label_map.keys() and node not in duplicates:
                    for label in node_label_map[node]:
                        use_cases.append(label)

            for node in decomposition[partition_name]:
                if node in node_label_map.keys() and node in duplicates:
                    max_match = 0
                    closest_match = node_label_map[node][0]
                    for label in node_label_map[node]:
                        matching_count = len(
                            list(filter(lambda c: c == label, use_cases))
                        )
                        if matching_count > max_match:
                            max_match = matching_count
                            closest_match = label
                    use_cases.append(closest_match)

            if len(use_cases) == 0:
                # Ignore partitions that don't support any business use case
                continue

            if ignore_dups:
                use_cases = list(set(use_cases))
            use_case_counts = np.unique(use_cases, return_counts=True)[1]

            ent = entropy(use_case_counts)
            if ent > 1:
                ent = 1
            entropies.append(ent)

        return (1 - np.sum(entropies) / len(entropies)) * 100

    # Similar to m2m BCP, except we count frequency of use cases per fucntion/method rather than saying it's just 1
    def _calculate_bcp_prime_version(
        self, labels, application, tool, partition_count, variant, is_method_name=True
    ):
        return self._calculate_m2m_bcp(
            labels,
            application,
            tool,
            partition_count,
            variant,
            is_method_name,
            ignore_dups=False,
        )
