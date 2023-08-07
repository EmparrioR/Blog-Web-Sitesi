from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=50)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class Comment(MPTTModel):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    text = RichTextField(blank=True,null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    level = models.PositiveIntegerField(db_index=True, editable=False, default=0)
    lft = models.PositiveIntegerField(db_index=True, editable=False, default=0)
    rght = models.PositiveIntegerField(db_index=True, editable=False, default=0)
    tree_id = models.PositiveIntegerField(db_index=True, editable=False, default=0)

    class MPTTMeta:
        order_insertion_by = ['pub_date']

    def __str__(self):
        author_username = self.author.username if self.author else 'Unknown'
        return f"{author_username} - {self.text[:50]}"


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True,null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name="posts")
    
    def __str__(self):
        return self.title
