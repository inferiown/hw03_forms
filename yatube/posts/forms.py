from django.forms.models import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']


class PostEdit(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
