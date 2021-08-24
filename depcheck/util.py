from typing import List


def flatten(list_2d: List[List[str]]) -> List[str]:
    return [item for sublist in list_2d for item in sublist]
