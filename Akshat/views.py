from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Post, Comments

def form(request) :
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        dp = request.FILES.get('dp')


        user = User.objects.create_user(
            email = email,
            username = username,
            password = password,
            
        )

        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.dp = dp
        user.save()
        return redirect('/test/login')
    return render(request, 'signupform.html')

@login_required
def post(request) :
    if request.method == 'POST':
        content = request.POST['content']
        tags = request.POST['tags']
        image = request.FILES.get('image')

        if content :    
            Post.objects.create(
                user = request.user,
                content = content,
                tags = tags,
                image = image
            )
            return redirect('/test/dashboard/')

        else:
            return HttpResponse("Post content is required.", status=400)

    return render(request, 'postform.html')

@login_required
def comment_views(request, post_id) :
        content = get_object_or_404(Post, id = post_id )
        comments = Comments.objects.all().filter(content_id = post_id)

        if request.method == "POST":
            comment = request.POST.get("comment")
            if comment:
                Comments.objects.create(
                user = request.user,
                content = content,
                comment = comment
            )
            return redirect('comment', post_id=post_id)
        return render(request, 'commentform.html', {'content': content, 'comments': comments})

def login_view(request) :
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/test/dashboard/')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'loginform.html')
    return render(request, 'loginform.html')

def logout_view(request) :
    logout(request)
    return redirect("/test/login/")

@login_required
def dashboard(request) :
    posts = Post.objects.all().order_by('-id')
    return render(request, "dashboard.html", {"posts": posts})

@login_required
def comm_count(request):
    comments = Comments.objects.all().order_by("-id")
    return render(request, "commentform.html",{"comments": comments})

@login_required
def profile(request):
    user = request.user
    return render(request, "profile.html", {"user": user})
