from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.utils import json
from .serializers import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .authentication import *
from django.utils import timezone


class Register(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["pass"]
        user = User.objects.filter(email=email).first()
        if user is None:
            raise APIException("Invalid Credentials")
        if not user.check_password(password):
            raise APIException("Invalid Credentials")
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        UserToken.objects.create(user_id=user.id, token=refresh_token, expired_at=datetime.datetime.utcnow() + datetime.timedelta(days=7))
        response = Response()
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)  # , samesite="none", secure=True)
        response.data = {"token": access_token, "refresh_token": refresh_token, "staff": user.is_staff}
        return response


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response(UsersSerializer(request.user).data)


class RefreshAPIView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        id = decode_refresh_token(refresh_token)
        if not UserToken.objects.filter(
            user_id=id, token=refresh_token, expired_at__gt=datetime.datetime.now(tz=timezone.utc)  # __gt shmainei grater than
        ).exists():
            raise exceptions.AuthenticationFailed("unauthenticated")
        access_token = create_access_token(id)
        return Response({"token": access_token})


@api_view(["POST"])
def user_registration(request):
    body = json.loads(request.body.decode("utf-8"))
    if request.method == "POST":
        name_req = body["name"]
        last_name_req = body["lastName"]
        email_req = body["email"]
        pass_req = body["password"]
        queryset = User.objects.filter
        check_name = queryset(username=name_req)
        if check_name.exists():
            return JsonResponse(-1, safe=False)
        else:
            user = User.objects.create_user(username=name_req, last_name=last_name_req, email=email_req, password=pass_req, name=name_req)
            user.save()
            return JsonResponse(user.id, safe=False)
