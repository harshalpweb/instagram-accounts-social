"""Mixed video+image carousels (Group CTO, 2026-09-06). A `slides` entry is
either a bare string (legacy image path) or `{"type": "image"|"video",
"src": "..."}`. Covers: an all-image carousel is byte-for-byte unchanged
(regression), a mixed carousel sends the right Graph params per child type,
a video child is polled with the longer REEL timeout, and `is_ai_generated`
never lands on ANY carousel child -- image or video -- only the parent.
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


def _capture_with_timeouts(monkeypatch):
    """Like _capture, but also records the timeout_s each wait_until_finished
    call was given, keyed by container_id, so tests can assert a video child
    got the long REEL timeout and an image child got the tight default."""
    calls = []
    waits = {}

    def fake_post(path, token, data=None, base=None, **kw):
        calls.append((path, dict(data or {})))
        return {"id": f"c{len(calls)}"}

    def fake_wait(container_id, timeout_s=pub.POLL_TIMEOUT_S):
        waits[container_id] = timeout_s

    monkeypatch.setattr(pub, "api_post", fake_post)
    monkeypatch.setattr(pub, "wait_until_finished", fake_wait)
    monkeypatch.setattr(pub, "IG_USER_ID", "17841400000000000")
    return calls, waits


def test_all_image_carousel_unchanged(monkeypatch):
    """Regression: a flat string-array carousel (the pre-2026-09-06 shape)
    still sends exactly image_url + is_carousel_item per child, no
    media_type key on any child at all."""
    calls = _capture(monkeypatch)
    pub.publish_post({
        "id": "k", "slides": ["a.png", "b.png"], "caption": "c",
    })
    children = [d for p, d in calls if d.get("is_carousel_item") == "true"]
    assert len(children) == 2
    for child in children:
        assert "media_type" not in child
        assert "video_url" not in child
        assert child["image_url"].endswith("a.png") or child["image_url"].endswith("b.png")


def test_mixed_carousel_sends_right_params_per_child(monkeypatch):
    calls = _capture(monkeypatch)
    pub.publish_post({
        "id": "m",
        "slides": [
            {"type": "image", "src": "a.png"},
            {"type": "video", "src": "loop.mp4"},
            {"type": "image", "src": "b.png"},
        ],
        "caption": "c",
    })
    children = [d for p, d in calls if d.get("is_carousel_item") == "true"]
    assert len(children) == 3

    image_children = [d for d in children if "media_type" not in d]
    video_children = [d for d in children if d.get("media_type") == "VIDEO"]
    assert len(image_children) == 2
    assert len(video_children) == 1

    for d in image_children:
        assert "image_url" in d and "video_url" not in d

    video_child = video_children[0]
    assert video_child["video_url"].endswith("loop.mp4")
    assert "image_url" not in video_child
    assert video_child["is_carousel_item"] == "true"


def test_video_child_polled_with_reel_timeout_image_child_with_default(monkeypatch):
    calls, waits = _capture_with_timeouts(monkeypatch)
    pub.publish_post({
        "id": "m",
        "slides": [
            {"type": "image", "src": "a.png"},
            {"type": "video", "src": "loop.mp4"},
        ],
        "caption": "c",
    })
    # Children are created in order: c1 (image), c2 (video); carousel c3.
    assert waits.get("c1") == pub.POLL_TIMEOUT_S
    assert waits.get("c2") == pub.REEL_POLL_TIMEOUT_S


def test_ai_flag_never_on_video_or_image_child_only_parent(monkeypatch):
    calls = _capture(monkeypatch)
    pub.publish_post({
        "id": "m",
        "slides": [
            {"type": "image", "src": "a.png"},
            {"type": "video", "src": "loop.mp4"},
        ],
        "caption": "c",
        "ai_generated": True,
    })
    children = [d for p, d in calls if d.get("is_carousel_item") == "true"]
    parents = [d for p, d in calls if d.get("media_type") == "CAROUSEL"]
    assert len(children) == 2 and len(parents) == 1
    assert all("is_ai_generated" not in d for d in children)
    assert parents[0]["is_ai_generated"] == "true"


def test_bare_string_slide_defaults_to_image_type():
    """_slide_type_and_path itself: a bare string is always ('image', <the
    string>) -- the sole legacy shape, still the default for a dict that
    omits "type"."""
    assert pub._slide_type_and_path("a.png") == ("image", "a.png")
    assert pub._slide_type_and_path({"src": "a.png"}) == ("image", "a.png")
    assert pub._slide_type_and_path({"type": "video", "src": "v.mp4"}) == ("video", "v.mp4")
