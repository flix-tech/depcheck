from typing import List

from depcheck.util import flatten


def test_flatten_returns_items_of_inner_lists_in_a_flatten_list() -> None:
    # Arrange
    list_2d: List[List[str]] = [["a", "b", "c"], ["1", "2"], ["x", "y", "z"]]
    expected_flatten_list: List[str] = ["a", "b", "c", "1", "2", "x", "y", "z"]

    # Act
    result: List[str] = flatten(list_2d)

    # Assert
    assert expected_flatten_list == result
