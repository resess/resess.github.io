import json

from access.applications import ApplicationRepository
from access.decompositions import DecompositionRepository
from access.manifest import Manifest
from utils.utils import Utils


class MethodLevelDecompositionConstructor:
    def __init__(self, decomposition_repository: DecompositionRepository, manifest: Manifest,
                 application_repository: ApplicationRepository, utils: Utils):
        self.decomposition_repository = decomposition_repository
        self.manifest = manifest
        self.application_repository = application_repository
        self.utils = utils

    def migrate_class_decompositions(self, application, tool, partition_count, variant):
        decomposition_folder = self.decomposition_repository.get_decomposition_folder(tool, application,
                                                                                      partition_count, variant)

        method_level_tools = ["tomicroservices", "cargo", "mosaic", "ground_truth"]
        if tool in method_level_tools:
            if tool == "tomicroservices":
                with open(f"{decomposition_folder}/decomposition.json", "r") as old_file:
                    with open(f"{decomposition_folder}/method_decomposition.json", "w", newline='\n') as new_file:
                        old_json = json.load(old_file)
                        pretty_json = json.dumps(old_json)
                        new_file.write(pretty_json)
            # There is no class-level decomposition to migrate
            return

        with open(f"{decomposition_folder}/decomposition.json", "r") as old_file:
            with open(f"{decomposition_folder}/class_decomposition.json", "w", newline='\n') as new_file:
                old_json = json.load(old_file)
                pretty_json = json.dumps(old_json)
                new_file.write(pretty_json)

    def migrate_all_class_decompositions(self, applications):
        for application in applications:
            print(f"Generating for application: {application}")
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
                            self.migrate_class_decompositions(application, tool, partition_count, variant)

    def construct_method_decompositions(self, applications):
        for application in applications:
            print(f"Constructing for application: {application}")
            for tool in self.manifest.get_available_tools(application):
                print(f"-> Constructing for tool: {tool}")
                for partition_count in self.manifest.get_partition_count_options(
                    application, tool
                ):
                    for variant in self.manifest.get_decomposition_variants(tool):
                        granularities = ["method_level"]
                        if self.manifest.get_granularity(tool) == "class":
                            granularities.append("class_level")
                        for granularity in granularities:
                            if "method" in granularity and tool not in ["cargo", "tomicroservices", "mosaic", "ground_truth"]:
                                class_decomposition = self.decomposition_repository.get_decomposition(tool,
                                                                                                      application,
                                                                                                      partition_count,
                                                                                                      "class_level",
                                                                                                      variant, filtered=False)

                                class_assignments = self.utils.get_node_partition_assignments(class_decomposition)

                                method_decomposition = {}
                                for partition_name in class_decomposition.keys():
                                    method_decomposition[partition_name] = []

                                method_names = self.application_repository.get_methods(application)
                                for method_name in method_names:
                                    class_name = self.utils.shorten_class_name(method_name, is_method_name=True)
                                    if class_name in class_assignments:
                                        method_decomposition[class_assignments[class_name][0]].append(
                                            self.utils.shorten_method_name(method_name)
                                        )
                                self.decomposition_repository.write_decomposition(tool,
                                                                                  application,
                                                                                  partition_count,
                                                                                  variant,
                                                                                  granularity,
                                                                                  method_decomposition,
                                                                                  False)
