from django.apps import AppConfig


class LoganalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'loganalyzer'

    def ready(self) -> None:
        from . import util_funcs_log
        util_funcs_log.scan_file()
