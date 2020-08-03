from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from django.db.models import Q

from .models import Blog
from .serializers import BlogSerializer
from .permissions import IsOwnerOrReadOnly
from .paginator import BlogPageNumberPaginator


class BlogListCreateView(CreateModelMixin, ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    pagination_class = BlogPageNumberPaginator

    def get_queryset(self):
        qs = Blog.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query)).distinct()
        return qs

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}


class BlogRudView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    lookup_field = 'id'
    serializer_class = BlogSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_context(self, *args, **kwargs):
        return {'request': self.request}
