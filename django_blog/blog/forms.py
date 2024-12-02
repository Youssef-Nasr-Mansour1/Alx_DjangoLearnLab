from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write your comment here...'}),
        }

from taggit.forms import TagField

class PostForm(forms.ModelForm):
    tags = TagField()  # Add tags to the form

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


from django import forms
from taggit.forms import TagWidget
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Ensure tags are included
        widgets = {
            'tags': TagWidget(attrs={'placeholder': 'Add tags here...'}),
        }
