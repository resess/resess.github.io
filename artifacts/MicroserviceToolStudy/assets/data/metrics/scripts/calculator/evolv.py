for app in ["demo", "jpetstore", "partsunlimited", "spring-petclinic"]:
    with open(
        f"../../../code/scripts/metrics/data/relationship_graphs/{app}/method_level/history.log"
    ) as history_file:
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

        with open(
            f"../../../code/scripts/metrics/data/relationship_graphs/{app}/class_level/commits.csv",
            "w",
        ) as outfile:
            for edge_label in edges.keys():
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

        with open(
            f"../../../code/scripts/metrics/data/relationship_graphs/{app}/class_level/contributors.csv",
            "w",
        ) as outfile:
            for edge_label in a_edges.keys():
                edge = a_edges[edge_label]
                outfile.write(f"0,{edge_label},{edge}\n")
