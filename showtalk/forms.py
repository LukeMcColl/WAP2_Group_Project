from django import forms

from showtalk.models import user, tv

FORM_FIELD_STYLES = {"class": "form-control"}


class UserForm(forms.ModelForm):
    class Meta:
        model = user
        fields = (
            "username",
            "name",
            "password",
            "email",
            "bio",
            "favourite_shows",
            "img",
        )
        widgets = {
            "username": forms.TextInput(attrs=FORM_FIELD_STYLES),
            "name": forms.TextInput(attrs=FORM_FIELD_STYLES),
            "password": forms.PasswordInput(attrs=FORM_FIELD_STYLES),
            "email": forms.EmailInput(attrs=FORM_FIELD_STYLES),
            "bio": forms.TextInput(attrs=FORM_FIELD_STYLES),
            "favourite_shows": forms.TextInput(attrs=FORM_FIELD_STYLES),
            "img": forms.FileInput(attrs=FORM_FIELD_STYLES),
        }


class TVForm(forms.ModelForm):
    class Meta:
        model = tv
        fields = ("title", "docs", "tv")
        widgets = {
            "title": forms.TextInput(attrs=FORM_FIELD_STYLES),
            "docs": forms.TextInput(attrs=FORM_FIELD_STYLES),
            "tv": forms.FileInput(attrs=FORM_FIELD_STYLES),
        }
