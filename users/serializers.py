from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):

        user = UserModel.objects.create(
            nickname=validated_data['nickname'],
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            group_number=validated_data['group_number'],
            course=validated_data['course'],
            is_student=True
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ( "id", "nickname", "password", "full_name", "email", "group_number", "course")