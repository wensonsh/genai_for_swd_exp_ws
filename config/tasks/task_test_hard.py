import json
from typing import List
import streamlit as st
from itertools import permutations


# Test cases
test_cases = [
    {"input": ["ab", "ba"], "expected_output": [[1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]},
    {"input": ["aa","ac"], "expected_output": [[2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]},
    {"input": ["aa","bb","cc"], "expected_output": [[2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]},
]

def test_solution_hard(solution_code: str):
    # strip leading/trailing whitespace from the solution code
    solution_code = solution_code.strip()

    # define a dictionary to hold the local variables for exec
    local_vars = {}

    # execute the solution code
    exec(solution_code, globals(), local_vars)

    # check if the Solution class is defined
    if "Solution" not in local_vars:
        raise ValueError("Solution class not found in the provided code.")

    # create an instance of the Solution class
    solution_instance = local_vars["Solution"]()

    # run the test cases
    for i, test_case in enumerate(test_cases):
        input_data = test_case["input"]
        expected_output = test_case["expected_output"]

        # call the supersequences method
        result = solution_instance.supersequences(input_data)

        # check if the result matches the expected output
        # check if the result matches the expected output
        if result == expected_output:
            st.success(
                f"Test case {i + 1} with input {input_data} passed.\n\nExpected {expected_output}, got {result}.",
                icon="✅")
        else:
            st.warning(
                f"Test case {i + 1} with input {input_data} failed. \n\nExpected {expected_output}, got {result}.",
                icon="❌")
