from rest_framework import serializers

from authors.models import AuthorModel


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorModel
        fields = ("id", "name")
