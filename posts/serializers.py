from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException

from authors.serializers import AuthorSerializer
from posts.models import PostModel
from posts.models import AnswerModel
from posts.models import ThreadModel


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadModel
        fields = ("id", "name")


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = ("post_id",)


class PostSerializer(FlexFieldsModelSerializer):
    author = AuthorSerializer(default={})
    thread = ThreadSerializer(default={})
    answers = AnswerSerializer(default=[], many=True)

    def validate(self, data: dict, required_fields: tuple = ()) -> dict:

        try:
            return {key: data[key] for key in required_fields}
        except KeyError:
            raise APIException(f"No one or more fields from required {required_fields}")

    class Meta:
        model = PostModel
        fields = (
            "id",
            "url",
            "thread",
            "text",
            "author",
            "created_at",
            "rating",
            "answers",
        )
