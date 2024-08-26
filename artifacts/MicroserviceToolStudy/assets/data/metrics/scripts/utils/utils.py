class Utils:
    def shorten_class_name(self, fully_qualified_name, is_method_name=False):
        fully_qualified_name = fully_qualified_name.strip()
        if is_method_name:
            return fully_qualified_name.split(".")[-2]
        else:
            return fully_qualified_name.split(".")[-1]

    def shorten_method_name(self, fully_qualified_name):
        fully_qualified_name = fully_qualified_name.strip()
        if len(fully_qualified_name.split(".")) < 2:
            print(f"WARNING: Fully qualified name too short: {fully_qualified_name}")
        return fully_qualified_name.split(".")[-2] + "." + fully_qualified_name.split(".")[-1]

    def shorten_name(self, fully_qualified_name, granularity, is_method_name=False):
        if "method" in granularity:
            return self.shorten_method_name(fully_qualified_name)
        else:
            return self.shorten_class_name(fully_qualified_name, is_method_name)

    def remove_ids(self, decomposition):
        no_id_decomp = {}
        for partition in decomposition.keys():
            no_id_decomp[partition] = list(map(lambda n: n["id"], decomposition[partition]))
        return no_id_decomp

    def get_node_partition_assignments(self, decomposition):
        partition_assignments = {}
        for partition_name in decomposition.keys():
            for node in decomposition[partition_name]:
                if node not in partition_assignments.keys():
                    partition_assignments[node] = []
                partition_assignments[node].append(partition_name)
        return partition_assignments

    def get_decomposition_size(self, decomposition, include_unobserved=False):
        size = 0
        for partition_name in decomposition.keys():
            if not include_unobserved and partition_name == "UNOBSERVED":
                continue
            size += len(decomposition[partition_name])
        return size

    def get_partition_count(self, decomposition, include_unobserved=False):
        size = 0
        for partition_name in decomposition.keys():
            if not include_unobserved and partition_name == "UNOBSERVED":
                continue
            size += 1
        return size
