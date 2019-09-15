from django import forms

from .models import Post, Comment, Subscription

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'outlined_material_icon_name')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class SubscriptionForm(forms.ModelForm):
    
    class Meta:
        model = Subscription
        fields = ('email',)