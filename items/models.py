from django.db import models
from users.models import User
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_delete,post_save,pre_save
# from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
# gd_storage = GoogleDriveStorage()

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(upload_to="items/images/", blank = True) #storage=gd_storage
    description = models.TextField(blank = True)
    original_cost = models.FloatField()
    revised_cost = models.FloatField()
    stock = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    booked = models.PositiveIntegerField(default=0)
    category = models.CharField(choices=(('women','Women'),('men','Men'),('childrenboy','Children Boys'),('childrengirl','Children Girls')), max_length=20)
    subcategory = models.CharField(choices=(('saree','Saree'),('kurtis','Kurtis'),('pant','Pant'),('shirt','Shirt'),('top','Top'),('chudidhar','Chididhar'),('other','Other')), max_length=20)
    material_type = models.CharField(choices=(('cotton','Cotton'),('silk','Silk'),('wool','Wool'),('leather','Leather'),('jeans','Jeans'),('other','Other')), max_length=20)
    newly_arrived = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.image.path)
    #
    #     output_size = (260,300)
    #     img = img.resize(output_size)
    #     img.save(self.image.path)

class Cart(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='carts')
    item_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'item',)


# Signals

# @receiver(post_delete, sender=Item)
# def submission_delete(sender, instance, **kwargs):
#     """
#     This function is used to delete attachments when a file object is deleted.
#     Django does not do this automatically.
#     """
#     instance.image.delete(False)
