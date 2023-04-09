from django.db import models
from accounts.models import CreatedUpdatedModel, User
from django.core.exceptions import ValidationError

# Create your models here.

class Category(CreatedUpdatedModel):
    name = models.CharField(max_length=200)
    cost_point = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.name}"

class Order(CreatedUpdatedModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="order", null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name="order", null=True)
    copies = models.IntegerField(default=1)
    page = models.IntegerField(default=1, null=True, blank=True)
    color_print = models.BooleanField(default=False)

    # printing_side False for one side and True for both side
    printing_side = models.BooleanField(default=False)
    special_instruction = models.CharField(max_length=500, null=True, blank=True)
    
    set_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.first_name} => {self.id}"
    
    def save(self, *args, **kwargs):
        if self.set_default == True:
            User.objects.filter(user = self.user, set_default = True).update(set_default = False)
        return super().save(self, *args, **kwargs)

