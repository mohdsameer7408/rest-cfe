from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.db import models


class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300)
    time_stamp = models.DateTimeField(auto_now_add=True)

    @property
    def owner(self):
        return self.author

    def __str__(self):
        return self.title

    def get_api_url(self, request=None):
        return reverse('blog-alter', kwargs={'id': self.pk}, request=request)

    class Meta:
        ordering = ['-id']
