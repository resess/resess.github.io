import json

from access.decompositions import DecompositionRepository
from access.manifest import Manifest


class MosaicCleaner:
    def __init__(self, decomposition_repository: DecompositionRepository, manifest: Manifest):
        self.decomposition_repository = decomposition_repository
        self.manifest = manifest

    def clean(self, applications):
        for application in applications:
            original_decomposition_path = self.decomposition_repository.get_raw_decomposition_path(
                "mosaic",
                application,
                "n_partitions")

            with open(f'./data/applications/{application}/classes.txt') as class_file:
                classes = class_file.readlines()

            with open(f'./data/applications/{application}/methods.txt') as method_file:
                methods = method_file.readlines()

            with open(original_decomposition_path, "r") as original_decomposition_file:
                original_decomposition = json.load(original_decomposition_file)["mosaic"]["decomposition"]
                new_decomposition = {}

                for partition in original_decomposition:
                    new_decomposition[partition] = []

                    for entity in original_decomposition[partition]:
                        if "." in entity["id"]:
                            new_decomposition[partition].append(entity["id"])
                        else:
                            for method in methods:
                                tokens = method.split(".")
                                short_method = tokens[-2] + "." + tokens[-1]
                                if short_method.startswith(entity["id"] + "."):
                                    new_decomposition[partition].append(short_method.strip())

            self.decomposition_repository.write_decomposition(
                tool="mosaic",
                application=application,
                partition_count="n_partitions",
                granularity="method_level",
                variant="default",
                decomposition=new_decomposition,
                filtered=False
            )
