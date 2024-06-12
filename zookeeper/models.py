from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name
    


class Animal(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='animals')
    scientific_name = models.CharField(max_length=255)
    description = models.TextField()
    habitat = models.CharField(max_length=100)
    diet = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name