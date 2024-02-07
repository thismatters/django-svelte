# `django-svelte` Demo Project

This project aims to demonstrate the functionality of the `django-svelte` package. It is intended to illustrate how Node.js can fit into the development and build environments so that it doesn't have to be used in a production environment.

Pay special attention to the `Dockerfile`, `docker-compose.yml`, and `gitlab-ci.yml` (I'm using Gitlab CI here because it is really great and it is what I use for all my professional projects; if there is enough interest I'll try to replicate the functionality in Github CI).

## Disclaimer

This demo probably will run fine, but you're on your own getting it to run.

## Django Project

What you'll find is a relatively vanilla Django project, created in the standard `django start-project` way. To it is added Django Rest Framework and this package, `django-svelte`, some templates and views along with the necessary serializers and api views.

## Svelte Project

What you'll find is a relatively vanilla Vite+Svelte project, with only a few lines added to the Vite config file. See the [readme within the `svelte` project](svelte/README.md).
