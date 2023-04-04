from rest_framework.decorators import APIView, api_view, permission_classes
from roboproject.serializers import PostSerializer, CommentSerializer
from roboproject.models import Post
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PostAPI(APIView):
    
    parser_class = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = PostSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status' : 'True','body': serializer.data}, status.HTTP_200_OK)
        else:
            return Response({'status' : 'False','body': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        if request.user.is_admin:
            data = request.data
            obj=Post.objects.get(id = data['id'])
            obj.delete()
            return Response({'status' : 'False','message': 'Post Deleted'}, status.HTTP_200_OK)
        else: 
            return Response({'status' : 'False','message': 'Pehli fursat mein nikal'}, status.HTTP_400_BAD_REQUEST)
            


@api_view(['GET'])    
def get_projects(request):
    objs = Post.objects.filter(is_verified = True)
    try:
        page = request.GET.get('page',1)
        page_size = 10
        paginator  = Paginator(objs, page_size)
        serializer = PostSerializer(paginator.page(page), many = True)
    except Exception as e:
        return Response({'status' : 'False','message': 'Empty Page'}, status.HTTP_400_BAD_REQUEST)
    
    return Response({'status' : 'True','body': serializer.data}, status.HTTP_200_OK)


@api_view(['POST'])
def post_comment(request, pk):
        data = request.data
        data= {"post": pk, "commentText" : data['commentText']}
        serializer = CommentSerializer(data=data)
        print("hello")
        if serializer.is_valid():
            serializer.save()
            return Response({'status' : 'True','body': serializer.data}, status.HTTP_200_OK)
        else:
            return Response({'status' : 'False','body': serializer.errors}, status.HTTP_400_BAD_REQUEST)
        
        
@api_view(['PUT'])
def react(request, pk, arg):
    obj=Post.objects.get(id = pk)
    num = obj.likes + 1 if arg == "likes" else obj.dislikes +1
    data= {arg : num}
    serializer = PostSerializer(obj, data= data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response({'status' : 'True','body': serializer.data}, status.HTTP_200_OK)
    else:
        return Response({'status' : 'False','body': serializer.errors}, status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def verify(request, pk):
    if request.user.is_admin:
        obj=Post.objects.get(id = pk)
        data= {"is_verified": True}
        serializer = PostSerializer(obj, data= data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status' : 'True','body': serializer.data}, status.HTTP_200_OK)
        else:
            return Response({'status' : 'False','body': serializer.errors}, status.HTTP_400_BAD_REQUEST)
    else: 
        return Response({'status' : 'False','message': 'Admin bnja phle'}, status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unverified(request):
    if request.user.is_admin:
        objs = Post.objects.filter(is_verified =False)
        serializer = PostSerializer(objs, many = True)
        return Response({'status' : 'True','body': serializer.data}, status.HTTP_200_OK)
    else: 
        return Response({'status' : 'False','message': 'Pehli fursat mein nikal'}, status.HTTP_401_UNAUTHORIZED)