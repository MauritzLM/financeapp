from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer
from knox.models import AuthToken

# user create
class UserCreate(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
        }, status=status.HTTP_201_CREATED)

