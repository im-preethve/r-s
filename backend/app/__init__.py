from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    app = Flask(__name__)
    
    # Set template folder
    app.template_folder = os.path.join(project_root, 'html')
    
    print("Template folder is:", app.template_folder)
    print("Project root is:", project_root)
    
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    
    # Custom static file handling
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(os.path.join(project_root, 'css'), filename)

    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(os.path.join(project_root, 'js'), filename)

    @app.route('/images/<path:filename>')
    def serve_images(filename):
        return send_from_directory(os.path.join(project_root, 'images'), filename)
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app