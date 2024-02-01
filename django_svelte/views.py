from django.views.generic import TemplateView


class BaseSvelteComponentView(TemplateView):
    component_name = None
    page_title = "Svelte Component"

    def get_svelte_props(self, **kwargs):
        raise NotImplementedError(
            "Define `get_svelte_props` in BaseSvelteComponentView subclass."
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "page_title": self.page_title,
                "component_name": self.component_name,
                "component_props": self.get_svelte_props(),
            }
        )
        return context
