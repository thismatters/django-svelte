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

Tell Django where your Svelte js/css bundles will be found (this guide assumes that you place your svelte directory beside your django project directory):

```py
STATICFILES_DIRS = [
    BASE_DIR.parent / "svelte" / "public" / "build",
]
```

## Usage

To use a Svelte component within your Django template load the `django_svelte` templatetag library and use the `display_svelte` templatetag:

```
{% load django_svelte %}

...

{% display_svelte "MySpecialComponent.svelte" %}
```

You can optionally pass some context (specifically a `dict`) to the component:

```
{% display_svelte "MySpecialComponent.svelte" component_props %}
```

## What about the Svelte!?

The Svelte side of things is dealt with in the [django-svelte-template](https://github.com/thismatters/django-svelte-template/) repo which you can use as a starting point for your Svelte projects (using `npx degit thismatters/django-svelte-template svelte`). It is configured to output js/css bundles for several different components, but you'll have to do some setup so be sure to read the README.

## Devops concerns

So, this isn't magic. For this to work you will need to have Node.js _somewhere_ in the mix. Fortunately, you won't need Node.js running in your production environment, but you will need it somewhere in your CI pipeline and probably in your dev environment. For a practical example of what this might look like for a production environment see [django-svelte-demo](https://github.com/thismatters/django-svelte-demo).

## Shoutouts

This work is inspired by the sentiments of [Owais Lone's writing](https://owais.lone.pw/blog/modern-frontends-with-django/) about the limitations of Django's frontend.

This work takes some technical direction from [a blog series on cbsofyalioglu](https://www.cbsofyalioglu.com/post/django-and-modern-js-libraries-svelte/). These references were immensely helpful in fleshing out this integration.
