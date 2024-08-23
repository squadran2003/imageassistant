from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from images.models import Image
from images.serializers import ImageSerializer


class ImageListUpdate(APIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def put(self, request, image_id):
        image = self.queryset.get(pk=image_id)
        name = request.data.get('name', None)
        if name is None:
            return Response(
                {'name': 'This field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        image.image.name = name
        image.processed = True
        image.save()
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
