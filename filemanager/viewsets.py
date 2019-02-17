from rest_framework import viewsets
from .models import Data
from .serializers import DataSerializer
from rest_framework.response import Response # from viewsets doc
from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import permissions, status

from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
# A ViewSet class is simply a type of class-based View,
# that does not provide any method handlers such as .get() or .post(),
# and instead provides actions such as .list() and .create().

# Typically, rather than explicitly registering the views in a viewset
# in the urlconf, you'll register the viewset with a router class,
# that automatically determines the urlconf for you.

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    permission_classes = (permissions.AllowAny,) # we assume that we have a session user
    parser_classes = (MultiPartParser, FormParser )

    def post(self, request, format=None):
        # print(request.data['file'].name)
        # print(dir(request.FILES['file']))
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            for k, v in kwargs.items():
                for id in v.split(','):
                    obj = get_object_or_404(Data, pk=int(id))
                    self.perform_destroy(obj)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    # def post(self, request):
    #     print(request.data)
    #     print(request.FILES)
    #     serializer_class = DataSerializer(data=request.data)
    #     if serializer_class.is_valid():
    #         serializer_class.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    #
    # @permission_classes((IsAdminUser, ))
    # def post(self, request, format=None):
    #     # file = self.request.data.get('file', False)
    #     print(file)



# class DataViewSet(viewsets.ViewSet):


#     def list(self, request, pk=None):
#         # queryset = Data.objects.all()
#         # serializer = DataSerializer(queryset, many=True)
#         # return Response(serializer.data)
#         querysets = Data.objects.all()
#         size = []
#         for queryset in querysets:
#             size.append(queryset.data.size)
#         file_size = get_object_or_404(size, pk=pk)
#         serializer = DataSerializer(file_size)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Data.objects.all()
#         filedata = get_object_or_404(queryset, pk=pk)
#         serializer = DataSerializer(filedata)
#         return Response(serializer.data)

#     def get_custom(self, request, pk=None):
#         queryset = Data.objects.all()
#         for query in queryset:
#             size = query.data.size
#         file_size = get_object_or_404(size, pk=pk)
#         serializer = DataSerializer(file_size)
#         return Response(serializer.data)
