from django.urls import path
from .views import BlogListCreateView, BlogRudView


urlpatterns = [
    path('blog/', BlogListCreateView.as_view(), name='blog-list'),
    path('blog/<int:id>/', BlogRudView.as_view(), name='blog-alter'),
]
