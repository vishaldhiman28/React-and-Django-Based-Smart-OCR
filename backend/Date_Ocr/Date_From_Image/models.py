from django.db import models



class Post(models.Model):
    title="IMAGE"
    image = models.ImageField(upload_to='post_images')
    
    def __str__(self):
        return self.title

    