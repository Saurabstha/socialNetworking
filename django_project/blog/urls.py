from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,UserPostListView, SearchPostListView

urlpatterns = [
    # path('home/', views.home, name = 'blog-home'),

    path('', PostListView.as_view(), name = 'blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),

    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
    path('about/', views.about, name = 'blog-about'),
    # path('raw_sql/<str:idd>/', views.raw_sql),
    path('raw_sql/<str:idd>/', views.raw_sql),
    path('raw_sql_search/<str:idd>/', views.search),

    path('search/', SearchPostListView.as_view(), name='query'),

]
