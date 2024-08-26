class Utils:
    def get_short_method_name(long_method_name: str):
        class_name = long_method_name.split()[-2]
        method_name = long_method_name.split()[-1].strip()
        return f"{class_name}.{method_name}"
