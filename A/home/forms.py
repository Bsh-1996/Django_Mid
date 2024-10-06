from django import forms
from . models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)



class CommentCreatreForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.TextInput(attrs= {'class': 'form-control'})
        }
        