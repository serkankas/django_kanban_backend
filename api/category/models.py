from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.
class Category(models.Model):
    category_id = models.PositiveSmallIntegerField(null=True)
    category_title = models.CharField(max_length=64, null=True, blank=True)
    order_id = models.PositiveSmallIntegerField(null=True)
    created_date = models.DateTimeField()
    user_accesses = models.ManyToManyField(User)

    def __str__(self) -> str:
        return self.category_title

    @classmethod
    def count(cls, user):
        return Category.objects.filter(user_accesses=user).count()
    
    @classmethod
    def get_next_id(cls):
        return Category.objects.all().count()

    def order(self, desired_id, user_id):
        order_before = Category.objects.filter(
            Q(user_accesses=user_id) & Q(order_id__lt=desired_id)
        )
        order_after = Category.objects.filter(
            Q(user_accesses=user_id) & Q(order_id__gte=desired_id)
        )
        
        counter = 1

        for item in order_before:
            if item != self:
                item.order_id = counter
                item.save()
                counter += 1
            else:
                pass
        
        self.order_id = desired_id
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
        ordering = ['order_id']
        verbose_name_plural = "Categories"
