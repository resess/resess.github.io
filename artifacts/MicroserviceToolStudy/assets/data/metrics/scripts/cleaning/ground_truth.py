import json

from access.application import Application
from access.applications import ApplicationRepository
from access.decompositions import DecompositionRepository
from access.manifest import Manifest
from utils.utils import Utils
import csv
import os


class GroundTruthCleaner:
    def __init__(
        self,
        decomposition_repository: DecompositionRepository,
        manifest: Manifest,
        application_repository: ApplicationRepository,
        utils: Utils,
    ):
        self.decomposition_repository = decomposition_repository
        self.manifest = manifest
        self.application_repository = application_repository
        self.utils = utils

    def extract_rsfs(self, applications):
        for application in applications:
            decomp_folder = os.path.abspath(self.decomposition_repository.get_decomposition_folder(
                "ground_truth", application, "n_partitions", "default"
            ))

            output_folder = os.path.abspath("./data/applications")
            original_class_path = f"{decomp_folder}/{application}_classes.csv"
            class_rsf = ""
            csv_reader = csv.reader(open(original_class_path), delimiter=",")
            for row in csv_reader:
                if "." not in row[0] or len(row) < 3:
                    continue
                partition = row[2].strip()
                class_name = row[1].strip()
                class_rsf += f"contain {partition} {class_name}\n"

            # with open(original_class_path, "r") as original_class_assigments:
            #     for line in original_class_assigments.readlines():
            #         if "." not in line:
            #             continue
            #         row = line.split(",")
            #         partition = row[2].strip()
            #         class_name = row[1].strip()
            #         class_rsf += f"contain {partition} {class_name}\n"

            with open(
                f"{output_folder}/{application}/ground_truth/ground_truth.rsf", "w", newline='\n'
            ) as class_output:
                class_output.write(class_rsf)
            with open(f"{decomp_folder}/class_decomposition.rsf", "w", newline='\n') as class_output:
                class_output.write(class_rsf)

            original_method_path = f"{decomp_folder}/{application}_methods.csv"
            method_rsf = ""
            csv_reader = csv.reader(open(original_method_path), delimiter=",")
            for row in csv_reader:
                if len(row) < 2 or "." not in row[0]:
                    continue
                partition = row[1]
                long_method_name = row[0].split("(")[0]
                method_name = (
                    long_method_name.split(".")[-2]
                    + "."
                    + long_method_name.split(".")[-1]
                )
                method_rsf += f"contain {partition} {method_name}\n"
            # with open(original_method_path, "r") as original_method_assigments:
            #     for line in original_method_assigments.readlines():
            #         if "." not in line:
            #             continue
            #         partition = line.split("),")[0].strip()
            #         long_method_name = line[0:line.rfind(",")].split("(")[0]
            #         method_name = long_method_name.split(".")[-2] + "." + long_method_name.split(".")[-1]
            #         method_rsf += f"contain {partition} {method_name}\n"

            with open(
                f"{output_folder}/{application}/ground_truth/method_ground_truth.rsf", "w", newline='\n'
            ) as method_output:
                method_output.write(method_rsf)
            with open(
                f"{decomp_folder}/method_decomposition.rsf", "w", newline='\n'
            ) as method_output:
                method_output.write(method_rsf)

    def clean_new(self, applications):
        for application in applications:
            decomp_folder = os.path.abspath(self.decomposition_repository.get_decomposition_folder(
                "ground_truth", application, "n_partitions", "default"
            ))
            original_class_path = os.path.abspath(f"{decomp_folder}/{application}_classes.csv")
            original_method_path = os.path.abspath(f"{decomp_folder}/{application}_methods.csv")

            class_decomp = {}
            with open(original_class_path, "r") as original_class_assigments:
                for line in original_class_assigments.readlines():
                    if "." not in line:
                        continue
                    row = line.split(",")
                    partition = row[2].strip()
                    class_name = row[1].strip()
                    if partition not in class_decomp.keys():
                        class_decomp[partition] = []
                    class_decomp[partition].append({"id": class_name})

            class_decomp_path = os.path.abspath((
                self.decomposition_repository.get_class_decomposition_path(
                    "ground_truth", application, "n_partitions", filtered=False
                )
            ))
            with open(class_decomp_path, "w", newline='\n') as class_decomposition_file:
                json.dump(
                    {"tool": {"decomposition": class_decomp}}, class_decomposition_file
                )

            print(
                f"INFO: Writing cleaned class-level decomposition to: {class_decomp_path}"
            )

            method_decomp = {}
            csv_reader = csv.reader(open(original_method_path), delimiter=",")
            for row in csv_reader:
                if len(row) < 2 or "." not in row[0]:
                    continue
                partition = row[1]
                long_method_name = row[0].split("(")[0]
                method_name = (
                    long_method_name.split(".")[-2]
                    + "."
                    + long_method_name.split(".")[-1]
                )
                if partition not in method_decomp.keys():
                    method_decomp[partition] = []
                method_decomp[partition].append({"id": method_name})

            # with open(original_method_path, "r") as original_method_assigments:
            #     for line in original_method_assigments.readlines():
            #         if "." not in line:
            #             continue
            #         partition = line.split("),")[0].strip()
            #         long_method_name = line[0:line.rfind(",")].split("(")[0]
            #         method_name = long_method_name.split(".")[-2] + "." + long_method_name.split(".")[-1]
            #         if partition not in method_decomp.keys():
            #             method_decomp[partition] = []
            #         method_decomp[partition].append({"id": method_name})

            method_decomp_path = os.path.abspath((
                self.decomposition_repository.get_method_decomposition_path(
                    "ground_truth", application, "n_partitions", filtered=False
                )
            ))
            with open(method_decomp_path, "w", newline='\n') as method_decomposition_file:
                json.dump(
                    {"tool": {"decomposition": method_decomp}},
                    method_decomposition_file,
                )

            print(
                f"INFO: Writing cleaned method-level decomposition to: {method_decomp_path}"
            )

    def clean(self, applications):
        for application in applications:
            for partition_count in self.manifest.get_partition_count_options(
                application, "ground_truth"
            ):
                original_path = (
                    self.decomposition_repository.get_raw_decomposition_path(
                        "ground_truth", application, partition_count
                    )
                )

                decomposition = {}
                with open(original_path, "r") as original_file:
                    for line in original_file.readlines():
                        row = line.strip().split(" ")
                        partition = row[1]
                        class_name = row[2]
                        if partition not in decomposition.keys():
                            decomposition[partition] = []
                        decomposition[partition].append({"id": class_name})

                decomposition_path = os.path.abspath((
                    self.decomposition_repository.get_class_decomposition_path(
                        "ground_truth", application, partition_count, filtered=False
                    )
                ))
                with open(decomposition_path, "w", newline='\n') as class_decomposition_file:
                    json.dump(
                        {"tool": {"decomposition": decomposition}},
                        class_decomposition_file,
                    )

                print(
                    f"INFO: Writing cleaned class-level decomposition to: {decomposition_path}"
                )
