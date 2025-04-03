from django.db import models

class NetworkNode(models.Model):
    LEVEL_CONTRIB = (
        (0, 'Завод'),
        (1, 'Дистрибьютор'),
        (2, 'Дилерский центр'),
        (3, 'Крупная розничная сеть'),
        (4, 'Индивидуальный предприниматель'),
    )
    name = models.CharField(max_length=50, editable=True, blank=False, null=False, db_comment="Название")
    email = models.EmailField(unique=True, editable=True, blank=False, null=False, db_comment="E-mail")
    country = models.CharField(editable=True, blank=False, null=False, max_length=64, db_comment="Страна")
    city = models.CharField(editable=True, blank=False, null=False, max_length=64, db_comment="Город")
    street = models.CharField(editable=True, blank=False, null=False, max_length=128, db_comment="Улица")
    house_number = models.CharField(editable=True, blank=False, null=False, db_comment="Номер дома")
    debt_to_producer = models.DecimalField(max_digits=10, decimal_places=2, default=0, db_comment="Задолженность перед поставщиком")
    create_time = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    level = models.IntegerField(choices=LEVEL_CONTRIB, default=0)
    producer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='producers')

    def save(self, *args, **kwargs):
        if not self.producer:
            self.level = 0
        else:
            self.level = self.producer.level + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Информация о поставщиках"

class Product(models.Model):
    name = models.CharField(max_length=256, blank=False, null=False, db_comment="Название продукта")
    model = models.CharField(max_length=128, blank=False, null=False, db_comment="Модель продукта")
    release_date = models.DateTimeField(blank=False, null=False, db_comment="Дата выхода")
    network_node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} ({self.model})"
    
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

class Employees(models.Model):
    first_name = models.CharField(max_length=64, editable=True, blank=False, null=False)
    last_name = models.CharField(max_length=64, editable=True, blank=False, null=False)
    network_node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"