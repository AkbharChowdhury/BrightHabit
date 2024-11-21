# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit
from django import forms
from .models import ContactEmail


class ContactEmailForm(forms.ModelForm):
    class Meta:
        model = ContactEmail
        fields = ('email', 'subject', 'message')



#
#
# class ContactForm(forms.Form):
#     name = forms.CharField(required=True)
#     email = forms.EmailField(required=True)
#     subject = forms.CharField(required=True)
#     message = forms.CharField(widget=forms.Textarea)
#
#     def __init__(self, *args, **kwargs):
#         self.helper = FormHelper()
#         self.helper.add_input(Submit('submit', 'Submit'))
#         # super().form_valid(form)
#         super(ContactForm, self).__init__(*args, **kwargs)

# class ProfileForm2(forms.Form):
#     name = forms.CharField()
#     email = forms.EmailField()
#     url = forms.URLField()
