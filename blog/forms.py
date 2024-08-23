from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(
        label="",
        max_length=64,
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"}),
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email"},
        ),
    )
    to = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter the reveiver email"},
        ),
    )
    comments = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Enter the comment"}),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter your name"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Enter your email"},
            ),
        }
        labels = {
            "name": "",
            "email": "",
            "body": "",
        }
        help_texts = {
            "name": "",
            "email": "",
            "body": "",
        }
        error_messages = {
            "name": "",
            "email": "",
            "body": "",
        }
        field_classes = {
            "name": forms.CharField,
            "email": forms.EmailField,
            "body": forms.CharField,
        }


class SearchForm(forms.Form):
    query = forms.CharField()
