from django.db import models
from django.template.defaultfilters import slugify


class Article(models.Model):
    article_title = models.CharField(max_length=150, unique=True)
    article_description = models.TextField()
    article_link = models.URLField()
    article_text = models.TextField()
    article_date = models.DateField()
    article_slug = models.SlugField(max_length=150, unique=True)
    article_source = models.CharField(max_length=50)
    article_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.article_title

    def save(self, *args, **kwargs):
        self.article_slug = slugify(self.article_title + str(self.article_date))
        super(Article, self).save(*args, **kwargs)
