from celery import shared_task
from django.utils import timezone
from random import randint
from .models import NetworkNode

@shared_task
def increase_debt():
    nodes = NetworkNode.objects.all()
    for node in nodes:
        node.debt += randint(5, 500)
        node.save()

@shared_task
def decrease_debt():
    nodes = NetworkNode.objects.all()
    for node in nodes:
        node.debt -= randint(100, 10000)
        if node.debt < 0:
            node.debt = 0
        node.save()
        
@shared_task
def clear_debt_async(node_ids):
    NetworkNode.objects.filter(id__in=node_ids).update(debt=0)