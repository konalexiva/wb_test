import json
import os
from django.core.management import BaseCommand
from dateutil.parser import parse

from authors.models import AuthorModel
from posts.models import AnswerModel
from posts.models import PostModel
from posts.models import ThreadModel


class Command(BaseCommand):
    help: str = "import parsed data"

    def handle(self, *args, **options):
        parsed_data_file = open(os.environ.get("PARSED_DATA_PATH"))

        parsed_posts_data: list = json.load(parsed_data_file)
        # parsed_posts_data: list = sorted(parsed_posts_data, key = lambda post: post["id"])

        def __create_post(data: dict) -> PostModel:
            post: PostModel = PostModel(
                id=data["id"],
                created_at=parse(data["created_at"]),
                text=data["text"],
                rating=data["rating"],
                is_deleted=data["is_deleted"],
                author_id=AuthorModel.objects.get_or_create(
                    id=data["author_id"], name=data["author_name"]
                )[0].id,
                thread_id=ThreadModel.objects.get_or_create(
                    id=data["thread"]["id"], name=data["thread"]["name"]
                )[0].id,
            )

            if data["answered_posts_ids"]:
                AnswerModel.objects.bulk_create(
                    [
                        AnswerModel(post_id=data["id"], answer_id=answer_id)
                        for answer_id in data["answered_posts_ids"]
                    ],
                    batch_size=25,
                )

            return post

        PostModel.objects.bulk_create(
            [__create_post(post) for post in parsed_posts_data],
            batch_size=100,
        )

        parsed_data_file.close()
