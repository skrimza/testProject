from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer, ProductSerializer

class IsActiveEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'employees') and request.user.employees.first().is_active

class NetworkNodeList(generics.ListAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]

class NetworkNodeByCountry(generics.ListAPIView):
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]

    def get_queryset(self):
        return NetworkNode.objects.filter(country=self.kwargs['country'])

class DebtAboveAverage(APIView):
    permission_classes = [IsActiveEmployee]

    def get(self, request):
        avg_debt = NetworkNode.objects.aggregate(Avg('debt'))['debt__avg']
        queryset = NetworkNode.objects.filter(debt__gt=avg_debt)
        serializer = NetworkNodeSerializer(queryset, many=True)
        return Response(serializer.data)

class NetworkNodeByProduct(generics.ListAPIView):
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]

    def get_queryset(self):
        return NetworkNode.objects.filter(products__id=self.kwargs['product_id'])

class NetworkNodeCreate(generics.CreateAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]

class NetworkNodeDelete(generics.DestroyAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]

class NetworkNodeUpdate(generics.UpdateAPIView):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]

class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]

class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveEmployee]