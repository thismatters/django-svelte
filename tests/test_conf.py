from pathlib import Path

import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from django_svelte.conf import DjangoSvelteAppConf


class TestDjangoSvelteAppConf:
    def test_configure__vite_manifest(self):
        assert DjangoSvelteAppConf().configure__vite_manifest(None) is None

    def test_configure__vite_manifest_bad(self):
        with pytest.raises(ImproperlyConfigured):
            DjangoSvelteAppConf().configure__vite_manifest("")

    def test_configure_entrypoint_prefix(self):
        assert DjangoSvelteAppConf().configure_entrypoint_prefix("slash/") == "slash/"

    def test_configure_entrypoint_prefix_none(self):
        assert DjangoSvelteAppConf().configure_entrypoint_prefix(None) == ""

    def test_configure_entrypoint_prefix_bad(self):
        with pytest.raises(ImproperlyConfigured):
            DjangoSvelteAppConf().configure_entrypoint_prefix("noslash")

    def test_configure_vite_assetsdir(self):
        assert DjangoSvelteAppConf().configure_vite_assetsdir("slash/") == "slash/"

    def test_configure_vite_assetsdir_none(self):
        assert DjangoSvelteAppConf().configure_vite_assetsdir(None) == ""

    def test_configure_vite_assetsdir_bad(self):
        with pytest.raises(ImproperlyConfigured):
            DjangoSvelteAppConf().configure_vite_assetsdir("noslash")

    def test_configure(self):
        conf = DjangoSvelteAppConf()
        conf._meta.configured_data = {
            "VITE_MANIFEST_PATH": Path(
                settings.BASE_DIR.parent / "static" / "fake_manifest.json"
            )
        }
        ret = conf.configure()
        assert ret["_VITE_MANIFEST"] == {"testkey": "testvalue"}

    def test_configure_no_file(self):
        conf = DjangoSvelteAppConf()
        conf._meta.configured_data = {"VITE_MANIFEST_PATH": Path("bad/path")}
        with pytest.raises(ImproperlyConfigured):
            ret = conf.configure()
