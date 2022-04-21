from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from posts.models import PostModel
from posts.models import AnswerModel
from posts.serializers import PostSerializer
from posts.serializers import AnswerSerializer


class PostsView(GenericViewSet):
    model: PostModel = PostModel
    serializer_class: PostSerializer = PostSerializer
    permission_classes: tuple = (AllowAny,)

    @action(detail=False, methods=["post"])
    def search(self, request: Request) -> Response:
        """Filter posts by text"""

        required_fields: tuple = ("text", "count")

        validated_data: dict = self.serializer_class().validate(
            data=request.data, required_fields=required_fields
        )
        filters_data: dict = dict(
            text__icontains=validated_data.get("text", None),
            count=validated_data.get("count", 10),
        )

        queryset: QuerySet = self.model.filter(
            data=filters_data, order_field="-created_at"
        )

        return Response(
            self.serializer_class(queryset, many=True).data, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def by_thread(self, request: Request) -> Response:
        """Get post by thread_id"""

        required_fields: tuple = ("thread_id", "count")

        filters_data: dict = self.serializer_class().validate(
            data=request.data, required_fields=required_fields
        )

        queryset: QuerySet = self.model.filter_with_checking_exists(
            data=filters_data, order_field="-created_at"
        )

        return Response(
            self.serializer_class(queryset, many=True).data, status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def replies(self, request: Request) -> Response:
        """Get replies by post_id"""

        required_fields: tuple = ("post_id",)

        validated_data: dict = self.serializer_class().validate(
            data=request.data, required_fields=required_fields
        )

        filters_data: dict = dict(answer_id=validated_data["post_id"])

        queryset: QuerySet = AnswerModel.filter(data=filters_data, order_field="id")

        return Response(
            AnswerSerializer(queryset, many=True).data,
            status=status.HTTP_200_OK,
        )
