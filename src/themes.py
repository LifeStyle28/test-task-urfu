from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class Theme:
    name: str = ""
    description: str = ""

    def __init__(self, name, desc):
        self.name = name
        self.description = desc

    @property
    def get_description(self) -> str:
        return self.description

    @property
    def get_name(self) -> str:
        return self.name


themes_map = {
    1: Theme("first theme", "first theme desc"),
    2: Theme("second theme", "second theme desc"),
    3: Theme("third theme", "third theme desc"),
}


class ThemeValidationError(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors


def validate_theme(theme_id):
    if themes_map.get(theme_id) is None:
        raise ThemeValidationError(f"Theme with {theme_id} is not supported")
