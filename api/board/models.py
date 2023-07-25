from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

from api.category.models import Category


# Create your models here.
class Item(models.Model):
    item_id = models.PositiveSmallIntegerField(null=True)
    item_title = models.CharField(max_length=64, null=True, blank=True)
    item_description = models.CharField(max_length=256, null=True, blank=True)
    order_id = models.PositiveSmallIntegerField(null=True)
    created_date = models.DateTimeField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.item_title
    
    @classmethod
    def count(cls, user, category_id):
        return Item.objects.filter(Q(owner=user) & Q(category_id = category_id)).count()
    
    @classmethod
    def get_next_id(cls):
        return Item.objects.all().count()

    def order(self, desired_id):
        order_before = Item.objects.filter(
            Q(owner=self.owner) & Q(order_id__lt=desired_id) & Q(category=self.category)
        )
        order_after = Item.objects.filter(
            Q(owner=self.owner) & Q(order_id__gte=desired_id) & Q(category=self.category)
        )
        
        counter = 1

        for item in order_before:
            if item != self:
                item.order_id = counter
                item.save()
                counter += 1
            else:
                pass
        
        self.order_id = counter
        self.save()
        counter += 1

        for item in order_after:
            if item != self:
                item.order_id = counter
                item.save()
                counter += 1
            else:
                pass

    class Meta:
        ordering = ['category__id', 'order_id']
