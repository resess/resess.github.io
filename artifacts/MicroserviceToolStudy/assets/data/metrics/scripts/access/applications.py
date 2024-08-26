class ApplicationRepository:
    def __init__(self, base_path):
        self.base_path = base_path

    def get_classes(self, application):
        class_list_path = f"{self.base_path}/{application}/classes.txt"
        with open(class_list_path, "r") as class_list_file:
            return list(map(lambda line: line.strip(), class_list_file.readlines()))

    def get_methods(self, application):
        method_list_path = f"{self.base_path}/{application}/methods.txt"
        with open(method_list_path, "r") as method_list_file:
            return list(map(lambda line: line.strip(), method_list_file.readlines()))

    def get_table_accesses(self, application):
        table_accesses_path = f"{self.base_path}/{application}/table_accesses.csv"
        with open(table_accesses_path, "r") as table_accesses_file:
            table_accesses = {}
            for line in table_accesses_file.readlines()[1:]:
                row = line.split(",")
                table = row[0]
                access_type = row[1]
                method = row[2].strip()
                if access_type in ["Direct", "Global"]:
                    if table not in table_accesses.keys():
                        table_accesses[table] = []
                    table_accesses[table].append(method)
            return table_accesses

    def get_use_cases(self, application):
        trace_path = f"{self.base_path}/{application}/trace.log"
        with open(trace_path, "r") as trace_file:
            use_cases = {}
            current_use_case = None
            for line in trace_file.readlines():
                if line.startswith("SF"):
                    current_use_case = line.split(":")[1].split("<")[0]
                    use_cases[current_use_case] = []
                else:
                    row = line.split("#")
                    method_name = row[0].split(":")[1] + "." + row[1].split(":")[1]
                    use_cases[current_use_case].append(method_name)

            return use_cases
