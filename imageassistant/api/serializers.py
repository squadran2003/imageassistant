from images.models import Service
from rest_framework import serializers
from users.models import CustomUser, Credit
import re


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    credits = serializers.SerializerMethodField()
    feature_flags = serializers.SerializerMethodField()
    def get_credits(self, obj):
        return Credit.objects.filter(user=obj)[0].total if Credit.objects.filter(user=obj).exists() else 0

    def get_feature_flags(self, obj):
        return obj.featureflag_set.values_list('name', flat=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'credits', 'feature_flags')

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    subject = serializers.CharField(max_length=200, required=True)
    message = serializers.CharField(required=True)
    confirmHuman = serializers.BooleanField(required=True)

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required")
        if re.match(r"[^@]+@[^@]+\.[^@]+", value) is None:
            raise serializers.ValidationError("Email is invalid")
        return value

    def validate_message(self, value):
        if not value or len(value) < 50:
            raise serializers.ValidationError("Message is too short; messages must be at least 50 characters.")
        return value

    def validate_confirmHuman(self, value):
        if not value:
            raise serializers.ValidationError("Please confirm you are not a robot.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        # check if the email is a google email
        if value.endswith('@gmail.com'):
            raise serializers.ValidationError("Google accounts cannot reset password via this method.")
        return value
