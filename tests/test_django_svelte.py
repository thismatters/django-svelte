from django.test import override_settings

from django_svelte.templatetags.django_svelte import (
    get_hashed_filename,
    get_static_file_url,
    de_svelte,
    display_svelte_css,
    display_svelte,
)


class TestGetStaticFileUrl:
    def test_none(self):
        assert (
            get_static_file_url(component_name="not-a_file", file_type="asdf") is None
        )

    def test_real(self):
        assert (
            get_static_file_url(component_name="real_file", file_type="txt")
            == "/static/real_file.txt"
        )

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/Hashed.js": {"isEntry": True, "file": "assets/Hashed-asdfsafd.js"}
        }
    )
    def test_hashed(self):
        assert (
            get_static_file_url(component_name="Hashed", file_type="js")
            == "/static/Hashed-asdfsafd.js"
        )

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/Bashed.js": {"isEntry": True, "file": "assets/Bashed-asdfsafd.js"}
        }
    )
    def test_hashed_missing(self):
        assert get_static_file_url(component_name="Bashed", file_type="js") is None

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/Bashed.js": {"isEntry": True, "file": "assets/Bashed-asdfsafd.js"}
        }
    )
    def test_hashed_absent(self):
        assert get_static_file_url(component_name="Hashed", file_type="js") is None


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


class TestGetHashedFilename:
    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/App.js": {"isEntry": True, "file": "assets/App-asdfsafd.js"}
        }
    )
    def test_good(self):
        assert (
            get_hashed_filename(component_name="App", file_type="js")
            == "App-asdfsafd.js"
        )

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/App.js": {"isEntry": True, "css": ["assets/App-asdfsafd.css"]}
        }
    )
    def test_css(self):
        assert (
            get_hashed_filename(component_name="App", file_type="css")
            == "App-asdfsafd.css"
        )

    @override_settings(DJANGO_SVELTE__VITE_MANIFEST={"src/App.js": {"isEntry": True}})
    def test_css_none(self):
        assert get_hashed_filename(component_name="App", file_type="css") is None

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/App.js": {"isEntry": True, "file": "assets/App-asdfsafd.js"}
        }
    )
    def test_nonexistent(self):
        assert get_hashed_filename(component_name="Abb", file_type="js") is None

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={"src/App.js": {"file": "assets/App-asdfsafd.js"}}
    )
    def test_nonentry(self):
        assert get_hashed_filename(component_name="App", file_type="js") is None

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/App.js": {"file": "bassets/App-asdfsafd.js"}
        },
        DJANGO_SVELTE_VITE_ASSETSDIR="bassets/",
    )
    def test_different_assetsdir(self):
        assert get_hashed_filename(component_name="App", file_type="js") is None

    @override_settings(
        DJANGO_SVELTE__VITE_MANIFEST={
            "src/entrypoints/App.js": {"file": "assets/App-asdfsafd.js"}
        },
        DJANGO_SVELTE_ENTRYPOINT_PREFIX="src/entrypoints/",
    )
    def test_different_prefix(self):
        assert get_hashed_filename(component_name="App", file_type="js") is None
