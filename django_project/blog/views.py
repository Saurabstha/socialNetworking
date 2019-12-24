from django.shortcuts import render, get_object_or_404
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.contrib import messages

# from django.http import HttpResponse

# posts = [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2018'
#     }
# ]

# Create your views here.
def home(request):
    # return HttpResponse("<h1>home</h1>")
    # return render(request, 'blog\home.html')
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})

# def abt(request):
#     return render(request, 'blog\abt.html')

class PostListView(ListView):
    model = Post
    template_name ='blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2
    #
    # def get_queryset(self, *args,**kwargs):
    #     request = self.request
    #     print(request)
    #     return Post.objects.all()

class SearchPostListView(ListView):
    model = Post
    template_name ='blog/search_result.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    # paginate_by = 2

    def get_queryset(self, *args,**kwargs):
        request = self.request
        # print(request.GET)
        query = request.GET.get('q')
        # print(query)
        if query is not None:
            print(Post.objects.filter(Q(title__icontains=query)))
            return Post.objects.filter(Q(title__icontains=query))
        return Post.objects.none()



class UserPostListView(ListView):
    model = Post
    template_name ='blog/user_posts.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def raw_sql(request,idd):
    name = ""
    print(idd)
    for p in Post.objects.raw('''SELECT * FROM blog_post where title = %s''',[idd]):
        name = name + " " + p.title
    return JsonResponse({'result':name})

def search(request, idd):

    # if request.method == 'POST':
    #     # srch = request.POST['search']

    if idd:

        match = Post.objects.filter(Q(title__icontains=idd))

        if match:
            return HttpResponse({'title': match })

        else:
            messages.error(request, 'no result')



