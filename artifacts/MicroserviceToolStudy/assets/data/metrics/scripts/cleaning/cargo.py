import json

from access.applications import ApplicationRepository
from access.decompositions import DecompositionRepository
from access.manifest import Manifest
from utils.utils import Utils
import os


class CargoCleaner:
    def __init__(self, decomposition_repository: DecompositionRepository, manifest: Manifest,
                 application_repository: ApplicationRepository, utils: Utils):
        self.decomposition_repository = decomposition_repository
        self.manifest = manifest
        self.application_repository = application_repository
        self.utils = utils

    def clean(self, applications):
        for application in applications:
            for partition_count in self.manifest.get_partition_count_options(application, "cargo"):
                original_path = self.decomposition_repository.get_raw_decomposition_path("cargo", application,
                                                                                         partition_count)

                print (f'INFO: cargo raw decomposition path is {original_path}') 
                with open(original_path, "r") as original_file:
                    original_json = json.load(original_file)

                application_classes = self.application_repository.get_classes(application)
                application_methods = self.application_repository.get_methods(application)

                class_decomposition = {}
                method_decomposition = {}

                for node in original_json.keys():
                    partition_name = str(original_json[node])
                    # CARGO marks constructor methods with "<clinit>" or "<init>"
                    if "<clinit>" in node or "<init>" in node:
                        qualifiers = node.split(".")
                        qualifiers[-1] = qualifiers[-2]
                        node = ".".join(qualifiers)

                    if node in application_classes:
                        if partition_name not in class_decomposition.keys():
                            class_decomposition[partition_name] = []
                        class_decomposition[partition_name].append({"id": self.utils.shorten_class_name(node)})
                    elif node in application_methods:
                        if partition_name not in method_decomposition.keys():
                            method_decomposition[partition_name] = []
                        method_decomposition[partition_name].append({"id": self.utils.shorten_method_name(node)})
                    elif not node.startswith("org.springframework"):
                        print(f"WARNING: Node not present: {node}")

                method_decomposition_path = os.path.abspath(self.decomposition_repository.get_method_decomposition_path("cargo",
                                                                                                        application,
                                                                                                        partition_count,
                                                                                                        filtered=False))
                with open(method_decomposition_path, "w") as method_decomposition_file:
                    json.dump({"tool": {"decomposition": method_decomposition}}, method_decomposition_file)

                print(f"INFO: Writing cleaned method-level decomposition to: {method_decomposition_path}")

                class_decomposition_path = self.decomposition_repository.get_class_decomposition_path("cargo",
                                                                                                      application,
                                                                                                      partition_count,
                                                                                                      filtered=False)
                with open(class_decomposition_path, "w") as class_decomposition_file:
                    json.dump({"tool": {"decomposition": class_decomposition}}, class_decomposition_file)

                print(f"INFO: Writing cleaned class-level decomposition to: {class_decomposition_path}")