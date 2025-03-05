from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import EmailPostForm, CommentPostForm
from django.core.mail import send_mail
from blog.models import Post
from mainSite import settings
from django.views.decorators.http import require_POST

"""
def post_list(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.xhtml", {"posts": posts})
"""


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None

    form = CommentPostForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.xhtml",
        {"post": post, "form": form, "comment": comment},
    )


class PostListView(ListView):
    template_name = "blog/post/list.xhtml"
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3


def post_share(request, post_id):
    sent = False
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"

            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )

            # send_mail(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
            print(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
            sent = True

    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.xhtml", {"post": post, "form": form, "sent": sent}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
        status=Post.Status.PUBLISHED,
    )
    return render(request, "blog/post/detail.xhtml", {"post": post})
