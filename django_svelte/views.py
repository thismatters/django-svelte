from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin


class SvelteContextMixin(ContextMixin):
    component_name = None
    page_title = "Svelte Component"

    def get_svelte_props(self, **kwargs):
        raise NotImplementedError(
            "Define `get_svelte_props` in BaseSvelteComponentView subclass."
        )

    def get_context_data(self, *, svelte_props=None, **kwargs):
        context = super().get_context_data(**kwargs)
        _svelte_props = svelte_props or {}
        context.update(
            {
                "page_title": self.page_title,
                "component_name": self.component_name,
                "component_props": self.get_svelte_props(**_svelte_props),
            }
        )
        return context


class SvelteTemplateView(SvelteContextMixin, TemplateView):
    """Display Svelte component. (Provide your own conformant template)"""

    pass
