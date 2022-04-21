from scrapy import Item
from scrapy import Field


class ThreadItem(Item):
    name = Field()
    id = Field()


class PostItem(Item):
    id = Field()
    theme_id = Field()
    text = Field()
    author_name = Field()
    author_id = Field()
    created_at = Field()
    rating = Field()
    answered_posts_ids = Field()
    thread = Field()
    is_deleted = Field()
