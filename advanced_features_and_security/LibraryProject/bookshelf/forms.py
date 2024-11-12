from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=True)

# bookshelf/forms.py
from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
