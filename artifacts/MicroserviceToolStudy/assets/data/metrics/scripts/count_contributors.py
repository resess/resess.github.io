for app in ["demo", "jpetstore", "open-mrs", "partsunlimited", "spring-petclinic"]:
    contributors = set()
    commits = set()
    with open(
        f"../../../code/scripts/metrics/data/relationship_graphs2/{app}/method_level/history.log"
    ) as history_file:
        for line in history_file.readlines():
            if line.startswith("commit:"):
                commits.add(line.split("commit: ")[1].split(" | author")[0])
                contributors.add(line.split("author: ")[1].strip())

    print(f"{app} | contributors: {len(contributors)} | commits: {len(commits)}")
