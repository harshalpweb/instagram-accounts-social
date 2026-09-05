"""`ai_generated: true` in a queue JSON must reach Meta as `is_ai_generated=true`
on the REELS container and on the CAROUSEL parent container only -- never on
carousel children (Meta errors on that), and never when the flag is absent.
"""
import publish_due_posts as pub


def _capture(monkeypatch):
    calls = []

    def fake_post(path, token, data=None, base=None, **kw):
        calls.append((path, dict(data or {})))
        return {"id": f"c{len(calls)}"}

    monkeypatch.setattr(pub, "api_post", fake_post)
    monkeypatch.setattr(pub, "wait_until_finished", lambda *a, **k: None)
    monkeypatch.setattr(pub, "IG_USER_ID", "17841400000000000")
    return calls


def test_reel_with_flag_sets_is_ai_generated(monkeypatch):
    calls = _capture(monkeypatch)
    pub.publish_post({"id": "r", "video": "v.mp4", "caption": "c", "ai_generated": True})
    create = [d for p, d in calls if d.get("media_type") == "REELS"]
    assert len(create) == 1
    assert create[0]["is_ai_generated"] == "true"


def test_reel_without_flag_unchanged(monkeypatch):
    calls = _capture(monkeypatch)
    pub.publish_post({"id": "r", "video": "v.mp4", "caption": "c"})
    create = [d for p, d in calls if d.get("media_type") == "REELS"]
    assert "is_ai_generated" not in create[0]


def test_carousel_flag_on_parent_only(monkeypatch):
    calls = _capture(monkeypatch)
    pub.publish_post({
        "id": "k", "slides": ["a.png", "b.png"], "caption": "c", "ai_generated": True,
    })
    children = [d for p, d in calls if d.get("is_carousel_item") == "true"]
    parents = [d for p, d in calls if d.get("media_type") == "CAROUSEL"]
    assert len(children) == 2 and len(parents) == 1
    assert all("is_ai_generated" not in d for d in children)
    assert parents[0]["is_ai_generated"] == "true"


def test_string_true_is_not_a_flag(monkeypatch):
    """Only a JSON boolean counts -- a stray "true" string must not disclose."""
    calls = _capture(monkeypatch)
    pub.publish_post({"id": "r", "video": "v.mp4", "caption": "c", "ai_generated": "true"})
    create = [d for p, d in calls if d.get("media_type") == "REELS"]
    assert "is_ai_generated" not in create[0]
