from root_package.package_1.model import Hello


class GetHelloQuery:
    def __init__(self, name="World") -> None:
        self.name = name


class GetHelloHandler:
    def __init__(self) -> None:
        pass

    def __call__(self, query: GetHelloQuery) -> str:
        return str(Hello(query.name))
