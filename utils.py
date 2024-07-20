from django.utils.translation import activate, deactivate, get_language


class PauseLanguage:
    def __enter__(self):
        self.language = get_language()
        deactivate()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        activate(self.language)
