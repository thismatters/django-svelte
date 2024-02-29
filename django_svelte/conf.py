import json

from appconf import AppConf
from django.conf import settings  # noqa: F401
from django.core.exceptions import ImproperlyConfigured


class DjangoSvelteAppConf(AppConf):
    VITE_MANIFEST_PATH = None
    _VITE_MANIFEST = None
    ENTRYPOINT_PREFIX = "src/"
    VITE_ASSETSDIR = "assets/"

    def configure__vite_manifest(self, value):
        if value is not None:
            raise ImproperlyConfigured(
                "Do not set the `DJANGO_SVELTE__VITE_MANIFEST` setting, "
                "its value is generated!"
            )
        return None

    def configure_entrypoint_prefix(self, value):
        if value is None:
            value = ""
        if value and not value.endswith("/"):
            raise ImproperlyConfigured(
                "Non-blank entrypoint prefix must end with a slash '/'."
            )
        return value

    def configure_vite_assetsdir(self, value):
        if value is None:
            value = ""
        if value and not value.endswith("/"):
            raise ImproperlyConfigured(
                "Non-blank vite assetsdir must end with a slash '/'."
            )
        return value

    def configure(self):
        """Load the vite manifest into memory"""
        _path = self.configured_data["VITE_MANIFEST_PATH"]
        if _path is None:
            return self.configured_data
        if not _path.exists():
            raise ImproperlyConfigured(f"Vite manifest must exist at path! {_path}")
        with open(_path) as manifest:
            self.configured_data["_VITE_MANIFEST"] = json.load(manifest)
        return self.configured_data
