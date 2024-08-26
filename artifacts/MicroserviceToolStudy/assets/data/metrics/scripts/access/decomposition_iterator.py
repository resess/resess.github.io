class DecompositionIterator:

    def __init__(self, applications, manifest):
        self.applications = applications
        self.manifest = manifest

    def get_list(self):
        for application in self.applications:
            for tool in self.manifest.get_available_tools(application):
                for partition_count in self.manifest.get_partition_count_options(
                    application, tool
                ):
                    for variant in self.manifest.get_decomposition_variants(tool):
                        granularities = ["method_level"]
                        if self.manifest.get_granularity(tool) == "class":
                            granularities.append("class_level")
                        for granularity in granularities: