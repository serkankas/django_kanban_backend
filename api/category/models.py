from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.
class Category(models.Model):
    category_id = models.SmallAutoField(verbose_name="Category ID")
    category_title = models.CharField(max_length=64, null=True, blank=True)
    order_id = models.PositiveSmallIntegerField(null=True)
    created_date = models.DateTimeField(auto_created=True)
    user_accesses = models.ManyToManyField(User, null=True)

    def __str__(self) -> str:
        return self.category_title

    @classmethod
    def count(cls, user):
        return Category.objects.filter(user_accesses=user).count()

    def order(self, desired_id):
        order_before = Category.objects.filter(
            Q(user_accesses=self.user_accesses) & Q(order_id__tl=desired_id)
        )
        order_after = Category.objects.filter(
            Q(user_accesses=self.user_accesses) & Q(order_id__gte=desired_id)
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
