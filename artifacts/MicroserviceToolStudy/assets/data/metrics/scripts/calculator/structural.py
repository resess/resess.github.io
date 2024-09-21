import xml.etree.ElementTree as et
from collections import Counter

from access.application import Application
from access.data_repository import DataRepository


class StructuralRelationshipExtractor:
    class ClassNode:
        def __init__(self, class_name: str):
            self.class_name = class_name
            self.outbound: list[str] = []
            self.inbound: list[str] = []

    def extract_method_dependencies(self, dependency_path, package_base, output_path):
        dependencies = {}
        tree = et.parse(dependency_path)
        root = tree.getroot()

        # Find dependencies between classes
        for package in root:
            package_name = package[0].text
            if package_name is not None and package_name.startswith(package_base):
                for clazz in package:
                    if clazz.tag == "class":
                        class_name = clazz[0].text
                        for child in clazz:
                            # Iterate through each of the class's features (read: methods) to find dependencies
                            if child.tag == "feature":
                                method_name = child[0].text.split("(")[0]
                                for feature_child in child:
                                    if (
                                            feature_child.tag == "outbound"
                                            or feature_child.tag == "inbound"
                                    ):
                                        if feature_child.attrib["type"] == "feature":
                                            dependency_method = (
                                                feature_child.text.split("(")[0]
                                            )
                                            if dependency_method.startswith(
                                                    package_base
                                            ):
                                                if (
                                                        method_name
                                                        not in dependencies.keys()
                                                ):
                                                    dependencies[method_name] = {
                                                        "outbound": [],
                                                        "inbound": [],
                                                    }
                                                dependencies[method_name][
                                                    feature_child.tag
                                                ].append(dependency_method)

        csv_output = ",MethodA,MethodB,ReferenceCount\n"
        counter = 0
        for method in dependencies.keys():
            dependency_counts = dict(Counter(dependencies[method]["outbound"]))
            for dependency in dependency_counts.keys():
                if method != dependency:
                    csv_output += f"{counter},{method},{dependency},{dependency_counts[dependency]}\n"

        output_file = open(output_path, "w", newline='\n')
        output_file.write(csv_output)
        output_file.close()

    def extract_class_dependencies(self, dependency_path, package_base, output_path):
        dependencies = {}
        # Find all classes under the package base
        classes = {}
        tree = et.parse(dependency_path)
        root = tree.getroot()
        for package in root:
            package_name = package[0].text
            if package_name is not None and package_name.startswith(package_base):
                for clazz in package:
                    if clazz.tag == "class":
                        class_name = clazz[0].text
                        classes[class_name] = {"outbound": [], "inbound": []}

        # Find dependencies between classes
        for package in root:
            package_name = package[0].text
            if package_name == "com.coveros.training.helpers":
                x = 1
            if package_name is not None and package_name.startswith(package_base):
                for clazz in package:
                    if clazz.tag == "class":
                        class_name = clazz[0].text
                        for child in clazz:
                            # Iterate through each of the class's features (read: methods) to find dependencies
                            if child.tag == "feature":
                                for feature_child in child:
                                    if (
                                            feature_child.tag == "outbound"
                                            or feature_child.tag == "inbound"
                                    ):
                                        dependency_class = feature_child.text
                                        if feature_child.attrib["type"] == "feature":
                                            dependency_method = feature_child.text.split("(")[0]
                                            dependency_class = dependency_method[0:dependency_method.rfind(".")]
                                            if dependency_class.startswith(package_base):
                                                if class_name not in dependencies.keys():
                                                    dependencies[class_name] = {
                                                        "outbound": [],
                                                        "inbound": [],
                                                    }
                                                dependencies[class_name][
                                                    feature_child.tag
                                                ].append(dependency_class)
                            # elif child.tag == "outbound" or child.tag == "inbound":
                            #     dependency_class = child.text
                            #     if child.attrib["type"] == "feature":
                            #         dependency_method = child.text.split("(")[0]
                            #         dependency_class = dependency_method[0:dependency_method.rfind(".")]
                            #     if dependency_class.startswith(package_base):
                            #         if class_name not in dependencies.keys():
                            #             dependencies[class_name] = {
                            #                 "outbound": [],
                            #                 "inbound": [],
                            #             }
                            #         dependencies[class_name][child.tag].append(
                            #             dependency_class
                            #         )

        csv_output = ",ClassA,ClassB,ReferenceCount\n"
        counter = 0
        for clazz in dependencies.keys():
            dependency_counts = dict(Counter(dependencies[clazz]["outbound"]))
            for dependency in dependency_counts.keys():
                if clazz != dependency:
                    csv_output += f"{counter},{clazz},{dependency},{dependency_counts[dependency]}\n"

        output_file = open(output_path, "w")
        output_file.write(csv_output)
        output_file.close()

    def extract_relationships(self, applications, data_repo: DataRepository, application_repository):
        for app in applications:
            application = Application(app, application_repository)
            dependency_path = data_repo.get_dependency_path(application.get_name())
            package_base = application.get_package_base()
            output_path = data_repo.get_method_static_structural_graph_path(application.get_name())

            self.extract_method_dependencies(dependency_path, package_base, output_path)

            output_path = data_repo.get_class_static_structural_graph_path(application.get_name())

            self.extract_class_dependencies(dependency_path, package_base, output_path)

