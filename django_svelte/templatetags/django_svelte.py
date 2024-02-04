from django import template
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()


def get_static_file_url(filename):
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
    component = de_svelte(component_name)

    return {
        "css_bundle_url": get_static_file_url(f"{component}.css"),
    }


@register.inclusion_tag("django_svelte/display_svelte.html")
def display_svelte(component_name, component_props={"name": "world"}):
    component = de_svelte(component_name)

    return {
        "bundle_url": get_static_file_url(f"{component}.js"),
        "element_id": f"{component.lower()}-target",
        "props_name": f"{component.lower()}-props",
        "props": component_props,
    }
