from access.applications import ApplicationRepository


class Application:
    def __init__(self, application_name, application_repository: ApplicationRepository):
        self.application_name = application_name
        self.application_repository = application_repository

    def get_classes(self):
        return self.application_repository.get_classes(self.application_name)

    def get_methods(self):
        return self.application_repository.get_methods(self.application_name)

    def get_table_accesses(self):
        return self.application_repository.get_table_accesses(self.application_name)

    def get_use_cases(self):
        return self.application_repository.get_use_cases(self.application_name)

    def get_name(self):
        return self.application_name

    def get_package_base(self):
        if self.application_name == "demo":
            return "com.coveros.training"
        elif self.application_name == "jpetstore":
            return "org.mybatis.jpetstore"
        elif self.application_name == "partsunlimited":
            return "smpl.ordering"
        elif self.application_name == "spring-petclinic":
            return "org.springframework.samples.petclinic"
        else:
            raise Exception("Invalid application name")
