from example.root.foo.animals import Cat


class Zoo:
    def __init__(self) -> None:
        self.animals = []
        self.animals.append(Cat('Kitty'))
        self.animals.append(Cat('Leo'))

    def list_animals(self) -> str:
        animal_names = [str(i) for i in self.animals]
        return ', '.join(animal_names)
