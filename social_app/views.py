from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .models import Post, Image
from taggit.models import Tag
from django.utils.html import escape
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

# Create your views here.


def log_out(request):
    logout(request)
    return HttpResponse('شما خارج شدید!')


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user)
    saved_posts = user.saved_post.all()

    context = {
        'posts': posts,
        'saved_posts': saved_posts,
    }
    return render(request, 'social/profile.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def user_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
        return redirect('social:profile')
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'user_form': user_form
    }
    return render(request, 'registration/edit_user.html', context)


def ticket(request):
    send = False
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}"
            send_mail(cd['subject'], message, 'ali0182mohammadi@gmail.com',
                      ['alimohammadi.dev01@gmail.com'], fail_silently=False)
            send = True
    else:
        form = TicketForm()

    return render(request, 'forms/ticket.html', {'form': form, 'send': send})


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = []
    except PageNotAnInteger:
        posts = paginator.page(1)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        render(request, 'social/list_ajax.html', {'posts': posts})

    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, 'social/list.html', context)


@login_required()
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            img1 = Image.objects.create(image_field=form.cleaned_data['image1'], post=post)
            post.images.add(img1)

            img2 = Image.objects.create(image_field=form.cleaned_data['image2'], post=post)
            post.images.add(img2)

            return redirect('social:profile')
    else:
        form = CreatePostForm()
        return render(request, 'forms/create-post.html', {'form': form})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:2]

    context = {
        'post': post,
        'similar_post': similar_post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'social/detail.html', context)


def post_search(request):
    query = None
    post_results = []
    tag_results = []
    if 'query' in request.GET:
        form = PostSearchForm(data=request.GET)
        if form.is_valid():
            query = escape(form.cleaned_data['query'])
            post_results = Post.objects.filter(description__icontains=query)
            tag_results = Tag.objects.filter(name__icontains=query)
            tag_results = Post.objects.filter(tags__in=tag_results)
            # results = tag_results | post_results

    context = {
        'query': query,
        'post_results': post_results,
        'tag_results': tag_results,
    }
    return render(request, 'social/search.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'comment': comment,
        'form': form
    }
    return render(request, 'forms/comment.html', context)


@login_required()
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('social:profile')
    return render(request, 'forms/delete_post.html', {'post': post})


@login_required()
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            Image.objects.create(image_field=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_field=form.cleaned_data['image2'], post=post)

            redirect('social:profile')
    else:
        form = CreatePostForm(instance=post)
    contex = {
        'post': post,
        'form': form,
    }
    return render(request, 'forms/create-post.html', contex)


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('social:profile')


@login_required()
@require_POST
def like_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = get_object_or_404(Post, id=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False

        else:
            post.likes.add(user)
            liked = True

        post_likes_count = post.likes.count()
        response_date = {
            'liked': liked,
            'likes_count': post_likes_count,
        }

    else:
        response_date = {'Error': 'Invalid post_id'}

    return JsonResponse(response_date)


@login_required
@require_POST
def save_post(request):
    post_id = request.POST.get('post_id')
    if post_id is not None:
        post = Post.objects.get(id=post_id)
        user = request.user

        if user in post.saved_by.all():
            post.saved_by.remove(user)
            saved = False
        else:
            post.saved_by.add(user)
            saved = True

        return JsonResponse({'saved': saved})
    return JsonResponse({'error': 'Invalid request'})












