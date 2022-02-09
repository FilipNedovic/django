from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from todos.models import User, Todo
from todos.serializers import UserSerializer, TodoSerializer
from rest_framework import mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render



class HomeView(APIView):
    def home(request):
        template = loader.get_template('index.html')
        return HttpResponse(template.render(), status=status.HTTP_200_OK)



class UserViewSet(mixins.ListModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class UserViewDetail(mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]
    permission_classes = [IsAdminUser]

    def get(self, request, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        return render(request, 'user.html', {'user': user})

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request):
        serializer = self.serializer_class(request.user)

        return Response(status=status.HTTP_200_OK)

    def put(request):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(request.user, data=serializer_data, partial=True)
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)



class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterUsersAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = [JSONRenderer]

    def get(self, request):
        term = request.GET.get('name', '')
        users = User.objects.filter(first_name=term)
        if users:
            return HttpResponse(users, status=status.HTTP_200_OK)
        else:
            users = User.objects.filter(last_name=term)
            if users:
                return HttpResponse(users, status=status.HTTP_200_OK)
            else:
                return HttpResponse('no user found', status=status.HTTP_404_NOT_FOUND)



class TodoViewSet(mixins.ListModelMixin, GenericAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)



class TodoViewDetail(mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.CreateModelMixin, 
                    mixins.DestroyModelMixin, 
                    GenericAPIView):

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
