def flatten(list_2d: list[list[str]]) -> list[str]:
    return [item for sublist in list_2d for item in sublist]
