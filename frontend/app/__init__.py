# frontend/app/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap5
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 확장 프로그램 초기화
    bootstrap = Bootstrap5(app)
    
    # 블루프린트 등록
    from app.routes import main, auth, dashboard
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(dashboard.bp, url_prefix='/dashboard')
    
    # 오류 핸들러 등록
    from app.handlers import handle_404, handle_500
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
    
    return app