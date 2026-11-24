
import secrets

from flask import Flask, render_template, request, redirect, url_for, session

from dataman.logic import check_answer
from dataman.store import JsonFileStore


QUESTION = "Which part of an application handles product rules?"
CORRECT_ANSWER = "business logic"


def create_app(store=None):
    app = Flask(__name__)
    app.secret_key = "dataman-development-key"

    if store is None:
        store = JsonFileStore()

    def get_player_id():
        if "player_id" not in session:
            session["player_id"] = secrets.token_hex(16)

        return session["player_id"]

    @app.route("/", methods=["GET"])
    def home():
        player_id = get_player_id()
        progress = store.load(player_id)

        return render_template(
            "index.html",
            question=QUESTION,
            progress=progress
        )

    @app.route("/answer", methods=["POST"])
    def answer():
        player_id = get_player_id()
        progress = store.load(player_id)

        if progress["completed"]:
            return redirect(url_for("home"))

        submitted_answer = request.form.get("answer", "").strip()

        if not submitted_answer:
            return redirect(url_for("home"))

        result = check_answer(
            CORRECT_ANSWER,
            submitted_answer,
            progress["attempts_used"]
        )

        progress["attempts_used"] = result["attempts_used"]
        progress["status"] = result["status"]
        progress["completed"] = result["status"] in (
            "correct",
            "revealed"
        )
        progress["message"] = result["message"]

        store.save(player_id, progress)

        return redirect(url_for("home"))

    @app.route("/reset", methods=["POST"])
    def reset():
        player_id = get_player_id()
        store.reset(player_id)

        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)
