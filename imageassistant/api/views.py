from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from images.models import Image
from images.serializers import ImageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class ImageListUpdate(APIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def put(self, request, image_id):
        image = self.queryset.get(pk=image_id)
        name = request.data.get('name', None)
        url = request.data.get('url', None)
        if name is None:
            return Response(
                {'name': 'This field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        image.image.name = name
        # since background removal process writes to another bucket, we need to update the alternate_url
        if url is not None:
            image.alternate_url = url
        image.processed = True
        image.save()
        serializer = ImageSerializer(image)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
# add allow any to allow any user to access this view
@permission_classes([AllowAny])
def test(request):
    try:
        value = int(request.GET.get("value", 0))
    except ValueError:
        return Response({"error": "Invalid value"}, status=status.HTTP_400_BAD_REQUEST)
    # Perform a lightweight computation
    squared = value ** 2
    result = {"original": value, "squared": squared, "message": f"Square of {value} is {squared}"}
    
    return Response(result, status=status.HTTP_200_OK)