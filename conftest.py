import pytest

@pytest.fixture
def word_dict_example() -> list[dict]:
    word = [{"twins": "Either of two people (or, less commonly,\
    animals) who shared the same uterus at the same time; one who was \
    born at the same birth as a sibling."}]
    return word