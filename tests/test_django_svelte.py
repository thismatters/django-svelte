from django_svelte.templatetags.django_svelte import (
    get_static_file_url,
    de_svelte,
    display_svelte_css,
    display_svelte,
)


def test_get_static_file_url_none():
    assert get_static_file_url("not-a_file.asdf") is None


def test_get_static_file_url_real():
    assert get_static_file_url("real_file.txt") == "/static/real_file.txt"


def test_de_svelte():
    assert de_svelte("something.svelte") == "something"


def test_de_svelte_no_change():
    assert de_svelte("something.smelte") == "something.smelte"


def test_display_svelte_css():
    assert display_svelte_css("Something.svelte") == {
        "css_bundle_url": "/static/Something.css"
    }


def test_display_svelte():
    assert display_svelte("Something.svelte", component_props={"great": "stuff"}) == {
        "bundle_url": "/static/Something.js",
        "element_id": "something-target",
        "props_name": "something-props",
        "props": {"great": "stuff"},
    }
