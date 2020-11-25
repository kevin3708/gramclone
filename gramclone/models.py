from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
import uuid

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.profile.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(max_length=120, null=True)
    avatar = CloudinaryField('image')
    
    def __str__(self):
        return self.bio
    
    def save_image(self):
        self.save()
        
    def delete_image(self):
        self.delete()
    
    @classmethod
    def update(cls, id, value):
        cls.objects.filter(id=id).update(avatar=value)
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    image = models.ImageField(upload_to=user_directory_path, verbose_name='Picture', null=True)
    image_name = models.CharField(max_length=120, null=True)
    caption = models.TextField(max_length=1000, verbose_name='Caption', null=True)
    date = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_profile')
    like = models.IntegerField(default=0)
    
    # class Meta:
    #     ordering = ['-date',]
    
    def __str__(self):
        return self.image_name
    
    def save_image(self):
        self.save()
        
    @classmethod
    def search_user(cls,search_term):
        users = User.objects.filter(username__icontains=search_term)
        return users
        
    def delete_image(self):
        self.delete()
    
    @classmethod
    def update_caption(cls, id, value):
        cls.objects.filter(id=id).update(caption=value)
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    
class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()
    
    def add_post(sender,instance,*args,**kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.date, following=user)
            stream.save()
            
class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

class Comment(models.Model):
    comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
            
post_save.connect(Stream.add_post, sender=Post)
