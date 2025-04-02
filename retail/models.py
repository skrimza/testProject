from django.db import models
from django.core.validators import MinValueValidator

class NetworkNode(models.Model):
    LEVEL_CHOICES = [
        (0, 'Завод'),
        (1, 'Дистрибьютор'),
        (2, 'Дилерский центр'),
        (3, 'Крупная розничная сеть'),
        (4, 'Индивидуальный предприниматель'),
    ]
    name = models.CharField(max_length=50, editable=True, blank=False, null=False, db_comment="Название")
    email = models.EmailField(unique=True, editable=True, blank=False, null=False, db_comment="E-mail")
    country = models.CharField(editable=True, blank=False, null=False, max_length=64)
    city = models.CharField(editable=True, blank=False, null=False, max_length=64)
    street = models.CharField(editable=True, blank=False, null=False, max_length=128)
    house_number = models.IntegerField(editable=True, blank=False, null=False, max_length=10)
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)])
    created_at = models.DateTimeField(blank=False, null=False, auto_now=True)
    level = models.IntegerField(choices=LEVEL_CHOICES, default=0)
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='clients')

    def save(self, *args, **kwargs):
        if not self.supplier:
            self.level = 0
        else:
            self.level = self.supplier.level + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=25)
    model = models.CharField(max_length=50)
    release_date = models.DateField()
    network_node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} ({self.model})"

class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    network_node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"