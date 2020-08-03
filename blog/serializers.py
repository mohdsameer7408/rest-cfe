from rest_framework import serializers

from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name='blog-alter', lookup_field='id')

    class Meta:
        model = Blog
        fields = ['url', 'id', 'author', 'title', 'description']

    def get_url(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

    def get_author(self, obj):
        return obj.author.username
