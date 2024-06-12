from rest_framework import generics
from django.core.cache import cache
from rest_framework.response import Response
from zookeeper.filters import AnimalFilter
import requests
from zookeeper.models import Animal, Category
from zookeeper.serializers import AnimalSerializer, CategorySerializer
# Create your views here.
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @method_decorator(cache_page(60 * 1))
    def list(self, request, *args, **kwargs):
        response = requests.get('https://httpbin.org/delay/2')
        return super().list(request, *args, **kwargs)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AnimalListView(generics.ListCreateAPIView):
    filterset_class = AnimalFilter
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def list(self, request, *args, **kwargs):
        query_params = request.query_params
        cache_key = f'animals_list{query_params}'
        data = cache.get(key=cache_key)
        if not data:
            filtered_queryset = self.filter_queryset(self.get_queryset())
            cache_time = 60 * 5
            serializer = AnimalSerializer(filtered_queryset, many=True)
            cache.set(key=cache_key, timeout=cache_time, value=serializer.data)
            return Response(serializer.data)
        
        return Response(data)


class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
