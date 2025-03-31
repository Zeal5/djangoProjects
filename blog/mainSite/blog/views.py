from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from blog.models import Post
from mainSite import settings
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.xhtml", {"posts": posts, "tag": tag})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None

    form = CommentForm(data=request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.xhtml",
        {"post": post, "form": form, "comment": comment},
    )


"""
class PostListView(ListView):
    template_name = "blog/post/list.xhtml"
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
"""


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
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]

    return render(
        request,
        "blog/post/detail.xhtml",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )
