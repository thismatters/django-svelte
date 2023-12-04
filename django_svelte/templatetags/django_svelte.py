from os import path
from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()


@register.inclusion_tag("django_svelte/display_svelte.html")
def display_svelte(component, component_props={"name": "world"}):
    if component.endswith(".svelte"):
        component = component[:-7]

    context = {
        "bundle_url": staticfiles_storage.url(f"{component}.js"),
        "css_bundle_url": staticfiles_storage.url(f"{component}.css"),
        "element_id": f"{component.lower()}-target",
        "props_name": f"{component.lower()}-props",
        "app_name": component,
        "props": component_props,
    }

    if not path.exists(context["css_bundle_url"]):
        context.pop("css_bundle_url")

    return context
