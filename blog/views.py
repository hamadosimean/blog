from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from .models import Post
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.


# ! This method return all the post with published status
# def post_list(request):
#     posts = Post.published.all()
#     context = {"posts": posts}
#     return render(
#         request,
#         "blog/post/list.html",
#         context,
#     )


# ! this is pagination page


def post_list(request, tag_slug=None):
    object_lists = Post.published.all()
    tags = Tag.objects.all().distinct()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_lists = object_lists.filter(tags__in=[tag])
    paginator = Paginator(object_lists, 4)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of the range
        posts = paginator.page(paginator.num_pages)

    context = {
        "posts": posts,
        "page": page,
        "tag": tag,
        "tags": tags,
    }
    return render(
        request,
        "blog/post/list.html",
        context,
    )


# ! This method return single post
# def post_detail(request, year, month, day, post):
#     post = get_object_or_404(
#         Post,
#         slug=post,
#         status="published",
#         publish__year=year,
#         publish__month=month,
#         publish__day=day,
#     )
#     context = {"post": post}

#     return render(
#         request,
#         "blog/post/detail.html",
#         context,
#     )


# ! This method return single post
def post_detail(request, year, month, day, post):
    post = Post.published.get(
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            print(post)
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    context = {
        "post": post,
        "comments": comments,
        "new_comment": new_comment,
        "comment_form": comment_form,
        "similar_posts": similar_posts,
    }
    return render(
        request,
        "blog/post/detail.html",
        context,
    )


# ! Share post with friends


def share_post(request, post_id):
    # retrieve respective post

    post = get_object_or_404(Post, id=post_id, status="published")

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cleand_data = form.cleaned_data
            print(cleand_data)
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cleand_data['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cleand_data['comments']}"
            send_mail(
                subject,
                message,
                "fatihamtech@gmail.com",
                [cleand_data.get("to")],
                fail_silently=False,
            )
            return render(
                request,
                "blog/post/share.html",
                {"form": form, "success": True},
            )
    else:
        form = EmailPostForm()
        context = {
            "form": form,
            "post": post,
        }
    return render(
        request,
        "blog/post/share.html",
        context,
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]

            #! First results only with query
            # results = Post.published.annotate(
            #     search=SearchVector("title", "body")
            # ).filter(search=query)

            #! Second results with stemming and ranking
            search_vector = SearchVector("title", "body")
            search_query = SearchQuery(query)
            results = (
                Post.published.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(search=search_query)
                .order_by(("-rank"))
            )
    context = {
        "form": form,
        "query": query,
        "results": results,
    }
    return render(request, "blog/post/search.html", context=context)
