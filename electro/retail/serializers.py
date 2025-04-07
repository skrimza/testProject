from rest_framework import serializers
from .models import NetworkNode, Product

class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'

class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    producer = serializers.PrimaryKeyRelatedField(queryset=NetworkNode.objects.all(), allow_null=True)

    class Meta:
        model = NetworkNode
        fields = '__all__'
        read_only_fields = ('debt_to_producer',)