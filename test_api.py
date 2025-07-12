"""
Test script for the Prompt Matching API.
Tests various scenarios including valid inputs, missing data, and invalid prompts.
"""

import requests
import json
from typing import Dict, Any


class APITester:
    """Class to test the Prompt Matching API."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.endpoint = f"{base_url}/match-prompt"
    
    def test_valid_prompts(self):
        """Test all valid prompt matching scenarios."""
        print("Testing Valid Prompts:")
        print("-" * 50)
        
        valid_test_cases = [
            {
                "name": "Prompt 1",
                "data": {
                    "situation": "Commercial Auto",
                    "level": "Structure",
                    "file_type": "Summary Report",
                    "data": "test data"
                },
                "expected": "Prompt 1"
            },
            {
                "name": "Prompt 2",
                "data": {
                    "situation": "General Liability",
                    "level": "Summarize",
                    "file_type": "Deposition",
                    "data": "test data"
                },
                "expected": "Prompt 2"
            },
            {
                "name": "Prompt 3",
                "data": {
                    "situation": "Commercial Auto",
                    "level": "Summarize",
                    "file_type": "Summons",
                    "data": "test data"
                },
                "expected": "Prompt 3"
            },
            {
                "name": "Prompt 4",
                "data": {
                    "situation": "Workers Compensation",
                    "level": "Structure",
                    "file_type": "Medical Records",
                    "data": "test data"
                },
                "expected": "Prompt 4"
            },
            {
                "name": "Prompt 5",
                "data": {
                    "situation": "Workers Compensation",
                    "level": "Summarize",
                    "file_type": "Summons",
                    "data": "test data"
                },
                "expected": "Prompt 5"
            }
        ]
        
        for test_case in valid_test_cases:
            self._run_test(test_case)
    
    def test_missing_data_scenarios(self):
        """Test missing data error scenarios."""
        print("\nTesting Missing Data Scenarios:")
        print("-" * 50)
        
        missing_data_cases = [
            {
                "name": "Missing situation field",
                "data": {
                    "level": "Structure",
                    "file_type": "Summary Report",
                    "data": "test data"
                },
                "expected_error": "Missing Data"
            },
            {
                "name": "Missing level field",
                "data": {
                    "situation": "Commercial Auto",
                    "file_type": "Summary Report",
                    "data": "test data"
                },
                "expected_error": "Missing Data"
            },
            {
                "name": "Missing file_type field",
                "data": {
                    "situation": "Commercial Auto",
                    "level": "Structure",
                    "data": "test data"
                },
                "expected_error": "Missing Data"
            },
            {
                "name": "Missing data field",
                "data": {
                    "situation": "Commercial Auto",
                    "level": "Structure",
                    "file_type": "Summary Report"
                },
                "expected_error": "Missing Data"
            },
            {
                "name": "Empty JSON",
                "data": {},
                "expected_error": "Missing Data"
            },
            {
                "name": "Null values",
                "data": {
                    "situation": None,
                    "level": "Structure",
                    "file_type": "Summary Report",
                    "data": "test data"
                },
                "expected_error": "Missing Data"
            }
        ]
        
        for test_case in missing_data_cases:
            self._run_test(test_case)
    
    def test_invalid_prompt_scenarios(self):
        """Test invalid prompt error scenarios."""
        print("\nTesting Invalid Prompt Scenarios:")
        print("-" * 50)
        
        invalid_prompt_cases = [
            {
                "name": "Invalid situation",
                "data": {
                    "situation": "Invalid Situation",
                    "level": "Structure",
                    "file_type": "Summary Report",
                    "data": "test data"
                },
                "expected_error": "Invalid Prompt"
            },
            {
                "name": "Invalid level",
                "data": {
                    "situation": "Commercial Auto",
                    "level": "Invalid Level",
                    "file_type": "Summary Report",
                    "data": "test data"
                },
                "expected_error": "Invalid Prompt"
            },
            {
                "name": "Invalid file_type",
                "data": {
                    "situation": "Commercial Auto",
                    "level": "Structure",
                    "file_type": "Invalid File Type",
                    "data": "test data"
                },
                "expected_error": "Invalid Prompt"
            },
            {
                "name": "Valid fields but no matching prompt",
                "data": {
                    "situation": "General Liability",
                    "level": "Structure",
                    "file_type": "Summary Report",
                    "data": "test data"
                },
                "expected_error": "Invalid Prompt"
            }
        ]
        
        for test_case in invalid_prompt_cases:
            self._run_test(test_case)
    
    def test_edge_cases(self):
        """Test edge cases and malformed requests."""
        print("\nTesting Edge Cases:")
        print("-" * 50)
        
        # Test with extra whitespace
        whitespace_test = {
            "name": "Whitespace in values",
            "data": {
                "situation": "  Commercial Auto  ",
                "level": "  Structure  ",
                "file_type": "  Summary Report  ",
                "data": "test data"
            },
            "expected": "Prompt 1"
        }
        self._run_test(whitespace_test)
        
        # Test non-JSON request
        print(f"Testing non-JSON request...")
        try:
            response = requests.post(
                self.endpoint,
                data="not json",
                headers={"Content-Type": "text/plain"}
            )
            result = response.json()
            success = (
                not result.get("success", True) and 
                result.get("error") == "Missing Data"
            )
            print(f"✓ Non-JSON request: {'PASS' if success else 'FAIL'}")
        except Exception as e:
            print(f"✗ Non-JSON request: FAIL - {e}")
    
    def _run_test(self, test_case: Dict[str, Any]):
        """Run a single test case."""
        try:
            response = requests.post(
                self.endpoint,
                json=test_case["data"],
                headers={"Content-Type": "application/json"}
            )
            
            result = response.json()
            
            if "expected" in test_case:
                # Test for successful prompt match
                success = (
                    result.get("success", False) and 
                    result.get("prompt") == test_case["expected"]
                )
                status = "PASS" if success else "FAIL"
                print(f"✓ {test_case['name']}: {status}")
                if not success:
                    print(f"  Expected: {test_case['expected']}")
                    print(f"  Got: {result}")
            
            elif "expected_error" in test_case:
                # Test for expected error
                success = (
                    not result.get("success", True) and 
                    result.get("error") == test_case["expected_error"]
                )
                status = "PASS" if success else "FAIL"
                print(f"✓ {test_case['name']}: {status}")
                if not success:
                    print(f"  Expected error: {test_case['expected_error']}")
                    print(f"  Got: {result}")
        
        except Exception as e:
            print(f"✗ {test_case['name']}: FAIL - {e}")
    
    def run_all_tests(self):
        """Run all test scenarios."""
        print("=" * 60)
        print("PROMPT MATCHING API TESTS")
        print("=" * 60)
        
        self.test_valid_prompts()
        self.test_missing_data_scenarios()
        self.test_invalid_prompt_scenarios()
        self.test_edge_cases()
        
        print("\n" + "=" * 60)
        print("TESTS COMPLETED")
        print("=" * 60)


if __name__ == "__main__":
    # Note: Make sure the Flask app is running before executing these tests
    print("Make sure the Flask app is running on http://localhost:5000")
    print("Run: python app.py")
    print()
    
    tester = APITester()
    tester.run_all_tests() 