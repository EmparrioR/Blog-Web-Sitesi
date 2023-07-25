from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, ReplyForm, CommentForm, UserCreationForm, PostCreateForm
from .models import Post, Comment
from .models import Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db.models import Prefetch
from .forms import CategoryForm



from .forms import PostForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('post_list')  
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()

    query = request.GET.get('q')
    if query:
        posts = posts.filter( 
            Q(title__icontains=query) | 
            Q(author__first_name__icontains=query) |
            Q(pub_date__icontains=query)  ).distinct()
           

    return render(request, 'blog/post_list.html', {'posts': posts})

def hesabim(request):

    

    return render(request, 'blog/hesabim.html')

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if comment.author == request.user or comment.replies.filter(author=request.user).exists() or request.user.is_superuser:
        comment.delete()
        messages.success(request, 'Yorum başarıyla silindi.')
    else:
        messages.error(request, 'Yorumu silme yetkiniz yok.')

    return redirect('post_detail', pk=comment.post.pk) 




def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post, parent=None)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            parent_comment_id = request.POST.get('parent_comment_id')
            parent_comment = Comment.objects.get(pk=parent_comment_id) if parent_comment_id else None
            comment = Comment(
                post=post,
                author=request.user,
                text=form.cleaned_data['text'],
                parent=parent_comment
            )
            comment.save()
            # Yorum gönderme işlemi tamamlandıktan sonra formu temizleyerek sayfayı yeniden yüklüyoruz
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

@login_required
def reply_to_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = comment.post
            reply.author = request.user
            reply.parent = comment
            reply.save()
            # Cevap gönderme işlemi tamamlandıktan sonra formu temizleyerek sayfayı yeniden yüklüyoruz
            return redirect('post_detail', pk=comment.post.pk)
    # PRG: Redirect in case of GET request or form validation failure
    return redirect('post_detail', pk=comment.post.pk)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def kategoriye_gore_listele(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/kategoriye_gore_listele.html', {'posts': posts, 'category': category})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostCreateForm()

    return render(request, 'blog/post_create.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'blog/post_delete.html', {'post': post})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('post_list')  # Veya istediğiniz başka bir sayfaya yönlendirin
    else:
        form = CategoryForm()
    return render(request, 'blog/create_category.html', {'form': form})
