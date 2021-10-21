from django.forms.models import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'group']
        help_texts = {
            'text': 'Текст вашего поста',
            'group': 'Выберите группу'
        }
        labels = {
            'text': 'Текст',
            'group': 'Группа'
        }
