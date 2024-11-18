class Autofocus:
    def __init__(self, fields):
        self.fields = fields

    def change_focus(self, old, new):
        self.fields[old].widget.attrs.update({'autofocus': ''})
        self.fields[new].widget.attrs.update({'autofocus': 'autofocus'})