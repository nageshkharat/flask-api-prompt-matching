"""
Main Flask application file.
Contains route definitions and error handling.
"""

from flask import Flask, jsonify
from views.prompt_controller import PromptController


def create_app():
    """Application factory function to create and configure the Flask app."""
    app = Flask(__name__)
    
    # Configure the app
    app.config['JSON_SORT_KEYS'] = False  # Preserve JSON key order
    
    # Register routes
    register_routes(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    return app


def register_routes(app):
    """Register all application routes."""
    
    @app.route('/match-prompt', methods=['POST'])
    def match_prompt():
        """
        POST endpoint for matching prompts based on input criteria.
        
        Expected JSON input:
        {
            "situation": "Commercial Auto",
            "level": "Structure", 
            "file_type": "Summary Report",
            "data": ""
        }
        
        Returns:
        {
            "success": true,
            "prompt": "Prompt 1"
        }
        """
        response_data, status_code = PromptController.match_prompt()
        return jsonify(response_data), status_code
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        response_data, status_code = PromptController.health_check()
        return jsonify(response_data), status_code
    
    @app.route('/', methods=['GET'])
    def index():
        """Root endpoint with API information."""
        return jsonify({
            "message": "Prompt Matching API",
            "version": "1.0.0",
            "endpoints": {
                "POST /match-prompt": "Match a system prompt based on input criteria",
                "GET /health": "Health check endpoint",
                "GET /": "API information"
            },
            "supported_values": {
                "situation": ["Commercial Auto", "General Liability", "Workers Compensation"],
                "level": ["Structure", "Summarize"],
                "file_type": ["Medical Records", "Deposition", "Summons", "Summary Report"]
            }
        }), 200


def register_error_handlers(app):
    """Register global error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            "success": False,
            "error": "Not Found",
            "message": "The requested endpoint does not exist"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 errors."""
        return jsonify({
            "success": False,
            "error": "Method Not Allowed",
            "message": "The requested method is not allowed for this endpoint"
        }), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return jsonify({
            "success": False,
            "error": "Internal Server Error",
            "message": "An internal server error occurred"
        }), 500


if __name__ == '__main__':
    # Create the Flask app
    app = create_app()
    
    # Run the development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    ) 