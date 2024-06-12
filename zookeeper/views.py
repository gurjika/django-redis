from rest_framework import generics
from django.core.cache import cache
from rest_framework.response import Response
from zookeeper.filters import AnimalFilter
from zookeeper.models import Animal, Category
from zookeeper.serializers import AnimalSerializer, CategorySerializer
# Create your views here.


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AnimalListView(generics.ListCreateAPIView):
    filterset_class = AnimalFilter
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'animals_list'
        cache_time = 60 * 5
        data = cache.get(key=cache_key)

        if not data:
            animals = self.get_queryset()
            serializer = AnimalSerializer(animals, many=True)
            cache.set(key=cache_key, timeout=cache_time, value=serializer.data)
            return Response(serializer.data)
        
        return Response(data)


class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
