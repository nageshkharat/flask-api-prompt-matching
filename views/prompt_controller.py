"""
View layer (Controller) for handling API requests and responses.
Handles HTTP requests and delegates business logic to the service layer.
"""

from flask import request, jsonify
from typing import Tuple, Dict, Any
import json

from services.prompt_service import PromptMatchingService


class PromptController:
    """Controller class for handling prompt matching API requests."""
    
    @staticmethod
    def match_prompt() -> Tuple[Dict[str, Any], int]:
        """
        Handle POST request for prompt matching.
        
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            # Ensure the request contains JSON data
            if not request.is_json:
                return {
                    "success": False,
                    "error": "Missing Data",
                    "message": "Request must contain JSON data"
                }, 400
            
            # Get the JSON data from the request
            request_data = request.get_json()
            
            # Handle case where JSON is empty or None
            if request_data is None:
                return {
                    "success": False,
                    "error": "Missing Data",
                    "message": "Request body cannot be empty"
                }, 400
            
            # Process the request using the service layer
            result = PromptMatchingService.process_request(request_data)
            
            # Determine the appropriate HTTP status code
            if result["success"]:
                return {
                    "success": True,
                    "prompt": result["prompt"]
                }, 200
            else:
                # Handle different error types with appropriate status codes
                error_type = result.get("error", "Unknown Error")
                
                if error_type == "Missing Data":
                    status_code = 400  # Bad Request
                elif error_type == "Invalid Prompt":
                    status_code = 422  # Unprocessable Entity
                else:
                    status_code = 500  # Internal Server Error
                
                response = {
                    "success": False,
                    "error": error_type
                }
                
                # Include additional message or details if available
                if "message" in result:
                    response["message"] = result["message"]
                if "details" in result:
                    response["details"] = result["details"]
                
                return response, status_code
                
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Missing Data",
                "message": "Invalid JSON format"
            }, 400
        except Exception as e:
            # Handle any unexpected errors gracefully
            return {
                "success": False,
                "error": "Internal Error",
                "message": f"An unexpected error occurred: {str(e)}"
            }, 500
    
    @staticmethod
    def health_check() -> Tuple[Dict[str, Any], int]:
        """
        Simple health check endpoint.
        
        Returns:
            Tuple of (response_data, status_code)
        """
        return {
            "status": "healthy",
            "message": "Prompt Matching API is running"
        }, 200 