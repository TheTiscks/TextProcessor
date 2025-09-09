# tests/test_api.py
from app import create_app


def test_create_and_consume():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client, app.app_context():
        # create
        res = client.post("/create", json={"encrypted_msg": "abc", "lifetime": "hour"})
        assert res.status_code == 200
        data = res.get_json()
        assert "url" in data

        # token from url
        token = data["url"].rsplit("/", 1)[-1]
        # view
        view_res = client.get(f"/m/{token}")
        assert view_res.status_code == 200
        # consume endpoint
        consume_res = client.get(f"/consume/{token}")
        assert consume_res.status_code == 200
