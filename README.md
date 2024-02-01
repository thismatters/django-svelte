# Django Svelte

Incorporate a Svelte frontend into a Django site with minimal impact to deployment strategy and authentication story.

## Scope

This package mainly consists of a templatetag which facilitates the import of the js/css bundle created by Svelte/Rollup/Node.js into your template. For this package to be useful you will also need the Svelte/Rollup/Node.js which produces the js/css bundle; consider using the accompanying project [django-svelte-template](https://github.com/thismatters/django-svelte-template/) as a starting point for your Svelte frontend. It has been modified to work easily alongside this package. If you run into any problems see the [django-svelte-demo](https://github.com/thismatters/django-svelte-demo) for an example of these two projects working together.

## Installation

Install the package:

```sh
pip install django-svelte
```

Add to INSTALLED_APPS:

```py
INSTALLED_APPS = (
    ...
    "django_svelte",
    ...
)
```

Tell Django where your Svelte JS/CSS bundles will be found (this guide assumes that you place your svelte directory beside your django project directory as shown in `demo_project`):

```py
STATICFILES_DIRS = [
    BASE_DIR.parent / "svelte" / "public" / "build",
]
```

## Usage

To use a Svelte component within your Django template load the `django_svelte` templatetag library and use the `display_svelte` and `display_svelte_css` templatetag:

```
{% load django_svelte %}

...

{% display_svelte_css "MySpecialComponent" %}

{% display_svelte "MySpecialComponent" %}
```

You can optionally pass some context (specifically a JSON serializable `dict`) to the component:

```
{% display_svelte "MySpecialComponent" component_props %}
```

Versions before 0.1.8 required using `.svelte` at the end of the component name, e.g.

```
{% display_svelte "MySpecialComponent.svelte" component_props %}
```

This is no longer required.

## Lets talk about CSS

There are many ways that Svelte generates CSS bundles.
Because of the flexibility of CSS many arrangements are possible, but they'll require you to update your Django templates accordingly.
Django templates are highly variable per project, so it is difficult to provide one-sized-fits-all advice in this arena.
It is likely that one or both of the use cases described below will work for your project.

If your project follows the standard `base.html -> site_base.html -> <page>.html` paradigm then you might find it convenient to also provide a `svelte_base.html` which includes a block (namely `svelte_styles`) in the `head` which will allow individual page templates to inject CSS where it ought to exist.

### Monolithic CSS

If your project collects all its CSS into a single stylesheet, then you can make that CSS file accessible as a staticfile and use a regular `link` to incorporate it into your template as shown below. It may be convenient to put this import for your stylesheet in your base template to limit boilerplate.

```
{% load static %}
{% load django_svelte %}

<html>
  <head>
    ...
    {% block svelte_styles %}
      {{ block.super }}
      <link href={% static "AllCssGeneratedByRollupOrViteOrWhatever.css" %}
    {% endblock %}
  <body>
    ...
    {% display_svelte "Component" %}
  </body>
</html>
```

### Per Component CSS

If you include `style` tags in your individual Svelte components then you'll want to include the per component stylesheets when you display your component:

```
{% extends "svelte_base.html" %}
{% load django_svelte %}

{% block svelte_styles %}
  {{ block.super }}
  {% display_svelte_css "Component" %}
{% endblock %}


{% block main_content %}
  {# or whatever... #}
  {% display_svelte "Component" %}
{% endblock %}
```

Note the use of `display_svelte_css` to specifically inject the CSS for the named component within the `svelte_styles` block.

## Recommended Patterns

In addition to the `svelte_base.html` template described above, there are some other tips that have proved effective when using this package. Basic implementations of the ideas described below are included with the demo project, but due to the extreme variability of django templates in practice you'll have to provide your own implementations.

### Class-based Wrapper View

If you have many components that each get loaded as the main content of their own pages then a reusable class-based view can reduce boilerplate. Subclass the `DjangoSvelteBaseView` class provided in `views.py` to utilize this pattern; be sure to provide your own `get_svelte_props` method so that your component will have data!

### Default Svelte Template

Once you have `svelte_base.html` in place, a subsequent template like `svelte_component.html` is a convenient template for loading in a single component. If you're using the class based view approach describe above then this template should include a `{{ page_title }}` as well as the use of `{% display_svelte_css component_name %}` in the `head` of the template, and `{% display_svelte component_name %}` in its body. See the sample implementation in the demo project.

## Use with `django-compressor`

The setting `DJANGO_SVELTE_OFFLINE_COMPRESOR` will be of service if you're using `django-compressor` (in offline mode). Setting to `True` will cause `django-svelte` to look in the `django-compessor` manifest for the appropriate file URL rather than the default staticfiles.

## What about the Svelte!?

The Svelte side of things is dealt with in the [django-svelte-template](https://github.com/thismatters/django-svelte-template/) repo which you can use as a starting point for your Svelte projects (using `npx degit thismatters/django-svelte-template svelte`). It is configured to output js/css bundles for several different components, but you'll have to do some setup so be sure to read the README.

## Devops concerns

So, this isn't magic. For this to work you will need to have Node.js _somewhere_ in the mix. Fortunately, you won't need Node.js running in your production environment, but you will need it somewhere in your CI pipeline and probably in your dev environment. For a practical example of what this might look like for a production environment see [django-svelte-demo](https://github.com/thismatters/django-svelte-demo).

## Shoutouts

This work is inspired by the sentiments of [Owais Lone's writing](https://owais.lone.pw/blog/modern-frontends-with-django/) about the limitations of Django's frontend.

This work takes some technical direction from [a blog series on cbsofyalioglu](https://www.cbsofyalioglu.com/post/django-and-modern-js-libraries-svelte/). These references were immensely helpful in fleshing out this integration.
