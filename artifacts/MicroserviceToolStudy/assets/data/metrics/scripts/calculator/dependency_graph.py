from access.application import Application
from access.data_repository import DataRepository
import xml.etree.ElementTree as et


class DependencyGraph:
    class Edge:
        def __init__(self, source, dest, count):
            self.source = source
            self.dest = dest
            self.count = count

        def get_source(self):
            return self.source

        def get_dest(self):
            return self.dest

        def get_count(self):
            return self.count

    def __init__(self, application: Application, data_repository: DataRepository):
        self.data_repository = data_repository
        self.application = application
        self.class_edges = []
        self.method_edges = []
        self._setup()

    def _setup(self):
        dependency_path = self.data_repository.get_dependency_path(self.application.get_name())

        tree = et.parse(dependency_path)
        root = tree.getroot()

        package_base = self.application.get_package_base()

        # Find dependencies between classes
        for package in root:
            package_name = package[0].text
            if package_name is not None and package_name.startswith(package_base):
                for package_child in package:
                    if package_child.tag == "class":
                        class_name = package_child[0].text
                        for class_child in package_child:
                            # Iterate through each of the class's features (read: methods) to find dependencies
                            if class_child.tag == "feature":
                                method_name = class_child[0].text.split("(")[0]
                                for feature_child in class_child:
                                    if feature_child.tag == "outbound":
                                        # Method - Method dependency
                                        if feature_child.attrib["type"] == "feature":
                                            dependency_method = feature_child.text.split("(")[0]
                                            if dependency_method.startswith(
                                                    package_base
                                            ):
                                                self.add_edge(method_name, dependency_method, "method")
                                                dependency_class = dependency_method[0:dependency_method.rfind(".")]
                                                self.add_edge(class_name, dependency_class, "class")
                                        # Method - Class dependency
                                        elif feature_child.attrib["type"] == "class":
                                            dependency_class = feature_child.text
                                            self.add_edge(class_name, dependency_class, "class")

                            elif package_child.tag == "outbound":
                                # Class - Class dependency
                                dependency_class = package_child.text
                                # Class - Method dependency
                                if package_child.attrib["type"] == "feature":
                                    dependency_method = package_child.text.split("(")[0]
                                    dependency_class = dependency_method[0:dependency_method.rfind(".")]

                                if dependency_class.startswith(package_base):
                                    self.add_edge(class_name, dependency_class, "class")

    def add_edge(self, source, dest, granularity):
        edges = self.method_edges if "method" in granularity else self.class_edges
        count = 1
        existing_edge = next(filter(lambda edge: edge.source == source and edge.dest == dest, edges), None)
        if existing_edge is not None:
            count += existing_edge.get_count()

        if "method" in granularity:
            self.method_edges.append(DependencyGraph.Edge(source, dest, count))
        else:
            self.class_edges.append(DependencyGraph.Edge(source, dest, count))

    def get_direct_usages(self, node, granularity):
        edges = self.method_edges if "method" in granularity else self.class_edges
        return set(map(lambda edge: edge.source, filter(lambda edge: edge.dest == node, edges)))

    def get_indirect_usages(self, node, granularity):
        old_usage_count = 0
        usages = self.get_direct_usages(node, granularity).union([node])

        while len(usages) != old_usage_count:
            old_usage_count = len(usages)
            for usage in usages:
                usages = usages.union(self.get_direct_usages(usage, granularity))

        return usages
