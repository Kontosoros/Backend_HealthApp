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
from .load_models.load_ai_models import use_ai_diabetes , use_ai_heart_disease

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


class DiagnosticAPIView(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        age = body['age']
        pregnancies = body['pregnancies']
        glucose = body['glucose']
        bloodpressure = body['bloodpressure']
        skinthickness = body['skinthickness']
        insulin = body['insulin']
        bmi = body['bmi']
        diabetespedigree = body['diabetespedigree']
        sex = 1 if body['sex'] == 'male' else 0
        trtbps = body['trtbps']
        chol = body['chol']
        fbs = body['fbs']
        thalachh = body['thalachh']
        exng = body['exng']
        thall = body['thall']
        user_id = body['user']
        queryset = Diagnostic.objects.filter
        user_in_db = queryset(user_id=user_id)
        if user_in_db.exists():
            return Response({"user exist": True})
        else:
            diabetes_ai_result = use_ai_diabetes([[pregnancies,glucose,bloodpressure,skinthickness,insulin,bmi,diabetespedigree,age]])
            heart_ai_result = use_ai_heart_disease([[age,sex,trtbps,chol,fbs,thalachh,exng,thall]])
            # diagnostic_db = Diagnostic(
            #     age=age,
            #     pregnancies=pregnancies,
            #     glucose=glucose,
            #     bloodpressure=bloodpressure,
            #     skinthickness=skinthickness,
            #     insulin=insulin,
            #     bmi=bmi,
            #     diabetespedigree=diabetespedigree,
            #     sex=sex,
            #     trtbps=trtbps,
            #     chol=chol,
            #     fbs=fbs,
            #     thalachh=thalachh,
            #     exng=exng,
            #     thall=thall,
            #     user_id=user_id
            # )
            # diagnostic_db.save()
            return Response({"user not exist": True})


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
