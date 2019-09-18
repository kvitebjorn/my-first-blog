from django import forms
from markdownx.widgets import MarkdownxWidget

from .models import Post, Comment, Subscription

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'outlined_material_icon_name', 'text', )
        widgets = {
            'text': MarkdownxWidget(attrs={'class':'textarea'}),     
        }
        
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['autofocus']  = 'on'

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        widgets = {
            'text': MarkdownxWidget(attrs={'class':'textarea'}),     
        }
        
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        else:
            self.user = None
        super(CommentForm, self).__init__(*args, **kwargs)
        
        if self.user != None:
            self.fields['author'].widget.attrs['value']  = self.user
            self.fields['author'].widget.attrs['readonly']  = True
            self.fields['text'].widget.attrs['autofocus']  = 'on'
        else:
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