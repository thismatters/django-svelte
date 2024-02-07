# Django Svelte

[![PyPI](https://img.shields.io/pypi/v/django-svelte?color=156741&logo=python&logoColor=ffffff&style=for-the-badge)](https://pypi.org/project/django-svelte/)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/thismatters/django-svelte/test.yml?branch=main&color=156741&label=CI&logo=github&style=for-the-badge)](https://github.com/thismatters/django-svelte/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-svelte?color=156741&logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/django-svelte/)
[![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-svelte?color=156741&logo=django&logoColor=ffffff&style=for-the-badge)](https://pypi.org/project/django-svelte/)
[![Codecov](https://img.shields.io/codecov/c/github/thismatters/django-svelte?color=156741&logo=codecov&logoColor=ffffff&style=for-the-badge)](https://codecov.io/gh/thismatters/django-svelte)


Incorporate a Svelte frontend into a Django site with minimal impact to deployment strategy and authentication story.

## Scope

This package mainly consists of a templatetags which facilitate the import of JS/CSS bundles created by Svelte/Vite/Node.js into your template. For this package to be useful you will also need the Svelte/Vite/Node.js which produces the JS/CSS bundle. The [svelte demo project](demo_project/svelte/) walks you through setting this up from scratch.

## Compatibility

This package was originally written during the Svelte 3 days and was bundled by Rollup. Version 0.1.7 and prior were devoted to supporting this stack. Newer versions of this package _ought_ to support that old stack, but they are untested.

Version 0.2.0 and on support Svelte 4 bundled by Vite.

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
    # ...
    BASE_DIR.parent / "svelte" / "dist" / "assets",
]
```

If you are using Vite as the bundler for Svelte then you'll also want to tell Django where to find the Vite manifest so that components can be located by hash (Vite does not generate a manifest by default, see the [`build.manifest` option](https://vitejs.dev/config/build-options.html#build-manifest)):

```py
DJANGO_SVELTE_VITE_MANIFEST_PATH = BASE_DIR.parent / "svelte" / "dist" / ".vite" / "manifest.json" ,
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

Versions prior to 0.2.0 required using `.svelte` at the end of the component name, e.g.

```
{% display_svelte "MySpecialComponent.svelte" component_props %}
```

This is no longer required.

## Lets talk about CSS

There are many ways that Svelte generates CSS bundles.
Because of the flexibility of CSS many arrangements are possible, but they'll require you to update your Django templates accordingly.
Django templates are highly variable per project, so it is difficult to provide one-sized-fits-all advice in this arena.
It is likely that one or both of the use cases described below will work for your project.

If your project follows the standard `base.html -> site_base.html -> <page>.html` paradigm then you might find it convenient to also provide a `svelte_base.html` which includes a block (namely `svelte_styles`) in the `head` which will allow individual page templates to inject CSS where it ought to exist:

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

See also the Vite [build option `cssCodeSplit`](https://vitejs.dev/config/build-options.html#build-csscodesplit)

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

If you have many components that each get loaded as the main content of their own pages then a reusable class-based view can reduce boilerplate. Subclass the `SvelteTemplateView` class provided in `views.py` to utilize this pattern; be sure to provide your own `get_svelte_props` method so that your component will have data! See the [sample implementation](demo_project/django_svelte_demo/django_svelte_demo/views.py)

### Default Svelte Template

Once you have `svelte_base.html` in place, a subsequent template like `svelte_component.html` is a convenient template for loading in a single component. If you're using the class based view approach describe above then this template should include a `{{ page_title }}` as well as the use of `{% display_svelte_css component_name %}` in the `head` of the template, and `{% display_svelte component_name %}` in its body. See the [sample implementation](demo_project/django_svelte_demo/django_svelte_demo/templates/svelte_component.html) in the demo project.

## What about Svelte!?

The Svelte side of things is demonstrated in the [Svelte demo project](demo_project/svelte/) which shows how a default Vite+Svelte project can be altered to output JS/CSS bundles useful for this package. It is configured to output JS/CSS bundles for several different components which can be imported independently.

### New Svelte, who dis?

The newer versions of Svelte are defaulting to SvelteKit, because routing is important stuff. If you're here then you're probably using Django for your routing, so there is no need for SvelteKit. Fortunately, Svelte (sans-Kit) is still available [by installing `vite`](https://svelte.dev/docs/introduction#start-a-new-project-alternatives-to-sveltekit).

The config for outputting multiple bundles got a bit easier from prior versions, and I changed the conventions around entrypoints in the demo project. What used to be called `main-<component_name>.js` is now called `<ComponentName>.js` and referenced as such in the `build.rollupOptions.input` array.

Vite, by default and with much difficulty to alter, hashes files and appends the hash to the filename; probably a good practice, but kind of annoying for integrated packages. Instruct Vite to output a manifest by setting the [`build.manifest` option](https://vitejs.dev/config/build-options.html#build-manifest). The complementary setting `DJANGO_SVELTE_VITE_MANIFEST_PATH` allows you to specify where in the file tree the manifest file lives. After setting this you may go about using the component name (sans hash) in the various templatetags. Alternately, it is possible to prevent Vite from putting hashes into its output filenames but you're on your own for that!

**NOTE:** This manifest arrangement _will_ get bothersome during dev as you have to cause Django to reload the manifest by saving a Django file each time you save a Svelte file (and the bundle hash changes). If **anybody** knows a way to make this more manageable, please please tell me!

Depending on how you have organized your Svelte project you may have specify where your Svelte component "Entrypoints" are located (Entrypoints are the thin javascript files that first import the Svelte component, see [App.js](demo_project/svelte/src/App.js). In the demo project, the entrypoints are directly in the `svelte/src/` directory. If you have put your entrypoints somewhere else then you'll need to say where in the `DJANGO_SVELTE_ENTRYPOIN_PREFIX` setting (value needs to be relative to the `svelte` directory and do include the trailing slash, e.g. the default value `src/`). It is necessary that your entrypoints follow the naming convention `<ComponentName>.js`; if your top-level Svelte component is called `MySpecialComponent.svelte` then the entrypoint needs to be called `MySpecialComponent.js` or this package will not function correctly!

It may be necessary to specify the `DJANGO_SVELTE_VITE_ASSETSDIR` setting. It must match the value used in `vite.config.js` under the key `build.assetsDir`. The default case (value `assets/` ) is covered.

## Devops concerns

So, this package isn't magic. For this to work you will need to have Node.js _somewhere_ in the mix. Fortunately, you won't need Node.js running in your production environment, but you will need it somewhere in your CI pipeline and probably in your dev environment. For a practical example of what this might look like for a production environment see [demo_project](demo_project).

## Shoutouts

This work is inspired by the sentiments of [Owais Lone's writing](https://owais.lone.pw/blog/modern-frontends-with-django/) about the limitations of Django's frontend.

This work takes some technical direction from [a blog series on cbsofyalioglu](https://www.cbsofyalioglu.com/post/django-and-modern-js-libraries-svelte/). These references were immensely helpful in fleshing out this integration.
