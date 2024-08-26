class DecompositionIdentifier:
    def __init__(self, application: str, tool: str, partition_count: str, variant: str, granularity: str):
        if application not in ["demo", "jpetstore", "partsunlimited", "spring-petclinic"]:
            raise Exception(f"Invalid application name: {application}")
        self._application = application

        if tool not in ["cargo", "datacentric", "ground_truth", "hydec", "log2ms", "mono2micro", "tomicroservices", "mosaic", "mem"]:
            raise Exception(f"Invalid tool name: {tool}")
        self._tool = tool

        self._partition_count = partition_count
        self._variant = variant

        if granularity not in ["method_level", "class_level"]:
            raise Exception(f"Invalid granularity: {granularity}")
        self._granularity = granularity

    def get_application(self):
        return self._application

    def get_tool(self):
        return self._tool

    def get_partition_count(self):
        return self._partition_count

    def get_variant(self):
        return self._variant

    def get_granularity(self):
        return self._granularity
