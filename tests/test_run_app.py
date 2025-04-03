# tests/test_run_app.py

def test_run_app_starts(monkeypatch):
    import app.app as main_app
    called = {}

    def fake_run(*args, **kwargs):
        called["ok"] = True

    monkeypatch.setattr(main_app.socketio, "run", fake_run)
    main_app.run_app()

    assert called.get("ok") is True

