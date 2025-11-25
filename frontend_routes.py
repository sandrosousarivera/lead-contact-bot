import json

def inject_frontend_routes(app):
    """Inject frontend routes into Flask app to serve React build"""
    from flask import send_from_directory
    from pathlib import Path
    
    static_dir = Path(__file__).parent / 'static'
    
    @app.route('/')
    @app.route('/<path:path>')
    def serve_react(path='index.html'):
        """Serve React build files"""
        file_path = static_dir / path
        
        # If file exists, serve it
        if file_path.exists() and file_path.is_file():
            return send_from_directory(static_dir, path)
        
        # Otherwise serve index.html for SPA routing
        return send_from_directory(static_dir, 'index.html')
