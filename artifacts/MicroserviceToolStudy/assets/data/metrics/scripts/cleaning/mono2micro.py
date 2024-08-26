import json

from access.decompositions import DecompositionRepository
from access.manifest import Manifest


class Mono2MicroCleaner:
    def __init__(self, decomposition_repository: DecompositionRepository, manifest: Manifest):
        self.decomposition_repository = decomposition_repository
        self.manifest = manifest

    def clean(self, applications):
        for application in applications:
            for partition_count in self.manifest.get_partition_count_options(application,
                                                                                       "mono2micro"):
                original_decomposition_path = self.decomposition_repository.get_raw_decomposition_path(
                    "mono2micro",
                    application,
                    partition_count)

                with open(original_decomposition_path, "r") as original_decomposition_file:
                    original_decomposition = json.load(original_decomposition_file)
                    business_partition = original_decomposition["micro_detail_partition_by_business_logic"]["nodes"]
                    natural_partition = original_decomposition["micro_detail_partition_by_natural_seam"]["nodes"]

                    self._parse_partition(business_partition, application, partition_count, "business")
                    self._parse_partition(natural_partition, application, partition_count, "natural")

    def _parse_partition(self, partition, application, partition_count, variant):
        decomposition = {}
        for node in partition:
            if node["category"] == "Unobserved":
                continue
            if node["category"] not in decomposition.keys():
                decomposition[node["category"]] = []
            decomposition[node["category"]].append(node["name"])

        self.decomposition_repository.write_decomposition(
            tool="mono2micro",
            application=application,
            partition_count=partition_count,
            variant=variant,
            granularity="class_level",
            decomposition=decomposition,
            filtered=False
        )
