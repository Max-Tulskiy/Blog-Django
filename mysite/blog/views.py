from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Постраничная разбивка
from django.views.generic import ListView
from .forms import EmailPostForm

# Create your views here.
'''
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
'''


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})


def post_list(request):
    post_list = Post.published.all()

    # Постраничная разбивка
    paginator = Paginator(post_list, 3)  # 3 поста на страницу
    page_number = request.GET.get('page', 1)  # получаем номер страницы, если нет, то возвращаем 1

    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


def post_share(request, post_id):
    # Извлекаем пост по id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # передача формы на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
        return render(request,
                      'blog/post/share.html',
                      {'post': post, 'form': form})
