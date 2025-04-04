from django.shortcuts import render
from django.db.models import Avg
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .models import NetworkNode
from .serializers import NetworkNodeSerializer
from rest_framework.permissions import BasePermission

class IsActiveEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active

class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country', 'products__id']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country=country)
        return queryset
    
    @action(detail=False, methods=['get'])
    def high_debt(self, request):
        avg_debt = NetworkNode.objects.aggregate(avg_debt=Avg('debt'))['avg_debt']
        nodes = NetworkNode.objects.filter(debt__gt=avg_debt)
        serializer = self.get_serializer(nodes, many=True)
        return Response(serializer.data)
