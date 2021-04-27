# from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

from accounts.models import User
from alumni import settings
from members.models import PersonalProfile
from students.models import Student


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


def create_member_profile(user, first_name, last_name):
    PersonalProfile.objects.create(first_name=first_name, last_name=last_name, user=user)


class RegisterSerializer(Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, validators=[validate_password])
    reg_no = serializers.CharField()
    pass_degree = serializers.CharField()
    pass_year = serializers.CharField()

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "User with email already exists."})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        reg_no = validated_data.pop('reg_no')
        pass_degree = validated_data.pop('pass_degree')
        pass_year = validated_data.pop('pass_year')
        passed_student = Student.objects.filter(
            reg_no=reg_no,
            degree=pass_degree,
            pass_year=pass_year
        )

        personal_profile = PersonalProfile.objects.filter(student__in=passed_student)
        if personal_profile.exists():
            raise ValidationError("Personal Profile for Student Details already exist.")

        user = User.objects.create(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])

        if passed_student.exists():
            user.is_active = True
            token = 'token'
            # token = user_tokenizer.make_token(user)
            user_id = urlsafe_base64_encode(force_bytes(user.id))
            url = 'http://localhost:8000' + reverse('confirm_email', kwargs={'user_id': user_id, 'token': token})
            mail_subject = 'Activate your account.'
            # current_site = get_current_site(request)

            message = render_to_string('accounts/verify_email.html', {
                'user': user,
                # 'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
                'token': token,
                # 'token': account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email],
                from_email=settings.EMAIL_HOST_USER
            )
            email.send()

            create_member_profile(user, first_name, last_name, passed_student.first())
        else:
            user.is_active = False
            mail_subject = 'Validation in progress'
            message = render_to_string('accounts/verify_inprogress_email.html', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email],
                from_email=settings.EMAIL_HOST_USER
            )
            email.send()
            send_mail('subject',
                      'Validation in progress. Once validated we will send you email to verify your details.',
                      'sender@example.com', [user.email, ])
        user.save()

        return user
