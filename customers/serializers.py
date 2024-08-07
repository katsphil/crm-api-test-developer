from rest_framework import serializers

from .models import Customer, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_admin']


class CustomerSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "surname",
            "photo",
            "photo_url",
            "created_by",
            "modified_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "modified_by", "created_at", "updated_at"]

    def get_photo_url(self, obj):
        return obj.get_photo_url()

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        validated_data["modified_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["modified_by"] = self.context["request"].user
        return super().update(instance, validated_data)
