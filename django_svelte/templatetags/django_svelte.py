from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings

register = template.Library()

@register.inclusion_tag("display_svelte.html")
def display_svelte(component, component_props={"name": "world"}):
    if not component.endswith(".svelte"):
        raise ValueError("component name should end with '.svelte'")

    app_name = component[:-7]

    rollup_setting = getattr(settings, "DJANGO_SVELTE_ROLLUP_CSS", None)

    if rollup_setting is not None:
        
        # Guard against misconfigured settings files
        rollup_setting = "/static" + rollup_setting.replace("/static", "")

        context = {
            "bundle_url": staticfiles_storage.url(f"{app_name}.js"),
            "css_bundle_url": staticfiles_storage.url(f"{app_name}.css"),
            "css_bundle_url_ext": rollup_setting,
            "element_id": f"{app_name.lower()}-target",
            "props_name": f"{app_name.lower()}-props",
            "app_name": app_name,
            "props": component_props,
        }
    else:
        context = {
            "bundle_url": staticfiles_storage.url(f"{app_name}.js"),
            "css_bundle_url": staticfiles_storage.url(f"{app_name}.css"),
            "element_id": f"{app_name.lower()}-target",
            "props_name": f"{app_name.lower()}-props",
            "app_name": app_name,
            "props": component_props,
        }
    return context
