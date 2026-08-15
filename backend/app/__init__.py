import logging

from flask import Flask, jsonify
from flask_cors import CORS

from app.config import Config
from app.database.db import init_pool


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    logging.basicConfig(
        level=logging.INFO if not config_class.DEBUG else logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # CORS - configurable via CORS_ORIGINS env var
    CORS(app, resources={r"/api/*": {"origins": config_class.CORS_ORIGINS},
                          r"/health": {"origins": config_class.CORS_ORIGINS}})

    # Database connection pool
    init_pool(config_class)

    # Blueprints
    from app.routes.tasks import tasks_bp
    from app.routes.stats import stats_bp
    from app.routes.health import health_bp

    app.register_blueprint(tasks_bp)
    app.register_blueprint(stats_bp)
    app.register_blueprint(health_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({"error": "Method not allowed."}), 405

    @app.errorhandler(500)
    def server_error(_error):
        return jsonify({"error": "Internal server error."}), 500

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "Task Management API",
                "status": "running",
                "endpoints": [
                    "GET /health",
                    "GET /api/tasks",
                    "GET /api/tasks/<id>",
                    "POST /api/tasks",
                    "PUT /api/tasks/<id>",
                    "DELETE /api/tasks/<id>",
                    "GET /api/stats",
                ],
            }
        )

    return app
