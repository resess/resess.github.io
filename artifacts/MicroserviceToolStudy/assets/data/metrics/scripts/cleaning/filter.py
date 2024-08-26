from access.applications import ApplicationRepository
from access.decompositions import DecompositionRepository
from access.manifest import Manifest
from utils.utils import Utils


class DecompositionFilter:
    def __init__(
        self,
        decomposition_repository: DecompositionRepository,
        application_repository: ApplicationRepository,
        utils: Utils,
        manifest: Manifest,
    ):
        self.decomposition_repository = decomposition_repository
        self.application_repository = application_repository
        self.utils = utils
        self.manifest = manifest

    def filter(self, application, tool, partition_count, variant, granularity):
        decomposition = self.decomposition_repository.get_decomposition(
            tool=tool,
            application=application,
            partition_count=partition_count,
            granularity=granularity,
            variant=variant,
            filtered=False,
        )
        if "method" in granularity:
            nodes = list(
                map(
                    lambda name: self.utils.shorten_method_name(name),
                    self.application_repository.get_methods(application),
                )
            )
        else:
            nodes = list(
                map(
                    lambda name: self.utils.shorten_class_name(name),
                    self.application_repository.get_classes(application),
                )
            )

        observed_nodes = []
        for partition_name in decomposition.keys():
            partition = decomposition[partition_name]
            new_node_list = []
            for old_node in partition:
                if old_node in nodes:
                    observed_nodes += [old_node]
                    new_node_list += [old_node]
            decomposition[partition_name] = list(set(new_node_list))

        old_decomp = decomposition
        decomposition = {}
        for partition_name in old_decomp.keys():
            if len(old_decomp[partition_name]) > 0:
                decomposition[partition_name] = old_decomp[partition_name]

        decomposition["UNOBSERVED"] = []
        for node in nodes:
            if node not in observed_nodes:
                decomposition["UNOBSERVED"] += [node]
        decomposition["UNOBSERVED"] = list(set(decomposition["UNOBSERVED"]))

        self.decomposition_repository.write_decomposition(
            tool=tool,
            application=application,
            partition_count=partition_count,
            variant=variant,
            granularity=granularity,
            decomposition=decomposition,
        )

    def filter_all(self, applications):
        for application in applications:
            print(f"Filtering application: {application}")
            for tool in self.manifest.get_available_tools(application):
                print(f"-> Filtering tool: {tool}")
                for (
                    partition_count
                ) in self.manifest.get_partition_count_options(
                    application, tool
                ):
                    for variant in self.manifest.get_decomposition_variants(tool):
                        for granularity in self.manifest.get_granularities(tool):
                            self.filter(
                                application=application,
                                tool=tool,
                                partition_count=partition_count,
                                variant=variant,
                                granularity=granularity,
                            )
