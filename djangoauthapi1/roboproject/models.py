from django.db import models


# Create your models here.
class Post(models.Model):
    title =models.CharField(max_length=100)
    description = models.TextField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name="comment")
    commentText  =  models.TextField()

    def __str__(self) -> str:
        return self.commentText


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="projects")


    def __str__(self):
        return "%s" % (self.post.title)



