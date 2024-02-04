TEST_PATH = ""

migrations:
	cd demo_project/django_svelte_demo && python manage.py makemigrations
init:
	cd demo_project/django_svelte_demo && python manage.py migrate
run:
	cd demo_project/django_svelte_demo && python manage.py runserver 0.0.0.0:8000
lint:
	black django_svelte
	isort django_svelte
	cd django_svelte && pflake8
test:
	DJANGO_SETTINGS_MODULE=django_svelte_demo.settings pytest --cov=django_svelte --cov-report term-missing tests/$(TEST_PATH)
