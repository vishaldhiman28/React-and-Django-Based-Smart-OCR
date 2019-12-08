from django.shortcuts import render
from django.http import HttpResponse
from .serializers import PostSerializer
from .models import Post
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .main_processor  import *
import os,glob
class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def get(self, request, *args, **kwargs):
        
        text_data=''
        date_info=''
        fn=''

        path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/media/post_images/"
        for filename in os.listdir(path):
            fn=os.path.join(path, filename)
            text_data,date_info=process_image(fn)
        
        data={}
        data["imageText"]=text_data
        data["dateInfo"]=date_info

        posts = Post.objects.all()
        posts.delete()
        
        path=path+"*"
        list_of_f=glob.glob(path)
        for i in list_of_f:
            os.remove(i)
      
        return Response(data,status=status.HTTP_200_OK)

       
    def post(self, request, *args, **kwargs):
        posts_serializer = PostSerializer(data=request.data)
        print(request.data['image'])
        if posts_serializer.is_valid():
            posts_serializer.save()
            return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', posts_serializer.errors)
            return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

