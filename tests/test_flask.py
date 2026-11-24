
from app import create_app
from dataman.store import JsonFileStore


def create_test_app(tmp_path):
    store = JsonFileStore(tmp_path / "test_progress.json")
    app = create_app(store)
    app.config["TESTING"] = True
    return app


def test_first_wrong_answer_allows_retry(tmp_path):
    app = create_test_app(tmp_path)
    client = app.test_client()

    response = client.post(
        "/answer",
        data={"answer": "interface"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"one attempt remaining" in response.data
    assert b"business logic" not in response.data


def test_second_wrong_answer_reveals_answer(tmp_path):
    app = create_test_app(tmp_path)
    client = app.test_client()

    client.post("/answer", data={"answer": "interface"})

    response = client.post(
        "/answer",
        data={"answer": "database"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"business logic" in response.data
    assert b"Question completed!" in response.data


def test_correct_answer_completes_question(tmp_path):
    app = create_test_app(tmp_path)
    client = app.test_client()

    response = client.post(
        "/answer",
        data={"answer": "business logic"},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Correct!" in response.data
    assert b"Question completed!" in response.data


def test_progress_survives_another_request(tmp_path):
    app = create_test_app(tmp_path)
    client = app.test_client()

    client.post("/answer", data={"answer": "wrong"})

    response = client.get("/")

    assert b"Attempts used: 1 / 2" in response.data
    assert b"one attempt remaining" in response.data
