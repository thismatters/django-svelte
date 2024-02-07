from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()


def get_hashed_filename(*, component_name, file_type):
    key = f"{settings.DJANGO_SVELTE_ENTRYPOINT_PREFIX}{component_name}.js"
    entry = settings.DJANGO_SVELTE__VITE_MANIFEST.get(key)
    if entry is None:
        return None
    if not entry.get("isEntry", False):
        return None
    if file_type == "js":
        filename = entry["file"]
    if file_type == "css":
        _css = entry.get("css", [])
        if not _css:
            return None
        filename = _css[0]
    # strip the vite build.assetsDir from the filename
    if filename.startswith(settings.DJANGO_SVELTE_VITE_ASSETSDIR):
        _len = len(settings.DJANGO_SVELTE_VITE_ASSETSDIR)
        filename = filename[_len:]
    return filename


def get_static_file_url(*, component_name, file_type="js"):
    filename = None
    if settings.DJANGO_SVELTE__VITE_MANIFEST is not None:
        filename = get_hashed_filename(
            component_name=component_name, file_type=file_type
        )
    else:
        filename = f"{component_name}.{file_type}"
    if filename is None:
        return None
    static_file = finders.find(filename)
    if static_file is None:
        return None
    return staticfiles_storage.url(filename)


def de_svelte(name):
    """Removes the .svelte suffix from a name, if present"""
    if name.endswith(".svelte"):
        return name[:-7]
    return name


@register.inclusion_tag("django_svelte/display_svelte_css.html")
def display_svelte_css(component_name):
    component_name = de_svelte(component_name)

    return {
        "css_bundle_url": get_static_file_url(
            component_name=component_name, file_type="css"
        ),
    }


@register.inclusion_tag("django_svelte/display_svelte.html")
def display_svelte(component_name, component_props=None):
    component_name = de_svelte(component_name)
    component_props = component_props or {}

    return {
        "bundle_url": get_static_file_url(
            component_name=component_name, file_type="js"
        ),
        "element_id": f"{component_name.lower()}-target",
        "props_name": f"{component_name.lower()}-props",
        "props": component_props,
    }
