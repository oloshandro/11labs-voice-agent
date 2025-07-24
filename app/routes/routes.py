from flask import render_template, request, jsonify, current_app


def register_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/start", methods=["POST"])
    def start():
        current_app.agent_controller.start()
        return jsonify({"status": "started"})

    @app.route("/stop", methods=["POST"])
    def stop():
        current_app.agent_controller.stop()
        return jsonify({"status": "stopped"})