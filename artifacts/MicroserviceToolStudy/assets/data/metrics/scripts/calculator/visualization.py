import os
import csv
import json
import shutil

import numpy as np

from access.application import Application
from access.applications import ApplicationRepository
from access.data_repository import DataRepository
from access.decompositions import DecompositionRepository
from access.manifest import Manifest
from calculator.data_access import DataAccess
from calculator.dependency_graph import DependencyGraph
from models.decomposition_identifier import DecompositionIdentifier
from utils.utils import Utils
from functools import reduce
from collections import Counter


class VisualizationGenerator:
    def __init__(
        self,
        data_repository: DataRepository,
        manifest: Manifest,
        decomposition_repository: DecompositionRepository,
        application_repository: ApplicationRepository,
        utils: Utils,
    ):
        self.data_repository = data_repository
        self.manifest = manifest
        self.decomposition_repository = decomposition_repository
        self.application_repository = application_repository
        self.utils = utils

    def get_relationship_json(
        self, decomposition, relationship_graph_path, granularity, application
    ):
        links = self.get_relationship_links(
            relationship_graph_path, granularity, application, decomposition
        )

        # Deal with nodes being duplicated across partitions
        node_assignments = Utils().get_node_partition_assignments(
            Utils().remove_ids(decomposition)
        )
        duplicates = [
            node for node in node_assignments if len(node_assignments[node]) > 1
        ]

        for partition_name, partition in decomposition.items():
            # Rename duplicate nodes
            for node in partition:
                if node["id"] in duplicates:
                    node["id"] = f"[duplicate ({partition_name})] {node['id']}"

        # Modify all edges that have duplicate nodes
        new_links = []
        for link in links:
            source = link["source"]
            target = link["target"]

            if source not in duplicates and target not in duplicates:
                new_links.append(link)

            elif source in duplicates and target in duplicates:
                for partition in node_assignments[source]:
                    if partition in node_assignments[target]:
                        new_links.append(
                            {
                                "source": f"[duplicate ({partition})] {source}",
                                "target": f"[duplicate ({partition})] {target}",
                                "weight": link["weight"],
                            }
                        )

            elif target in duplicates:
                source_partition = node_assignments[source][0]
                if source_partition in node_assignments[target]:
                    link["target"] = f"[duplicate ({source_partition})] {target}"
                    new_links.append(link)

            elif source in duplicates:
                target_partition = node_assignments[target][0]
                if target_partition in node_assignments[source]:
                    link["source"] = f"[duplicate ({target_partition})] {source}"
                    new_links.append(link)

        return {"links": new_links, "decomposition": decomposition}

    def get_relationship_links(
        self, dependency_graph_file, granularity, application, decomposition
    ):
        no_id_decomp = {}
        for partition in decomposition.keys():
            no_id_decomp[partition] = list(
                map(lambda n: n["id"], decomposition[partition])
            )
        observed_nodes = Utils().get_node_partition_assignments(no_id_decomp).keys()

        dep_graph = []
        first_row = ""
        with open(dependency_graph_file, "r") as f:
            csv_reader = csv.reader(f)
            for dep in csv_reader:
                if "." not in dep[1]:
                    # Title row
                    continue
                caller_class = self.utils.shorten_name(dep[1], granularity)
                callee_class = self.utils.shorten_name(dep[2], granularity)

                if "AbstractActionBean" in callee_class:
                    x = 1

                if first_row == "":
                    first_row = f"'{caller_class}'  '{callee_class}'"
                if caller_class in observed_nodes and callee_class in observed_nodes:
                    dep_graph.append(
                        {
                            "source": caller_class,
                            "target": callee_class,
                            "weight": dep[3],
                        }
                    )
        if len(dep_graph) == 0:
            print(f"WARNING: Graph is empty for {application} {granularity}")
        return dep_graph

    def copy_visualizations(self):
        self.copy_visualization("jpetstore", "ground_truth")
        self.copy_visualization(
            "jpetstore", "mono2micro", p_count="3", variant="business"
        )
        self.copy_visualization("jpetstore", "hydec")
        self.copy_visualization("jpetstore", "datacentric")
        self.copy_visualization("jpetstore", "log2ms")
        self.copy_visualization(
            "jpetstore",
            "tomicroservices",
            granularity="method",
            p_count="3",
            variant="functionality",
        )
        self.copy_visualization("jpetstore", "cargo", granularity="method", p_count="3")

        self.copy_visualization("spring-petclinic", "ground_truth")
        self.copy_visualization(
            "spring-petclinic", "mono2micro", p_count="3", variant="business"
        )
        self.copy_visualization("spring-petclinic", "hydec")
        self.copy_visualization("spring-petclinic", "datacentric")
        self.copy_visualization("spring-petclinic", "log2ms")
        self.copy_visualization(
            "spring-petclinic",
            "tomicroservices",
            granularity="method",
            p_count="3",
            variant="functionality",
        )
        self.copy_visualization(
            "spring-petclinic", "cargo", granularity="method", p_count="3"
        )

        self.copy_visualization("partsunlimited", "ground_truth")
        self.copy_visualization(
            "partsunlimited", "mono2micro", p_count="5", variant="business"
        )
        self.copy_visualization("partsunlimited", "hydec")
        self.copy_visualization("partsunlimited", "datacentric")
        # self.copy_visualization("partsunlimited", "log2ms")
        self.copy_visualization(
            "partsunlimited",
            "tomicroservices",
            granularity="method",
            p_count="5",
            variant="functionality",
        )
        self.copy_visualization(
            "partsunlimited", "cargo", granularity="method", p_count="5"
        )

        self.copy_visualization("demo", "ground_truth")
        self.copy_visualization("demo", "mono2micro", p_count="4", variant="business")
        self.copy_visualization("demo", "hydec")
        self.copy_visualization("demo", "datacentric")
        # self.copy_visualization("demo", "log2ms")
        self.copy_visualization(
            "demo",
            "tomicroservices",
            granularity="method",
            p_count="4",
            variant="functionality",
        )
        self.copy_visualization("demo", "cargo", granularity="method", p_count="5")

    def copy_visualization(
        self, app, tool, granularity="class", p_count="n", variant="default"
    ):
        p_count = f"{p_count}_partitions"
        visualization_path = self.data_repository.get_visualization_path(
            app, tool, p_count, variant, granularity
        )
        base_path = "../../../data/decomposition_visualizations"
        if app == "jpetstore":
            app_name = "1_jpetstore"
        elif app == "spring-petclinic":
            app_name = "2_spring-petclinic"
        elif app == "partsunlimited":
            app_name = "3_partsunlimited"
        else:
            app_name = "4_demo"

        if tool == "ground_truth":
            tool_name = "1_ground_truth"
        elif tool == "mono2micro":
            tool_name = "2_mono2micro"
        elif tool == "hydec":
            tool_name = "3_hydec"
        elif tool == "datacentric":
            tool_name = "4_datacentric"
        elif tool == "log2ms":
            tool_name = "5_log2ms"
        elif tool == "tomicroservices":
            tool_name = "6_tomicroservices"
        else:
            tool_name = "7_cargo"
        output_path = (
            f"{base_path}/{app_name}/{tool_name}/{granularity}_visualization.json"
        )

        with open(visualization_path, "r") as vis_file:
            with open(output_path, "w") as out_file:
                vis = vis_file.read()
                out_file.write(vis)

    def generate(self, applications, relationships):
        for application in applications:
            print(f"Generating for application: {application}")
            app_obj = Application(application, self.application_repository)
            table_accesses = DataAccess(
                app_obj, DependencyGraph(app_obj, self.data_repository)
            ).get_table_accesses()

            for tool in self.manifest.get_available_tools(application):
                print(f"-> Generating for tool: {tool}")
                for partition in self.manifest.get_partition_count_options(
                    application, tool
                ):
                    for decomposition_type in self.manifest.get_decomposition_variants(
                        tool
                    ):
                        granularities = ["method_level"]
                        tool_granularity = self.manifest.get_granularity(tool)
                        if tool_granularity == "class":
                            granularities.append("class_level")
                        for granularity in granularities:
                            visualization_json = {}
                            for relationship in relationships:
                                decomposition = (
                                    self.decomposition_repository.get_decomposition(
                                        tool=tool,
                                        application=application,
                                        partition_count=partition,
                                        granularity=granularity,
                                        variant=decomposition_type,
                                        filtered=True,
                                        with_ids=True,
                                    )
                                )
                                if "UNOBSERVED" in decomposition:
                                    decomposition.pop("UNOBSERVED")
                                if "uncounted" in decomposition:
                                    decomposition.pop("uncounted")
                                relationship_graph_path = (
                                    self.data_repository.get_relationship_path(
                                        application, relationship, granularity
                                    )
                                )

                                relationship_json = self.get_relationship_json(
                                    decomposition,
                                    relationship_graph_path,
                                    granularity,
                                    application,
                                )
                                if relationship == "structural_static":
                                    rel_name = "1_structural_static"
                                elif relationship == "semantic_names":
                                    rel_name = "2_semantic_names"
                                elif relationship == "evolutionary_contributors":
                                    rel_name = "3_evolutionary_contributors"
                                elif relationship == "evolutionary_commits":
                                    rel_name = "4_evolutionary_commits"

                                visualization_json[rel_name] = relationship_json

                                # Add table accesses
                                table_decomposition = {}
                                table_links = []
                                for table in table_accesses.keys():
                                    table_decomposition[f"{table} TABLE"] = [
                                        {"id": f"{table} TABLE"}
                                    ]
                                    node_names = list(
                                        map(
                                            lambda node: self.utils.shorten_name(
                                                node, granularity, is_method_name=True
                                            ),
                                            table_accesses[table],
                                        )
                                    )
                                    unique_node_names, counts = np.unique(
                                        node_names, return_counts=True
                                    )
                                    for node, count in zip(unique_node_names, counts):
                                        table_links.append(
                                            {
                                                "source": node,
                                                "target": f"{table} TABLE",
                                                "weight": str(count),
                                            }
                                        )
                                table_decomposition.update(decomposition)
                                table_visualization = {
                                    "links": table_links,
                                    "decomposition": table_decomposition,
                                }

                                visualization_json["4_database_access"] = (
                                    table_visualization
                                )

                                # Add use cases
                                decomp_id = DecompositionIdentifier(
                                    tool=tool,
                                    application=application,
                                    partition_count=partition,
                                    granularity=granularity,
                                    variant=decomposition_type,
                                )
                                use_case_accesses = (
                                    self.application_repository.get_use_cases(
                                        decomp_id.get_application()
                                    )
                                )

                                use_case_decomposition = {}
                                use_case_links = []
                                for use_case in use_case_accesses.keys():
                                    use_case_decomposition[f"{use_case} USE CASE"] = [
                                        {"id": f"{use_case.upper()} USE CASE"}
                                    ]
                                    node_names = list(
                                        map(
                                            lambda node: self.utils.shorten_name(
                                                node, granularity, is_method_name=True
                                            ),
                                            use_case_accesses[use_case],
                                        )
                                    )
                                    unique_node_names, counts = np.unique(
                                        node_names, return_counts=True
                                    )
                                    for node, count in zip(unique_node_names, counts):
                                        use_case_links.append(
                                            {
                                                "target": node,
                                                "source": f"{use_case.upper()} USE CASE",
                                                "weight": str(count),
                                            }
                                        )
                                use_case_decomposition.update(decomposition)
                                use_case_visualization = {
                                    "links": use_case_links,
                                    "decomposition": use_case_decomposition,
                                }

                                visualization_json["3_business_use_cases"] = (
                                    use_case_visualization
                                )

                            visualization_path = (
                                self.data_repository.get_visualization_path(
                                    application,
                                    tool,
                                    partition,
                                    decomposition_type,
                                    granularity.split("_")[0],
                                )
                            )
                            with open(visualization_path, "w") as visualization_file:
                                visualization_file.write(
                                    json.dumps(
                                        visualization_json, indent=4, sort_keys=True
                                    )
                                )

        self.copy_visualizations()
