from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = MarkdownxField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    outlined_material_icon_name = models.CharField(max_length=200)
    
    @property 
    def formatted_markdown(self):
        return markdownify(self.text)

    def publish(self):
        self.published_date = timezone.now()
        self.save()
        
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = MarkdownxField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    
    @property 
    def formatted_markdown(self):
        return markdownify(self.text)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

class Subscription(models.Model):
    email = models.EmailField(max_length=256, unique=True)
    subscribed_date = models.DateTimeField(default=timezone.now)
    
    def create_unsubscribe_link(self):
        email, token = self.make_token().split(":", 1)
        return reverse('unsubscribe',
                       kwargs={'email': email, 'token': token,})
    
    def make_token(self):
        return TimestampSigner().sign(self.email)
    
    def check_token(self, token):
        try:
            key = '%s:%s' % (self.email, token)
            TimestampSigner().unsign(key, max_age=60 * 60 * 48) # Valid for 2 days
        except (BadSignature, SignatureExpired):
            return False
        return True
    
    def __str__(self):
        return self.email
