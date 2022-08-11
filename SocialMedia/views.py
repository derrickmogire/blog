from django.shortcuts import render, redirect, get_object_or_404
from SocialMedia.models import Post, Profile, Images
from SocialMedia.forms import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.forms import modelformset_factory
from django.contrib.auth.forms import *
from django.views.generic import View
# Create your views here.


def home(request):
    post_list = Post.objects.all().order_by('-created')
    query = request.GET.get('q')
    if query:
        post_list = Post.objects.filter(Q(title__icontains=query) | Q(
            body__icontains=query) | Q(author__username=query))
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    if page is None:
        start_index = 0
        end_index = 7
    else:
        (start_index, end_index) = proper_pagination(posts, index=4)
    page_range = list(paginator.page_range)[
        start_index:end_index]
    context = {'posts': posts, 'page_range': page_range, }
    return render(request, 'social.html', context)


def proper_pagination(posts, index):
    start_index = 0
    end_index = 7
    if posts.number > index:
        start_index = posts.number-index
        end_index = start_index+end_index
    return (start_index, end_index)


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comment.objects.filter(post=post).order_by('-id')
    is_liked = False
    is_favourite = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    if post.favourite.filter(id=request.user.id).exists():

        is_favourite = True

    if request.method == 'POST':
        comment = CommentForm(request.POST)
        if comment.is_valid():
            content = request.POST.get('comment')
            post_comment = Comment.objects.create(
                post=post, user=request.user, comment=content)
            post_comment.save()
            return HttpResponseRedirect(post.get_absolute_url())

    else:
        comment = CommentForm()
    context = {'post': post, 'is_liked': is_liked, 'is_favourite': is_favourite,
               'total_likes': post.total_likes(), "comments": comments, 'comment': comment}

    return render(request, 'post_detail.html', context)


def createpost(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=4)
    if request.method == 'POST':
        form = SocialForm(request.POST)
        formset = ImageFormSet(
            request.POST or None, request.FILES or None, queryset=Images.objects.none())
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            for f in formset:

                photo = Images(
                    post=instance, image=f.cleaned_data['image'])
                photo.save()
                return redirect('home')

        return redirect('home')
    else:
        form = SocialForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'create_post.html', {'form': form, 'formset': formset})


def edit_profile(request):
    form = EditProfileForm()
    return render(request, 'edit_profile.html', {'form': form})


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {'post': post, 'is_liked': is_liked,
               'total_likes': post.total_likes()}
    return HttpResponse('')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('login')

    return render(request, 'registration/login.html', {})


def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'registration/sign-up.html', {'form': form})


def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    if request.method == "POST":
        form = EditPostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = EditPostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'edit_profile.html', context)


def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        raise Http404()
    post.delete()
    return redirect('home')


def favourite_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)

    else:
        post.favourite.add(request.user)

    return HttpResponseRedirect(post.get_absolute_url())


@login_required
def favourite_posts_list(request):
    user = request.user
    favourite_posts = user.favourite.all()
    context = {'favourites': favourite_posts}
    return render(request, 'favourite.html', context)


# class Viewscount(View):
#     model = Post
#     template_name = 'post_detail.html'

#     def get_object(self):
#         object = super(Post, self).get_object()
#         object.views += 1
#         object.save()
#         return object
