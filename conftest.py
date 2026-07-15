import pytest

@pytest.fixture(scope="session")
def session_config():
    print("\n[session] loading config once")
    yield {"env": "test"}
    print("\n[session] teardown")

@pytest.fixture(scope="module")
def shared_dataset():
    print("\n[module] building dataset")
    data = [1, 2, 3]
    yield data
    print("\n[module] clearing dataset")

# @pytest.fixture(scope="function")
# def calculator():
#     from legacy.calculator import Calculator
#     calc = Calculator()
#     yield calc
#     del calc  # explicit teardown, even if trivial — shows you understand the lifecycle
