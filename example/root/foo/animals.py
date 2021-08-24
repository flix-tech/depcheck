class Cat:
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"Meow {self.name}!"
