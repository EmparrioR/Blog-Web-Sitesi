from django import forms
from .models import Post, Comment, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.widgets import CKEditorWidget

class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        
        # Alt kategorilere sahip olan kategorileri buluyor ve bunları parent_category kabul ediyoruz
        self.fields['category'].queryset = Category.objects.filter(parent_category__isnull=False)
    class Meta:
        model = Post
        fields = ('title', 'content','category')


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))
    parent_comment_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': CKEditorWidget(),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text'] 
        widgets = {
            'text': CKEditorWidget(),  
        }       

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password'] 



class PostCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostCreateForm, self).__init__(*args, **kwargs)
        
        # Alt kategorilere sahip olan kategorileri buluyor ve bunları parent_category kabul ediyoruz
        self.fields['category'].queryset = Category.objects.filter(parent_category__isnull=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

class CategoryForm(forms.ModelForm):
    parent_category = forms.ModelChoiceField(queryset=Category.objects.filter(parent_category=None), required=False)
    class Meta:
        model = Category
        fields = ['name','parent_category']      