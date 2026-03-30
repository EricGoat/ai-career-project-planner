from flask import Flask
from flask_cors import CORS
from routes.resume_routes import resume_bp
from routes.job_routes import job_bp
from routes.recommendation_routes import recommendation_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(resume_bp, url_prefix="/api/resume")
    app.register_blueprint(job_bp, url_prefix="/api/job")
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommend")

    @app.route("/")
    def home():
        return {"message": "AI Career Project Planner backend is running"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)