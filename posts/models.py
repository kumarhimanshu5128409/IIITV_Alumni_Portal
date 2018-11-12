from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from urllib.parse import urlparse
from datetime import datetime


class Post(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete='CASCADE')
    date = models.DateTimeField(auto_now_add=True)
    link = models.URLField(max_length=600, blank=True)
    text = models.TextField(blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='posts')
    def score(self):
        return Vote.objects.filter(post=self, upvote=True).count() - Vote.objects.filter(post=self,
                                                                                         upvote=False).count()

    def comments_count(self):
        return Comment.objects.filter(post=self).count()

    def get_domain(self):
        return urlparse(self.link).netloc

    def get_absolute_url(self):
        return reverse('posts:details', args=[str(self.pk)])

    def __unicode__(self):
        return self.title


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete='CASCADE')
    post = models.ForeignKey(Post, on_delete='CASCADE')
    upvote = models.BooleanField()

    def __unicode__(self):
        return "%s upvoted %s" % (self.voter.username, self.post.title)


class Comment(MPTTModel):
    """ Threaded comments for posts """
    post = models.ForeignKey(Post, on_delete='CASCADE')
    author = models.ForeignKey(User, on_delete='CASCADE')
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    # a link to comment that is being replied, if one exists
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete='CASCADE')

    def score(self):
        return CommentVote.objects.filter(comment=self, upvote=True).count() - CommentVote.objects.filter(comment=self,
                                                                                                          upvote=False).count()

    class MPTTMeta:
        order_insertion_by = ['date']

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now()
        super(Comment, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s comment on %s" % (self.author.username, self.post)


class CommentVote(models.Model):
    voter = models.ForeignKey(User, on_delete='CASCADE')
    comment = models.ForeignKey(Comment, on_delete='CASCADE')
    upvote = models.BooleanField()

    def __unicode__(self):
        return "%s upvoted %s" % (self.voter.username, self.comment)
