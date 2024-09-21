from access.data_repository import DataRepository
import subprocess as sp
import numpy as np

from access.applications import ApplicationRepository
from access.application import Application


class EvolutionaryRelationshipExtrator:
    def _generate_method_logs(self, app, data_repo: DataRepository, app_repo: ApplicationRepository):
        application = Application(app, app_repo)
        methods = application.get_methods()
        application_src_path = data_repo.get_application_src_path(app)
        out_path = data_repo.get_git_log_path(app)

        output_file = open(out_path, "w", newline='\n')
        output_file.write("")
        output_file.close()

        missing_methods = set()

        for method in methods:
            # Find the path to the file that the method is located in
            qualifiers = method.split(".")[:-1]
            functionName = method.split(".")[len(method.split(".")) - 1].strip()
            file_path = f"{application_src_path}/{'/'.join(qualifiers)}"
            file_path = file_path.split("$")[0] + ".java"
            file_path = file_path.replace("[]", "")
            src_file = open(file_path, "r")

            found = False
            start = -1
            brackets = -1
            done = False
            lines = src_file.readlines()
            for i, line in enumerate(lines):
                if (
                    functionName in line
                    and (line.strip()[-1] == "{" or lines[i + 1].strip() == "{")
                    and "class" not in line
                ):
                    found = True
                    brackets = 1
                    start = i + 1

                else:
                    for c in line:
                        if c == "{":
                            brackets += 1
                        elif c == "}":
                            brackets -= 1

                if found and brackets == 0 and not done:
                    output_file = open(out_path, "a")
                    output_file.write(
                        f"method: {method.strip()} | lines: {start}:{i + 1} | file: {file_path}\n"
                    )
                    output_file.close()
                    sp.call(
                        f'cd {application_src_path} && git log --format="commit: %H | author: %an" -s -L {start},{i + 1}:{file_path} >> {out_path}',
                        shell=True,
                    )
                    done = True
            if not found:
                missing_methods.add(method)

        print(
            f"Found {len(methods) - len(missing_methods)} out of {len(methods)} methods ({(len(methods) - len(missing_methods))/len(methods)}%)"
        )

    def _generate_graphs(self, application, data_repo: DataRepository):
        with open(data_repo.get_git_log_path(application), "r") as history_file:
            commit_map = {}
            author_map = {}
            curr_method = ""
            for line in history_file.readlines():
                if line.startswith("method:"):
                    curr_method = line.split("method: ")[1].split(" | ")[0]
                else:
                    assert line.startswith("commit:")
                    commit_hash = line.split("commit: ")[1].split(" | ")[0]
                    author = line.split("author: ")[1].strip()

                    if commit_hash not in commit_map.keys():
                        commit_map[commit_hash] = []
                    commit_map[commit_hash].append(curr_method)

                    if author not in author_map.keys():
                        author_map[author] = set()
                    author_map[author].add(curr_method)

            edges = {}

            for commit in commit_map.keys():
                methods = commit_map[commit]
                for method_a in methods:
                    for method_b in methods:
                        if method_a == method_b:
                            continue

                        if method_a <= method_b:
                            edge_label = f"{method_a},{method_b}"
                        else:
                            edge_label = f"{method_b},{method_a}"

                        if edge_label not in edges.keys():
                            edges[edge_label] = 0
                        edges[edge_label] += 0.5

            with open(data_repo.get_commit_graph_path(application), "w", newline='\n') as outfile:
                sorted_keys = sorted(edges.keys())
                for edge_label in sorted_keys:
                    edge = edges[edge_label]
                    outfile.write(f"0,{edge_label},{edge}\n")

            a_edges = {}

            for author in author_map.keys():
                methods = author_map[author]
                for method_a in methods:
                    for method_b in methods:
                        if method_a == method_b:
                            continue

                        if method_a <= method_b:
                            edge_label = f"{method_a},{method_b}"
                        else:
                            edge_label = f"{method_b},{method_a}"

                        if edge_label not in a_edges.keys():
                            a_edges[edge_label] = 0
                        a_edges[edge_label] += 0.5

            with open(data_repo.get_contributor_graph_path(application), "w", newline='\n') as outfile:
                sorted_keys = sorted(a_edges.keys())
                for edge_label in sorted_keys:
                    edge = a_edges[edge_label]
                    outfile.write(f"0,{edge_label},{edge}\n")


    def extract_method_relationships(self, application, data_repo: DataRepository, app_repo: ApplicationRepository):
        self._generate_method_logs(application, data_repo, app_repo)
        self._generate_graphs(application, data_repo)
