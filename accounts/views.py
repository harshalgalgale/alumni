# Create your views here.
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from accounts.serializers import UserSerializer, RegisterSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance
            return Response(data={"user_id": instance.id, "status": instance.is_active}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ConfirmRegistrationView(View):
#     def get(self, request, user_id, token):
#         user_id = force_text(urlsafe_base64_decode(user_id))
#
#         user = User.objects.get(pk=user_id)
#
#         context = {
#             'form': AuthenticationForm(),
#             'message': 'Registration confirmation error . Please click the reset password to generate a new confirmation email.'
#         }
#         if user and user_tokenizer.check_token(user, token):
#             user.is_valid = True
#             user.save()
#             context['message'] = 'Registration complete. Please login'
#
#         return render(request, 'survey/login.html', context)
