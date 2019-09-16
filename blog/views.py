from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.validators import validate_email
from django.core.mail import send_mass_mail

from .models import Post, Comment, Subscription
from .forms import PostForm, CommentForm, SubscriptionForm

# Create your views here.

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    posts = posts[:3]
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def archive_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/archive_list.html', {'posts': posts})

def search(request):
    search_term = ""
    if ('term' in request.GET) and request.GET['term'].strip():
        search_term = request.GET['term']
    posts = []
    if search_term != "":
        posts = Post.objects.filter(
                    Q(published_date__lte=timezone.now()) &
                    ( Q(text__contains=search_term) | 
                      Q(title__contains=search_term))).order_by('-published_date')
    return render(request, 'blog/search.html', {'posts': posts, 'term':search_term})

def subscribe(request):
    email_address = ""
    status = ""
    
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.clean_email()
            subscription = form.save(commit=False)
            email_address = subscription.email
            
            try:                
                validate_email(email_address)
                subscription.save()
            except:
                status = "invalid"
                
    else:
        form = SubscriptionForm()
        
    return render(request, 'blog/subscribe.html', {'form': form, 'email_address':email_address, 'status':status})

def unsubscribe(request, email, token):
    subscription = get_object_or_404(Subscription, email=email);
    valid_token = subscription.check_token(token)
    if valid_token:
        unsubscribed_email = email
        subscription.delete()
    else:
        unsubscribed_email = "invalid token"
    return render(request, 'blog/unsubscribe.html', {'email':unsubscribed_email})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    
    # Send a notification email to all subscribers
    recipients = [subscriber.email for subscriber in Subscription.objects.all()]
    recipients = list(set(recipients))
    datatuple = []
    for recipient in recipients:
        subscription = get_object_or_404(Subscription, email=recipient);
        title = post.title
        body = ("New post \'" + post.title + "\'" + 
                "\n\nCheck it out here:\nhttps://www.serialexperimentskyle.com/post/" + pk + "/" +
                "\n\n\nDon't want to get these notifications anymore? click here: " +
                "https://www.serialexperimentskyle.com" +
                subscription.create_unsubscribe_link())
        sender = 'kyle@serialexperimentskyle.com'
        this_tuple = (title, body, sender, [recipient])
        datatuple.append(this_tuple)
    send_mass_mail(tuple(datatuple))
    
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
