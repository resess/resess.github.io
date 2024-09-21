raw_path = "/Users/sarah/Documents/University/ReSeSS/repos/2022_microservices_tools/data/tool_decomposition_raw_results/mem"
data_path = "../../../code/scripts/metrics/data/decompositions"
import shutil

import os
import csv
import json


def get_subfolder_names(folder_path):
    # Check if the given path is a directory
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a valid directory.")
        return []

    all_items = os.listdir(folder_path)
    subfolders = [
        item for item in all_items if os.path.isdir(os.path.join(folder_path, item))
    ]

    return subfolders


def get_file_names(folder_path):
    # Check if the given path is a directory
    if not os.path.isdir(folder_path):
        print(f"{folder_path} is not a valid directory.")
        return []

    all_items = os.listdir(folder_path)
    subfolders = [
        item for item in all_items if not os.path.isdir(os.path.join(folder_path, item))
    ]

    return subfolders


for app in ["demo", "petclinic", "jpetstore", "PartsUnlimitedMRP"]:
    variants = get_subfolder_names(f"{raw_path}/{app}")

    data_app_name = app
    if app == "petclinic":
        data_app_name = "spring-petclinic"
    elif app == "PartsUnlimitedMRP":
        data_app_name = "partsunlimited"

    for variant in variants:
        for file in get_file_names(f"{raw_path}/{app}/{variant}"):
            if "config" in file:
                continue
            variant_suffix = (
                file.replace(f"{app}", "").replace("spring-", "").split(".")[0]
            )
            # os.makedirs(f"{data_path}/{data_app_name}/mem/{variant}{variant_suffix}")
            # shutil.copy(f"{raw_path}/{app}/{variant}/{file}", f"{data_path}/{data_app_name}/mem/{variant}{variant_suffix}/original.csv")

            with open(
                f"{data_path}/{data_app_name}/mem/{variant}{variant_suffix}/original.csv"
            ) as original_file:
                reader = csv.reader(original_file)
                next(reader, None)

                decomp = {}

                for row in reader:
                    if row[0] not in decomp.keys():
                        decomp[row[0]] = []

                    decomp[row[0]].append({"id": row[1].split(".java")[0]})

                with open(
                    f"{data_path}/{data_app_name}/mem/{variant}{variant_suffix}/class_decomposition.json",
                    "w", newline='\n'
                ) as decomp_file:
                    decomp_file.write(
                        json.dumps({"MEM": {"decomposition": decomp}}, indent=4)
                    )
