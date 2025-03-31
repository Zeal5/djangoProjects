from django import forms
from blog.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class":"p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Your Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Your Email",
                }
            ),
            "body": forms.Textarea(
                attrs={
                    "class": "w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    "placeholder": "Write your comment...",
                    "rows": 5,
                }
            ),
        }


class SearchForm(forms.Form):
    query = forms.CharField()
