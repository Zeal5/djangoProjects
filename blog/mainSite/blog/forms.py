from django import forms
from blog.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
