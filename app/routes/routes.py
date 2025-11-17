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

    @app.route("/transcript", methods=["GET"])
    def get_transcript():
        # Get the starting index for incremental fetching
        start_index = int(request.args.get('start', 0))
        # Return transcript entries from start_index onwards
        transcript = current_app.agent_controller.transcript_log[start_index:]
        return jsonify({
            "transcript": transcript,
            "total": len(current_app.agent_controller.transcript_log)
        })