from rest_framework import serializers


class HomepageSerializer(serializers.Serializer):
    Best_Selling_products = serializers.ListField(source='Best-Selling products')
    Articles = serializers.DictField()
    Discussion = serializers.ListField()
