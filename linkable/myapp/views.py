import pandas as pd
import numpy as np
from .models import Book, Recommend, MyUser,Cluster,MyCategory
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from .rankalgoritm import rank
from .gaugealgorithm import gauge
from .serializers import CreateUserSerializer, UserSerializer, BookSerializer, RecommendSerializer, ClusterSerializer, MyCategoriSerializer

id_data = pd.read_csv('../datafile/node.csv', header=None)
arr = np.load('../datafile/test.npy')


@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def select_book(request):
    try:
        book = Book.objects.get(node=request.GET["node"])
        user = request.user
        print(user)
    except Book.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        origin_recommend = Recommend.objects.get(username=user)
        if serializer.data['node'] in origin_recommend.books:
            return Response(serializer.data, headers={'exist': 'true'})
        return Response(serializer.data, headers={'exist': 'false'})

    elif request.method == 'POST':
        append_book = book.node
        origin_recommend = Recommend.objects.get(username=user)
        if append_book in origin_recommend.books:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        origin_recommend.books.append(append_book)
        recommend = Recommend(username=origin_recommend.username, books=origin_recommend.books)
        serializer = RecommendSerializer(recommend)
        serializer = RecommendSerializer(origin_recommend, data=serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        delete_book = book.node
        origin_recommend = Recommend.objects.get(username=user)
        if delete_book in origin_recommend.books:
            index=origin_recommend.books.index(delete_book)
            del origin_recommend.books[index]
            recommend = Recommend(username=origin_recommend.username, books=origin_recommend.books)
            serializer = RecommendSerializer(recommend)
            serializer = RecommendSerializer(origin_recommend, data=serializer.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def book_list(request):
    if request.method == 'GET':
        book_list=Book.objects.all()
        serializer = BookSerializer(book_list, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def book_list5(request):
    if request.method == 'GET':
        book_list = []
        for i in range(5):
            book=Book.objects.get(pk=i+1)
            book_list.append(book)
        serializer = BookSerializer(book_list, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def my_book(request):
    try:
        user = request.user
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET' and user is not None:
        mybook_serializer=RecommendSerializer(Recommend.objects.get(username=user))
        mybook = mybook_serializer.data.get('books')
        response_data=[]
        for i in mybook:
            print(i)
            response_data.append(Book.objects.get(node=i))

        response_serializer = BookSerializer(response_data,many=True)
        return Response(response_serializer.data)
    else:
        return Response(status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def recommend_book(request):
    try:
        user = request.user
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        tmp_list = []
        mybook_serializer = RecommendSerializer(Recommend.objects.get(username=user))
        mybook = mybook_serializer.data.get('books')
        print(mybook)
        r_value = rank(mybook,id_data,arr)
        print(r_value)
        for i in range(0, 10):
            tmp_list.append(Book.objects.get(pk=r_value[i]+1))
        serializer = BookSerializer(tmp_list, many=True)

        return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
def gauge_cluster(request):
    try:
        user = request.user
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        print(request.data.get("list"))
        rate_list=[]
        rate=request.data.get("list")
        tmp=rate.split(" ")
        print(tmp)
        for i in tmp:
            rate_list.append(int(i))

        tmp_list = []
        mycategory_serializer = MyCategoriSerializer(MyCategory.objects.get(username=user))
        mycategory = mycategory_serializer.data.get('category')
        r_value = gauge(mycategory,rate_list)
        for i in range(len(r_value)):
            tmp_list.append(Book.objects.get(pk=r_value[i]+1))
        print(tmp_list)
        serializer = BookSerializer(tmp_list, many=True)

        return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def user_info(request):
    try:
        user = request.user
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET' and user is not None:
        userinfo = MyUser.objects.get_by_natural_key(username=user)
        user_serializer = UserSerializer(userinfo)

        return Response(user_serializer.data)


@csrf_exempt
@api_view(['GET'])
def search(request):
    if request.method=='GET':
        pattern=request.GET["pattern"]
        result = Book.objects.filter(title__contains=pattern)
        print(result)
        serializer = BookSerializer(result, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def category_list(request):
    try:
        user = request.user
    except:
        Response(status=HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        a = Cluster.objects.all()
        serializer = ClusterSerializer(a, many=True)
        mycategory = MyCategory.objects.get(username=user)
        my=""
        for i in mycategory.category:
            my+=str(i+1)+" "
        return Response(serializer.data,headers={"list":my})


@csrf_exempt
@api_view(['GET'])
def category_book(request):
    if request.method == 'GET':
        category=request.GET['category']
        cluster = Cluster.objects.get(category=category)
        response_data=[]
        for i in cluster.cluster:
            book = Book.objects.get(id=i+1)
            response_data.append(book)

        serializer = BookSerializer(response_data, many=True)
        return Response(serializer.data)


@csrf_exempt
@api_view(['POST', 'DELETE'])
def category_user(request):
    try:
        user=request.user
    except:
        return Response(status=HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        idx=request.GET['category_id']
        origin_mycategory = MyCategory.objects.get(username=user)
        if idx in origin_mycategory.category:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        origin_mycategory.category.append(idx)
        mycategory = MyCategory(username=origin_mycategory.username, category=origin_mycategory.category)
        serializer = MyCategoriSerializer(mycategory)
        serializer = MyCategoriSerializer(origin_mycategory, data=serializer.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        delete_category = request.GET["category_id"]
        origin_category = MyCategory.objects.get(username=user)
        delete_category = int(delete_category)
        if delete_category in origin_category.category:
            index = origin_category.category.index(delete_category)
            del origin_category.category[index]
            category = MyCategory(username=origin_category.username, category=origin_category.category)
            serializer = MyCategoriSerializer(category)
            serializer = MyCategoriSerializer(origin_category, data=serializer.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=HTTP_200_OK)


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        if len(request.data["username"]) < 6 or len(request.data["password"]) < 4:
            body = {"message": "short field"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user1 = MyUser.objects.get_by_natural_key(username=request.data["username"])
        recommend = Recommend(username=user1)
        recommend.save()
        mycategory = MyCategory(username=user1)
        mycategory.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )
