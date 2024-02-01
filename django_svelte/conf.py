from appconf import AppConf
from django.conf import settings  # noqa: F401


class DjangoSvelteAppConf(AppConf):
    USE_COMPRESSOR_OFFLINE = False
