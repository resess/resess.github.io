from access.application import Application
from calculator.dependency_graph import DependencyGraph


class DataAccess:
    def __init__(self, application: Application, dependency_graph: DependencyGraph):
        self.application = application
        self.dependency_graph = dependency_graph

    def get_table_accesses(self):
        granularity = "method_level"
        direct_table_accesses = self.application.get_table_accesses()

        indirect_table_accesses = {}

        for table in direct_table_accesses.keys():
            indirect_accesses = set()
            if "method" not in granularity:
                direct_table_accesses[table] = list(map(lambda n: n[0:n.rfind(".")], direct_table_accesses[table]))
            for node in direct_table_accesses[table]:
                indirect_accesses = indirect_accesses.union(self.dependency_graph.get_indirect_usages(
                    node, granularity))
            indirect_table_accesses[table] = indirect_accesses

        return indirect_table_accesses
