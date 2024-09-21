from .data_repository import DataRepository

import os


def get_subfolder_names(folder_path):
    # Check if the given path is a directory
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a valid directory.")
        return []

    # Get a list of all items in the directory
    all_items = os.listdir(folder_path)

    # Filter out only the directories (sub-folders)
    subfolders = [
        item for item in all_items if os.path.isdir(os.path.join(folder_path, item))
    ]

    return subfolders


class Manifest:
    def __init__(self, data_repository: DataRepository):
        self.manifest = data_repository.get_decompositions_manifest()

    def get_available_tools(self, application):
        return ["mem"] + list(self.manifest["applications"][application].keys())

    def get_decomposition_variants(self, tool):
        variants = ["default"]
        if tool == "mem":
            return variants
        if "decomposition_types" in self.manifest["tools"][tool].keys():
            variants = self.manifest["tools"][tool]["decomposition_types"]
        return variants

    def get_partition_count_options(self, application, tool):
        if tool == "mem":
            return get_subfolder_names(
                f"./data/decompositions/{application}/mem"
            )
        return list(
            filter(
                lambda p: self.manifest["applications"][application][tool][p],
                list(self.manifest["applications"][application][tool].keys()),
            )
        )

    def get_granularity(self, tool):
        if tool == "mem":
            return "class"
        return self.manifest["tools"][tool]["granularity"]

    def get_granularities(self, tool):
        granularities = ["method_level"]
        if self.get_granularity(tool) == "class":
            granularities.append("class_level")
        return granularities
