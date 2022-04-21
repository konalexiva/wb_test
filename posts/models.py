from django.db import models
from django.db.models import QuerySet
from django.http import Http404

from authors.models import AuthorModel


class ThreadModel(models.Model):

    name = models.CharField(max_length=255, blank=True)


class PostModel(models.Model):

    rating = models.IntegerField(default=0)
    thread = models.ForeignKey(ThreadModel, on_delete=models.CASCADE)
    author = models.ForeignKey(AuthorModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True)
    text = models.TextField(blank=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def url(self) -> str:
        """get url by id of post"""

        return f"http://forum.mfd.ru/forum/post/?id={self.id}"

    @classmethod
    def filter(cls, data: dict, order_field: str):
        """filter posts"""

        try:
            count: int = data.pop("count")
        except KeyError:
            count = 10

        return (
            cls.objects.select_related("thread", "author")
            .filter(**data)
            .order_by(order_field)[:count]
        )

    @classmethod
    def filter_with_checking_exists(cls, data: dict, order_field: str):
        """filter posts and check that result queryset is not empty"""

        queryset: QuerySet = cls.filter(data=data, order_field=order_field)

        if not queryset.exists():
            raise Http404
        return queryset


class AnswerModel(models.Model):

    post_id = models.IntegerField(db_index=True)
    answer_id = models.IntegerField(db_index=True)

    @classmethod
    def filter(cls, data: dict, order_field: str):
        """filter posts"""

        return cls.objects.filter(**data).only("post_id").order_by(order_field)
