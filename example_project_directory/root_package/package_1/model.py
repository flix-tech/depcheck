class Hello:
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"Hello {self.name}!"
