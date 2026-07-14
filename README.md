Python Calculator Project

A simple calculator project written in Python. This project provides basic arithmetic operations and includes automated tests to verify that the calculator works correctly in different scenarios.

Installation
1. Clone the repository
git clone <repository-url>
cd <project-directory>
2. Create and activate a virtual environment (recommended)

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate

On Windows:

python -m venv venv
venv\Scripts\activate
3. Install dependencies

Install the required Python packages using:

pip install -r requirements.txt

If the project does not have external dependencies, no additional installation is required.

Running the Tests

The project uses Python's testing framework to run automated tests.

Run all tests with:

pytest

or, if using Python's built-in test runner:

python -m unittest

A successful test run confirms that the calculator functions behave as expected.

Test Coverage

The tests cover the main calculator functionality, including:

Addition
Testing positive numbers
Testing negative numbers
Testing combinations of positive and negative values
Testing addition with zero
Subtraction
Testing subtraction of positive numbers
Testing negative number calculations
Testing subtraction resulting in zero
Multiplication
Testing multiplication of positive and negative values
Testing multiplication by zero
Testing multiplication by one
Division
Testing division with valid inputs
Testing decimal results
Testing division by zero handling
Edge Cases
Large number calculations
Zero as an input value
Invalid operations and error handling (where applicable)

The goal of the test suite is to ensure that the calculator produces correct results and handles unexpected inputs safely.