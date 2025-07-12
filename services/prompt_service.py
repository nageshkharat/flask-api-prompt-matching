"""
Service layer for prompt matching logic.
Contains business logic for validating input and matching prompts.
"""

from typing import Dict, Any, Union


class PromptMatchingService:
    """Service class for handling prompt matching logic."""
    
    # Define the valid values for each field
    VALID_SITUATIONS = ["Commercial Auto", "General Liability", "Workers Compensation"]
    VALID_LEVELS = ["Structure", "Summarize"]
    VALID_FILE_TYPES = ["Medical Records", "Deposition", "Summons", "Summary Report"]
    
    # Define the prompt matching criteria
    PROMPT_MAPPING = {
        ("Commercial Auto", "Structure", "Summary Report"): "Prompt 1",
        ("General Liability", "Summarize", "Deposition"): "Prompt 2",
        ("Commercial Auto", "Summarize", "Summons"): "Prompt 3",
        ("Workers Compensation", "Structure", "Medical Records"): "Prompt 4",
        ("Workers Compensation", "Summarize", "Summons"): "Prompt 5"
    }
    
    @classmethod
    def validate_input(cls, data: Dict[str, Any]) -> Dict[str, str]:
        """
        Validate the input data structure and required fields.
        
        Args:
            data: Dictionary containing the input data
            
        Returns:
            Dictionary with validation errors, empty if valid
            
        Raises:
            ValueError: If missing required fields
        """
        required_fields = ["situation", "level", "file_type", "data"]
        missing_fields = []
        
        # Check for missing fields
        for field in required_fields:
            if field not in data or data[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            raise ValueError(f"Missing Data: Required fields missing: {', '.join(missing_fields)}")
        
        # Validate field values
        validation_errors = {}
        
        situation = data.get("situation", "").strip()
        level = data.get("level", "").strip()
        file_type = data.get("file_type", "").strip()
        
        if situation not in cls.VALID_SITUATIONS:
            validation_errors["situation"] = f"Invalid situation. Must be one of: {', '.join(cls.VALID_SITUATIONS)}"
        
        if level not in cls.VALID_LEVELS:
            validation_errors["level"] = f"Invalid level. Must be one of: {', '.join(cls.VALID_LEVELS)}"
        
        if file_type not in cls.VALID_FILE_TYPES:
            validation_errors["file_type"] = f"Invalid file_type. Must be one of: {', '.join(cls.VALID_FILE_TYPES)}"
        
        return validation_errors
    
    @classmethod
    def match_prompt(cls, situation: str, level: str, file_type: str) -> str:
        """
        Match the input criteria to a prompt.
        
        Args:
            situation: The situation type
            level: The level type
            file_type: The file type
            
        Returns:
            The matched prompt name
            
        Raises:
            ValueError: If no matching prompt is found
        """
        # Create the lookup key
        lookup_key = (situation.strip(), level.strip(), file_type.strip())
        
        # Try to find a matching prompt
        matched_prompt = cls.PROMPT_MAPPING.get(lookup_key)
        
        if matched_prompt is None:
            raise ValueError("Invalid Prompt: No matching prompt found for the given criteria")
        
        return matched_prompt
    
    @classmethod
    def process_request(cls, data: Dict[str, Any]) -> Dict[str, Union[str, bool]]:
        """
        Process the complete request: validate input and match prompt.
        
        Args:
            data: Dictionary containing the request data
            
        Returns:
            Dictionary with success status and result/error message
        """
        try:
            # Validate input
            validation_errors = cls.validate_input(data)
            
            if validation_errors:
                return {
                    "success": False,
                    "error": "Invalid Prompt",
                    "details": validation_errors
                }
            
            # Extract the validated values
            situation = data["situation"].strip()
            level = data["level"].strip()
            file_type = data["file_type"].strip()
            
            # Match the prompt
            matched_prompt = cls.match_prompt(situation, level, file_type)
            
            return {
                "success": True,
                "prompt": matched_prompt
            }
            
        except ValueError as e:
            error_message = str(e)
            if "Missing Data" in error_message:
                return {
                    "success": False,
                    "error": "Missing Data",
                    "message": error_message
                }
            elif "Invalid Prompt" in error_message:
                return {
                    "success": False,
                    "error": "Invalid Prompt",
                    "message": error_message
                }
            else:
                return {
                    "success": False,
                    "error": "Processing Error",
                    "message": error_message
                }
        except Exception as e:
            return {
                "success": False,
                "error": "Internal Error",
                "message": f"An unexpected error occurred: {str(e)}"
            } 