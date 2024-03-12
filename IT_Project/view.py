from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def about_us(request):
    try:
        with open('path/to/your/static/about_us.txt', 'r') as file:  # Open text file
            content = file.read()  # read content
        return Response(content, content_type='text/plain')  # content type set to plain text
    except Exception as e:
        return Response({'error': str(e)}, status=500)   # error message with status code 500
