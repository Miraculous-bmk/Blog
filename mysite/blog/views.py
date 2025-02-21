from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User  # Only if you want to display authors

# views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Post, Comment

def hero(request):
    categories = [choice[0] for choice in Post.CategoryChoices.choices]
    selected_category = request.GET.get('category')
    if selected_category in categories:
        recent_posts = Post.published.filter(category=selected_category).order_by('-publish')[:4]
    else:
        recent_posts = Post.published.order_by('-publish')[:4]
        selected_category = None 
    featured_authors = (
        User.objects
        .annotate(total_posts=Count('blog_posts'))
        .order_by('-total_posts')[:4]
    )
    recent_comments = Comment.objects.select_related('post').order_by('-created')[:10]

    return render(request, 'blog/home.html', {
        'categories': categories,
        'selected_category': selected_category,
        'recent_posts': recent_posts,
        'featured_authors': featured_authors,
        'recent_comments': recent_comments,
    })

# Create your views here.
class PostListView(ListView):
    """
    Post list view with custom pagination error handling.
    """
    model = Post
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset with error handling for invalid pages.
        """
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page') or 1
        
        try:
            # Retrieve the requested page
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            # Return the first page if the page is not an integer
            page_obj = paginator.page(1)
        except EmptyPage:
            # Return the last page if the page is out of range
            page_obj = paginator.page(paginator.num_pages)

        return (paginator, page_obj, page_obj.object_list, page_obj.has_other_pages())

    def get_queryset(self):
        # Retrieve all published posts
        return Post.published.all()

def search(request):
    query = request.GET.get('q', '')
    results = Post.objects.filter(title__icontains=query)
    return render(request, 'blog/post/search_results.html', {'results': results, 'query': query})

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag =get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags=tag)
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag':tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED, slug=post,publish__year=year, publish__month=month, publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form':form, 'similar_posts': similar_posts})

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = EmailPostForm()
    sent = False

    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'mikosnetworks@gmail.com', [cd['to']])
            sent = True
    return render(request, 'blog/post/share.html', {'post': post,'form': form, 'sent':sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post,'form': form, 'comment': comment})