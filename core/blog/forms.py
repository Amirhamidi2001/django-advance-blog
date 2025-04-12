from django import forms
from blog.models import Post


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "status", "content", "image", "category", "published_at"]
