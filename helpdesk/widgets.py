from django.forms import Select


# Виджет чтобы сделать недоступным для выбора некоторые пункты Select
class SelectWidget(Select):
    """
    Subclass of Django's select widget that allows disabling options.
    """
    def __init__(self, *args, **kwargs):
        self._disabled_choices = []
        super().__init__(*args, **kwargs)

    @property
    def disabled_choices(self):
        return self._disabled_choices

    @disabled_choices.setter
    def disabled_choices(self, other):
        self._disabled_choices = other

    def create_option(self, name, value, *args, **kwargs):
        option_dict = super().create_option(name, value, *args, **kwargs)
        if value in self.disabled_choices:
            option_dict['attrs']['disabled'] = 'disabled'
            option_dict['attrs']['style'] = 'background: rgba(200, 200, 200, 0.3);'
        return option_dict