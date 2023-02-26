from numpy import source
from . models import Product
from rest_framework import serializers


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    subcategory = serializers.CharField(source='subcategory_id')
    class Meta:
        model = Product
        fields = '__all__'