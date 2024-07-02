from crispy_forms.helper import FormHelper
from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'desc', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
