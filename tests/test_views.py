from unittest.mock import patch

import pytest

from django_svelte import views


def mocked_get_svelte_props(self, **kwargs):
    kwargs.update(
        {
            "new_prop": "here",
        }
    )
    return kwargs


class TestSvelteComponentMixin:
    @patch.object(views.SvelteContextMixin, "get_svelte_props", mocked_get_svelte_props)
    def test_get_context_data(self):
        mixin = views.SvelteContextMixin()
        mixin.component_name = "FakeComponent"
        mixin.page_title = "Fake Component"
        ctx = mixin.get_context_data()
        assert "page_title" in ctx
        assert ctx["page_title"] == "Fake Component"
        assert "component_name" in ctx
        assert ctx["component_name"] == "FakeComponent"
        assert "component_props" in ctx
        assert ctx["component_props"] == {"new_prop": "here"}

    def test_get_context_data_no_subclass(self):
        mixin = views.SvelteContextMixin()
        with pytest.raises(NotImplementedError):
            ctx = mixin.get_context_data()
