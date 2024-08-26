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

        output_file = open(out_path, "w")
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

    def _parse_logs(self, application, data_repo: DataRepository, app_repo: ApplicationRepository):
        log_file = open(data_repo.get_git_log_path(application), "r")
        method_commits = {}
        commit_authors = {}
        current_method = ""

        for line in log_file.readlines():
            if line.startswith("method"):
                method_name = line.split("|")[0].replace("method: ", "").strip()
                method_commits[method_name] = set()
                current_method = method_name
            else:
                commit_hash = line.split("|")[0].replace("commit: ", "").strip()
                author = line.split("|")[1].replace("author: ", "").strip()
                method_commits[current_method].add(commit_hash)
                commit_authors[commit_hash] = author

        return (method_commits, commit_authors)

    def extract_method_relationships(self, application, data_repo: DataRepository, app_repo: ApplicationRepository):
        self._generate_method_logs(application, data_repo, app_repo)
        method_commits, commit_authors = self._parse_logs(application, data_repo, app_repo)
        commit_graph = ",methodA,methodB,weight\n"
        contributor_graph = ",methodA,methodB,weight\n"
        for methodA in method_commits.keys():
            for methodB in method_commits.keys():
                if methodA != methodB:
                    methodACommits = method_commits[methodA]
                    methodBCommits = method_commits[methodB]
                    intersection = methodACommits.intersection(methodBCommits)
                    union = methodACommits.union(methodBCommits)
                    commit_weight = np.divide(len(intersection), len(union))
                    if commit_weight > 0:
                        commit_graph += f"0,{methodA},{methodB},{commit_weight}\n"

                    methodAContributors = set(
                        list(map(lambda hash: commit_authors[hash], methodACommits))
                    )
                    methodBContributors = set(
                        list(map(lambda hash: commit_authors[hash], methodBCommits))
                    )

                    intersection = methodAContributors.intersection(methodBContributors)
                    union = methodAContributors.union(methodBContributors)
                    contributor_weight = np.divide(len(intersection), len(union))
                    if contributor_weight > 0:
                        contributor_graph += (
                            f"0,{methodA},{methodB},{contributor_weight}\n"
                        )

        commit_output_file = open(data_repo.get_commit_graph_path(application), "w")
        commit_output_file.write(commit_graph)

        contributor_output_file = open(
            data_repo.get_contributor_graph_path(application), "w"
        )
        contributor_output_file.write(contributor_graph)
