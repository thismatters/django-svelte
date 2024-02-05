from django_svelte.views import SvelteTemplateView


class MySvelteTemplateView(SvelteTemplateView):
    template_name = "svelte_component.html"

    def get_svelte_props(self, **kwargs):
        return kwargs


class MyContextSvelteTemplateView(MySvelteTemplateView):
    def get_svelte_props(self, **kwargs):
        kwargs.update({"name": "single component view"})
        return kwargs
