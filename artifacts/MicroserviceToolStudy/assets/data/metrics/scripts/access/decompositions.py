import json

from models.decomposition_identifier import DecompositionIdentifier


class DecompositionRepository:
    def __init__(self, base_path):
        self.base_path = base_path

    def get_raw_decomposition_path(self, tool, application, partition_count, variant="default"):
        if tool in ["mono2micro", "mosaic"]:
            return f"{self.get_decomposition_folder(tool, application, partition_count, variant)}/original.json"
        return f"{self.get_decomposition_folder(tool, application, partition_count, variant)}/original"

    def get_method_decomposition_path(self, tool, application, partition_count, variant="default", filtered=True):
        file_name = "filtered_method_decomposition.json" if filtered else "method_decomposition.json"
        return f"{self.get_decomposition_folder(tool, application, partition_count, variant)}/{file_name}"

    def get_class_decomposition_path(self, tool, application, partition_count, variant="default", filtered=True):
        file_name = "filtered_class_decomposition.json" if filtered else "class_decomposition.json"
        return f"{self.get_decomposition_folder(tool, application, partition_count, variant)}/{file_name}"

    def get_decomposition_path(self, tool, application, partition_count, granularity, variant="default", filtered=True):
        if "method" in granularity:
            return self.get_method_decomposition_path(tool, application, partition_count, variant=variant, filtered=filtered)
        else:
            return self.get_class_decomposition_path(tool, application, partition_count, variant=variant, filtered=filtered)

    def get_decomposition(self, tool, application, partition_count, granularity, variant="default", filtered=True, with_ids=False):
        decomposition_id = DecompositionIdentifier(tool=tool,
                                                   application=application,
                                                   partition_count=partition_count,
                                                   granularity=granularity,
                                                   variant=variant)
        return self.get_decomposition_by_id(decomposition_id, filtered, with_ids)

    def get_decomposition_by_id(self, decomposition_id: DecompositionIdentifier, filtered=True, with_ids=False):
        decomposition_path = self.get_decomposition_path(decomposition_id.get_tool(),
                                                         decomposition_id.get_application(),
                                                         decomposition_id.get_partition_count(),
                                                         decomposition_id.get_granularity(),
                                                         decomposition_id.get_variant(),
                                                         filtered)

        with open(decomposition_path, "r") as decomposition_file:
            decomposition_json = json.load(decomposition_file)

            decomposition = decomposition_json
            if "tool" in decomposition_json.keys():
                decomposition = decomposition_json["tool"]["decomposition"]
            elif "MEM" in decomposition_json.keys():
                decomposition = decomposition_json["MEM"]["decomposition"]

            if not with_ids:
                for partition_name in decomposition.keys():
                    old_partition = decomposition[partition_name]
                    new_partition = list(map(lambda node: node["id"], old_partition))
                    decomposition[partition_name] = new_partition

            return decomposition

    def get_decomposition_folder(self, tool, application, partition_count, variant):
        if variant == "default":
            return f"{self.base_path}/{application}/{tool}/{partition_count}"
        else:
            return f"{self.base_path}/{application}/{tool}/{partition_count}/{variant}"

    def write_decomposition(self, tool, application, partition_count, variant, granularity, decomposition, filtered=True):
        file_path = self.get_decomposition_path(tool, application, partition_count, granularity, variant, filtered)
        with open(file_path, "w", newline='\n') as filtered_decomposition_file:
            for partition_name in decomposition.keys():
                old_partition = decomposition[partition_name]
                new_partition = list(map(lambda node: {"id": node}, old_partition))
                new_partition.sort(key=lambda x: x['id'])
                decomposition[partition_name] = new_partition

            filtered_decomposition_file.write(json.dumps({"tool": {"decomposition": decomposition}}, indent=4))
