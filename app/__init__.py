from flask import Flask
from flask_migrate import Migrate  
from .db import db
from .models import task, goal

import os

def create_app(config=None):
    app = Flask(__name__)

    from flask_cors import CORS
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    
    # 修复迁移初始化 - 添加以下三行
    migrate = Migrate()
    migrate.init_app(app, db)

    # 注册蓝图
    from .routes.task_routes import bp as tasks_bp
    from .routes.goal_routes import bp as goals_bp  # 改为相对导入
    app.register_blueprint(tasks_bp)
    app.register_blueprint(goals_bp)

    return app
