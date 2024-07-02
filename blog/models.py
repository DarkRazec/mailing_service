from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Post(models.Model):
    name = models.CharField(unique=True, max_length=60, verbose_name="название")
    desc = models.TextField(verbose_name="описание")
    image = models.ImageField(upload_to='new_images', verbose_name="изображение", **NULLABLE)
    view_count = models.PositiveIntegerField(default=0, verbose_name="счетчик просмотров")
    created_at = models.DateField(verbose_name="дата создания", auto_now_add=True)
    updated_at = models.DateField(auto_now=True, verbose_name='дата изменения')
    is_published = models.BooleanField(default=True, verbose_name="опубликован")
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL", **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"

        permissions = [
            (
                'set_published',
                'Can change is_published field'
            )
        ]
