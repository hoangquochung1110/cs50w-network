from django import forms

from network.models import Post


class PostCreateForm(forms.ModelForm):
    """Form to update post content."""

    content = forms.CharField(widget=forms.Textarea(attrs={"rows": "3"}))

    class Meta:
        model = Post
        fields = ("content",)
