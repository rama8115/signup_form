from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from .models import BlogPost, Category

@login_required
def create_blog_post(request):
    if request.user.user_type != 'doctor':
        return redirect('login')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('doctor_blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_blog_post.html', {'form': form})

@login_required
def doctor_blog_list(request):
    if request.user.user_type != 'doctor':
        return redirect('login')
    
    blog_posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/doctor_blog_list.html', {'blog_posts': blog_posts})

@login_required
def patient_blog_list(request):
    if request.user.user_type != 'patient':
        return redirect('login')
    
    categories = Category.objects.all()
    return render(request, 'blog/patient_blog_list.html', {'categories': categories})

@login_required
def patient_blog_category(request, category_id):
    if request.user.user_type != 'patient':
        return redirect('login')
    
    category = Category.objects.get(id=category_id)
    blog_posts = BlogPost.objects.filter(category=category, is_draft=False)
    return render(request, 'blog/patient_blog_category.html', {'category': category, 'blog_posts': blog_posts})
