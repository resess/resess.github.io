import json
import math

from access.data_repository import DataRepository
from access.manifest import Manifest
from utils.utils import Utils
import numpy as np
import os


class Evaluator:
    def __init__(self, data_repository: DataRepository, manifest: Manifest):
        self.table = []
        self.data_repository = data_repository
        self.manifest = manifest

    def calculate_cycles(self, edges, decomposition, partition_assignments):
        total_pairs = 0
        interdependent_pairs = 0

        partition_names = list(decomposition.keys())
        for partition_name in partition_names:
            for other_partition_name in partition_names:
                if partition_name == other_partition_name:
                    continue

                total_pairs += 1

                has_forward_dep = False
                has_backward_dep = False

                for edge in edges:
                    source_partition = partition_assignments[edge["source"]][0]
                    target_partition = partition_assignments[edge["target"]][0]

                    assert (
                        len(partition_assignments[edge["source"]]) == 1
                        and len(partition_assignments[edge["target"]]) == 1
                    )

                    if (
                        source_partition == partition_name
                        and target_partition == other_partition_name
                    ):
                        has_forward_dep = True
                    if (
                        target_partition == partition_name
                        and source_partition == other_partition_name
                    ):
                        has_backward_dep = True

                if has_forward_dep and has_backward_dep:
                    interdependent_pairs += 1

        if total_pairs == 0:
            return 0

        return (interdependent_pairs / total_pairs) * 100

    def calculate_commit_mq(
        self, decomposition, partition_assignments, app_name, granularity
    ):
        internal_changes = {}
        external_changes = {}

        for partition_name in decomposition.keys():
            internal_changes[partition_name] = 0
            external_changes[partition_name] = 0

        filename = os.path.abspath(f"./data/relationship_graphs/{app_name}/class_level/commits.csv")
        with open(
            filename
        ) as edge_file:

            for line in edge_file.readlines():
                row = line.strip().split(",")
                source = Utils().shorten_name(row[1], granularity, True)
                target = Utils().shorten_name(row[2], granularity, True)

                if (
                    source not in partition_assignments.keys()
                    or target not in partition_assignments.keys()
                ):
                    continue

                if partition_assignments[source] == partition_assignments[target]:
                    internal_changes[partition_assignments[source][0]] += float(row[3])
                else:
                    external_changes[partition_assignments[source][0]] += float(row[3])
                    external_changes[partition_assignments[target][0]] += float(row[3])

        cf = 0

        for partition_name in decomposition.keys():
            icf = internal_changes[partition_name]
            ecf = external_changes[partition_name]

            if icf > 0:
                cf += (2 * icf) / ((2 * icf) + ecf)

        if len(decomposition) == 0:
            print(f"WARNING: Decomposition is empty for file {filename} [calculate_commit_mq]")
            return 0
        return (cf / len(decomposition)) * 100

    def calculte_contrib_mq(
        self, decomposition, partition_assignments, app_name, granularity
    ):
        internal_changes = {}
        external_changes = {}

        for partition_name in decomposition.keys():
            internal_changes[partition_name] = 0
            external_changes[partition_name] = 0

        filename = os.path.abspath(f"./data/relationship_graphs/{app_name}/class_level/contributors.csv")
        with open(
            filename
        ) as edge_file:
            for line in edge_file.readlines():
                row = line.strip().split(",")
                source = Utils().shorten_name(row[1], granularity, True)
                target = Utils().shorten_name(row[2], granularity, True)

                if (
                    source not in partition_assignments.keys()
                    or target not in partition_assignments.keys()
                ):
                    continue

                if partition_assignments[source] == partition_assignments[target]:
                    internal_changes[partition_assignments[source][0]] += float(row[3])
                else:
                    external_changes[partition_assignments[source][0]] += float(row[3])
                    external_changes[partition_assignments[target][0]] += float(row[3])

        cf = 0

        for partition_name in decomposition.keys():
            icf = internal_changes[partition_name]
            ecf = external_changes[partition_name]

            if icf > 0:
                cf += (2 * icf) / ((2 * icf) + ecf)

        if len(decomposition) == 0:
            print(f"WARNING: Decomposition is empty for file {filename}[calculte_contrib_mq]")
            return 0
        return (cf / len(decomposition)) * 100

    def calculate_normalized_turbomq(
        self, edges, decomposition, partition_assignments, is_m2m=False
    ):
        cf = 0
        for partition_name in decomposition.keys():
            partition = decomposition[partition_name]
            internal_edges = 0.0
            external_edges = 0.0
            for edge in edges:
                source = edge["source"]
                target = edge["target"]
                if (
                    source in partition_assignments.keys()
                    and target in partition_assignments.keys()
                ):
                    # if is_m2m and (source in ["AbstractActionBean", "OrderActionBean", "AccountActionBean", "CartActionBean", "Cart"] or target in ["AbstractActionBean", "OrderActionBean", "AccountActionBean", "CartActionBean", "Cart"]):
                    #     internal_edges += float(edge["weight"])
                    if source in partition and target in partition:
                        internal_edges += float(edge["weight"])
                    elif source in partition or target in partition:
                        external_edges += float(edge["weight"])
            if internal_edges > 0:
                cf += (2 * internal_edges) / ((2 * internal_edges) + external_edges)

        if len(decomposition) == 0:
            print(f"WARNING: Decomposition is empty [calculate_normalized_turbomq]")
            return 0
        return (cf / len(decomposition)) * 100

    def calculate_fosci_mq(self, edges, decomposition, partition_assignments):
        return -1
        scohs = []
        scops = []
        empty_partitions = 0
        for partition_name in decomposition.keys():
            # Calculate scoh for each partition
            partition = decomposition[partition_name]
            if len(partition) == 0:
                empty_partitions += 1
                continue
            internal_edges = 0
            int_edges = {}
            for edge in edges:
                source = edge["source"]
                target = edge["target"]
                if (
                    source in partition_assignments.keys()
                    and target in partition_assignments.keys()
                ):
                    if (
                        source in partition
                        and target in partition
                        and (
                            source not in int_edges.keys()
                            or target not in int_edges[source]
                        )
                    ):
                        internal_edges += 1  # float(edge["weight"])
                        if source not in int_edges.keys():
                            int_edges[source] = []
                        int_edges[source].append(target)

            scohs.append(internal_edges / math.pow(len(partition), 2))

            # Calculate scop for each partition pair
            for partition_name_2 in decomposition.keys():
                if partition_name_2 == partition_name:
                    continue
                partition_2 = decomposition[partition_name_2]
                if len(partition_2) == 0:
                    empty_partitions += 1
                    continue
                external_edges = 0
                for edge in edges:
                    source = edge["source"]
                    target = edge["target"]
                    if (
                        source in partition_assignments.keys()
                        and target in partition_assignments.keys()
                    ):
                        if (source in partition and target in partition_2) or (
                            source in partition_2 and target in partition
                        ):
                            external_edges += 1  # float(edge["weight"])

                scops.append(external_edges / (2 * len(partition) * len(partition_2)))

        n = len(decomposition) - empty_partitions
        if n < 2:
            return 0
        try:
            return np.average(scohs) - np.average(scops)
        except:
            x = 1

    def calculate_turbomq(
        self,
        visualization_path,
        tool,
        application,
        partition_name,
        decomposition_type,
        granularity,
        relationships,
    ):
        visualization_file = open(visualization_path, "r")
        visualization = json.load(visualization_file)
        visualization_file.close()

        row = {
            "tool": tool,
            "application": application,
            "partition": partition_name,
            "decomposition_type": decomposition_type,
            "granularity": granularity,
        }

        for relationship in relationships:
            if relationship == "structural_static":
                rel_name = "1_structural_static"
            else:
                rel_name = "2_semantic_names"
            edges = visualization[rel_name]["links"]
            decomposition = visualization[rel_name]["decomposition"]
            if "UNOBSERVED" in decomposition.keys():
                decomposition.pop("UNOBSERVED")

            for partition in decomposition.keys():
                decomposition[partition] = list(
                    map(lambda n: n["id"], decomposition[partition])
                )

            partition_assignments = Utils().get_node_partition_assignments(
                decomposition
            )

            cycles = self.calculate_cycles(edges, decomposition, partition_assignments)
            turbomq = self.calculate_normalized_turbomq(
                edges, decomposition, partition_assignments, tool == "mono2micro"
            )
            fosci_mq = self.calculate_fosci_mq(
                edges, decomposition, partition_assignments
            )
            rei = self.calculate_commit_mq(
                decomposition, partition_assignments, application, granularity
            )
            contrib_mq = self.calculte_contrib_mq(
                decomposition, partition_assignments, application, granularity
            )

            row[relationship] = turbomq
            row[relationship + "-fosci"] = fosci_mq
            row["CDP"] = cycles
            row["commits"] = rei
            row["contributors"] = contrib_mq

        self.table.append(row)

    def calculate_metrics(self, applications, relationships):
        for application in applications:
            print(f"Evaluating application: {application}")
            for tool in self.manifest.get_available_tools(application):
                print(f"-> Evaluating tool: {tool}")
                for partition in self.manifest.get_partition_count_options(
                    application, tool
                ):
                    for decomposition_type in self.manifest.get_decomposition_variants(
                        tool
                    ):
                        granularities = ["method_level"]
                        if self.manifest.get_granularity(tool) == "class":
                            granularities.append("class_level")
                        for granularity in granularities:
                            if (
                                tool == "ground_truth"
                                and application == "spring-petclinic"
                            ):
                                x = 1
                            self.calculate_turbomq(
                                self.data_repository.get_visualization_path(
                                    application,
                                    tool,
                                    partition,
                                    decomposition_type,
                                    granularity,
                                ),
                                tool,
                                application,
                                partition,
                                decomposition_type,
                                granularity,
                                relationships,
                            )

        self.data_repository.write_metrics_to_csv(self.table)
