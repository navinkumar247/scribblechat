from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from  .utils import get_unique_code

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=254, unique=True, blank = False)
    image = models.ImageField(upload_to='profile_pics', default='default.png')
    bio = models.TextField(max_length=500, default='no bio...')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # contacts = models.ManyToManyField(User, related_name='contacts')

    def __str__(self):
        return self.user.username

    def get_friends(self):
        friends_receiver = self.receiver.filter(status = 'accepted')
        friends_sender = self.sender.filter(status = 'accepted')
        friends = friends_receiver.union(friends_sender)
        return friends

    def get_received_friends_request(self):
        return self.user.receiver.filter(status = 'sent')


    # def get_absolute_url(self):
    #     return reverse("profiles/register.html", kwargs={"pk": self.pk})
STATUS_CHOICE = {
    ('sent','sent'),
    ('accepted','accepted'),
}

class Relationship(models.Model):
    # users = models.ManyToManyField(Profile, related_name='friends')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(choices=STATUS_CHOICE, max_length=8)
    slug = models.SlugField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}--{}--{}".format(self.sender.user.username, self.receiver.user.username, self.status) 

    def save(self, *args, **kwargs):
        slug_exist = False
        if self.sender and self.receiver:
            to_slug = slugify(str(self.sender.user.username)+str(self.receiver.user.username))
            slug_exist = Relationship.objects.filter(slug=to_slug).exists()
            while slug_exist:
                to_slug = str(to_slug+ str(get_unique_code()))
                slug_exist = Relationship.objects.filter(slug=to_slug).exists()
        else:
            to_slug = None
        self.slug = to_slug

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
