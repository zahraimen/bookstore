from django.db import models

from django.urls import reverse
from django.contrib.auth import get_user_model


# Create your models here.
class Book(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    content = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    cover = models.ImageField(upload_to='covers/', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.id])


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    full_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    text = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    recommend = models.BooleanField(default=True)

    def __str__(self):
        return self.text

    def get_author_name(self):
        try:
            return self.user.username
        except AttributeError:
            return self.full_name

    def get_absolute_url(self):
        return reverse('book_detail', args=[self.book.id]) + f'#{self.id}'
