from django import forms

from .models import Post, Comment, Subscription

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'outlined_material_icon_name')
        
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['autofocus']  = 'on'

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['author'].widget.attrs['autofocus']  = 'on'

class SubscriptionForm(forms.ModelForm):
    
    class Meta:
        model = Subscription
        fields = ('email',)
        
    def __init__(self, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus']  = 'on'

    def clean_email(self):
        return self.cleaned_data['email'].lower()