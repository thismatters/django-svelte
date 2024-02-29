from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()


def clean_hashed_filename(filename):
    # strip the vite `build.assetsDir` from the filename
    if filename.startswith(settings.DJANGO_SVELTE_VITE_ASSETSDIR):
        _len = len(settings.DJANGO_SVELTE_VITE_ASSETSDIR)
        filename = filename[_len:]
    return filename


def get_bundle_hashed_filename(*, component_name):
    key = f"{settings.DJANGO_SVELTE_ENTRYPOINT_PREFIX}{component_name}.js"
    entry = settings.DJANGO_SVELTE__VITE_MANIFEST.get(key)
    if entry is None:
        return None
    if not entry.get("isEntry", False):
        return None
    filename = entry["file"]
    filename = clean_hashed_filename(filename)
    return filename


def _get_css_bundle_hashed_filenames(*, key):
    entry = settings.DJANGO_SVELTE__VITE_MANIFEST.get(key)
    bundles = entry.get("css", [])
    for subkey in entry.get("imports", []):
        bundles.extend(_get_css_bundle_hashed_filenames(key=subkey))
    return bundles


def get_css_bundle_hashed_filenames(*, component_name):
    key = f"{settings.DJANGO_SVELTE_ENTRYPOINT_PREFIX}{component_name}.js"
    bundles = _get_css_bundle_hashed_filenames(key=key)
    return [clean_hashed_filename(b) for b in set(bundles)]


def get_css_bundle_urls(*, component_name):
    filenames = []
    if settings.DJANGO_SVELTE__VITE_MANIFEST is not None:
        filenames = get_css_bundle_hashed_filenames(component_name=component_name)
    else:
        filenames.append(f"{component_name}.css")
    cleaned_bundles = []
    for filename in filenames:
        found_file = finders.find(filename)
        if found_file is None:
            continue
        cleaned_bundles.append(staticfiles_storage.url(filename))
    return cleaned_bundles


def get_bundle_url(*, component_name):
    filename = None
    if settings.DJANGO_SVELTE__VITE_MANIFEST is not None:
        filename = get_bundle_hashed_filename(component_name=component_name)
    else:
        filename = f"{component_name}.js"
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
        "css_bundle_urls": get_css_bundle_urls(component_name=component_name),
    }


@register.inclusion_tag("django_svelte/display_svelte.html")
def display_svelte(component_name, component_props=None):
    component_name = de_svelte(component_name)
    component_props = component_props or {}

    return {
        "bundle_url": get_bundle_url(component_name=component_name),
        "element_id": f"{component_name.lower()}-target",
        "props_name": f"{component_name.lower()}-props",
        "props": component_props,
    }
