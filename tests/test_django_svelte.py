from django.test import override_settings

from django_svelte.templatetags.django_svelte import (
    clean_hashed_filename,
    get_bundle_hashed_filename,
    _get_css_bundle_hashed_filenames,
    get_css_bundle_hashed_filenames,
    get_css_bundle_urls,
    get_bundle_url,
    de_svelte,
    display_svelte_css,
    display_svelte,
)


class TestGetStaticFileUrl:
    def test_none(self):
        assert get_bundle_url(component_name="not-a_file") is None

    def test_real(self):
        assert get_bundle_url(component_name="real_file") == "/static/real_file.js"

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/Hashed.js": {"isEntry": True, "file": "assets/Hashed-asdfsafd.js"}
        }
    )
    def test_hashed(self):
        assert get_bundle_url(component_name="Hashed") == "/static/Hashed-asdfsafd.js"

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/Bashed.js": {"isEntry": True, "file": "assets/Bashed-asdfsafd.js"}
        }
    )
    def test_hashed_missing(self):
        assert get_bundle_url(component_name="Bashed") is None

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/Bashed.js": {"isEntry": True, "file": "assets/Bashed-asdfsafd.js"}
        }
    )
    def test_hashed_absent(self):
        assert get_bundle_url(component_name="Hashed") is None


def test_de_svelte():
    assert de_svelte("something.svelte") == "something"


def test_de_svelte_no_change():
    assert de_svelte("something.smelte") == "something.smelte"


def test_display_svelte_css():
    assert display_svelte_css("Something.svelte") == {
        "css_bundle_urls": ["/static/Something.css"]
    }


def test_display_svelte_css_missing():
    assert display_svelte_css("Plain.svelte") == {"css_bundle_urls": []}


def test_display_svelte():
    assert display_svelte("Something.svelte", component_props={"great": "stuff"}) == {
        "bundle_url": "/static/Something.js",
        "element_id": "something-target",
        "props_name": "something-props",
        "props": {"great": "stuff"},
    }


class TestGetHashedFilename:
    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/App.js": {"isEntry": True, "file": "assets/App-asdfsafd.js"}
        }
    )
    def test_good(self):
        assert get_bundle_hashed_filename(component_name="App") == "App-asdfsafd.js"

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "a.js": {"imports": ["b.js", "c.js"], "css": ["assets/a.css"]},
            "src/App.js": {
                "isEntry": True,
                "css": ["assets/App-asdfsafd.css"],
                "imports": ["a.js", "b.js"],
            },
            "b.js": {"imports": ["c.js"], "css": ["assets/b.css"]},
            "c.js": {},
        }
    )
    def test_css(self):
        css = _get_css_bundle_hashed_filenames(key="src/App.js")
        print(css)
        assert "assets/App-asdfsafd.css" in css
        assert "assets/a.css" in css
        assert "assets/b.css" in css
        # this list is not deduped!
        assert len(css) == 4

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "a.js": {"imports": ["b.js", "c.js"], "css": ["assets/a.css"]},
            "src/App.js": {
                "isEntry": True,
                "css": ["assets/App-asdfsafd.css"],
                "imports": ["a.js", "b.js"],
            },
            "b.js": {"imports": ["c.js"], "css": ["assets/b.css"]},
            "c.js": {},
        }
    )
    def test_get_css_bundle_hashed_filenames(self):
        css = get_css_bundle_hashed_filenames(component_name="App")
        print(css)
        assert "App-asdfsafd.css" in css
        assert "a.css" in css
        assert "b.css" in css
        assert len(css) == 3

    @override_settings(DJANGO_SVELTE__VITE_MANIFEST={"src/App.js": {"isEntry": True}})
    def test_css_none(self):
        assert get_css_bundle_urls(component_name="App") == []

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/App.js": {"isEntry": True, "file": "assets/App-asdfsafd.js"}
        }
    )
    def test_nonexistent(self):
        assert get_bundle_hashed_filename(component_name="Abb") is None

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={"src/App.js": {"file": "assets/App-asdfsafd.js"}}
    )
    def test_nonentry(self):
        assert get_bundle_hashed_filename(component_name="App") is None

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/App.js": {"file": "bassets/App-asdfsafd.js"}
        },
        DJANGO_SVELTE_VITE_ASSETSDIR="bassets/",
    )
    def test_different_assetsdir(self):
        assert get_bundle_hashed_filename(component_name="App") is None

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/entrypoints/App.js": {"file": "assets/App-asdfsafd.js"}
        },
        DJANGO_SVELTE_ENTRYPOINT_PREFIX="src/entrypoints/",
    )
    def test_different_prefix(self):
        assert get_bundle_hashed_filename(component_name="App") is None
