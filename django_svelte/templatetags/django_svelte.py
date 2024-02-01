from os import path
from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles import finders

from django.conf import settings

if settings.DJANGO_SVELTE_USE_COMPRESSOR_OFFLINE:
    from compressor.cache import cache_get, get_offline_manifest


register = template.Library()


def get_static_file_url(filename):
    if settings.DJANGO_SVELTE_USE_COMPRESSOR_OFFLINE:
        # TODO: get the file with hash from django_compressor
        pass
    else:
        static_file = finders.find(filename)
        if static_file is None:
            return None
        return staticfiles_storage.url(filename)


@register.inclusion_tag("django_svelte/display_svelte_css.html")
def display_svelte_css(component_name):
    if component_name.endswith(".svelte"):
        component_name = component_name[:-7]

    context = {
        "css_bundle_url": get_static_file_url(f"{component_name}.css"),
    }

    return context


@register.inclusion_tag("django_svelte/display_svelte.html")
def display_svelte(component, component_props={"name": "world"}):
    if component.endswith(".svelte"):
        component = component[:-7]

    return {
        "bundle_url": get_static_file_url(f"{component}.js"),
        "element_id": f"{component.lower()}-target",
        "props_name": f"{component.lower()}-props",
        "app_name": component,
        "props": component_props,
    }
