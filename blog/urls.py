from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogDeleteView, BlogUpdateView, published_activity

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='view'),
    path('create/', BlogCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>/', published_activity, name='activity'),
]
