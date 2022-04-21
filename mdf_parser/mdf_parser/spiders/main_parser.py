from typing import List
from scrapy import Spider
from scrapy import Request
from mdf_parser.items import ThreadItem
from mdf_parser.items import PostItem
from w3lib.html import remove_tags


class MfdSpider(Spider):

    name: str = "mfd_spider"
    base_url: str = "http://forum.mfd.ru"
    start_urls = ["http://forum.mfd.ru/forum/subforum/?id=649"]

    def parse_posts_page(self, response):
        """Parsing of one post's page"""

        __posts_path: str = (
            "//div[@class='mfd-post' or @class='mfd-post mfd-post-deleted']"
        )
        __author_id_path: str = "div[@class='mfd-post-top']/div[@class='mfd-post-top-0']/a[@class='mfd-poster-link']/@title"
        __anonymous_author_id_path: str = "div[@class='mfd-post-top']/div[@class='mfd-post-top-0']/a[@class='mfd-anonymous-link']/@title"
        __author_name_path: str = "div[@class='mfd-post-top']/div[@class='mfd-post-top-0']/a[@class='mfd-poster-link']"
        __anonymous_author_name_path: str = "div[@class='mfd-post-top']/div[@class='mfd-post-top-0']/a[@class='mfd-anonymous-link']/text()"
        __created_at_path: str = "div[@class='mfd-post-top']/div[@class='mfd-post-top-1']/a[@class='mfd-post-link']/text()"
        __is_deleted_path: str = "table//div[@class='mfd-post-remark']/text()"
        __id_path: str = "table//button[@class='mfd-button-attention']/@data-id"
        __rating_path: str = (
            "div[@class='mfd-post-top']/div[@class='mfd-post-top-2']/span/text()"
        )
        __answered_posts_ids_path: str = "table//div[@class='mfd-post-text']/blockquote/div[@class='mfd-quote-info']/a[2]/@href"

        __text_path: str = (
            "table//div[@class='mfd-post-text']/div[@class='mfd-quote-text']"
        )

        for post in response.xpath(__posts_path):
            post_item: PostItem = PostItem()

            __is_deleted_value = post.xpath(__is_deleted_path).get()
            __rating_value = post.xpath(__rating_path).get()
            __text_value = post.xpath(__text_path).get()

            post_item["id"] = post.xpath(__id_path).get()

            if post_item["id"] is None:
                continue

            try:
                post_item["author_name"] = remove_tags(
                    post.xpath(__author_name_path).get()
                )
            except Exception:
                post_item["author_name"] = post.xpath(
                    __anonymous_author_name_path
                ).get()

            try:
                post_item["author_id"] = (
                    post.xpath(__author_id_path).get().rpartition("ID: ")[2]
                )
            except Exception:
                post_item["author_id"] = (
                    post.xpath(__anonymous_author_id_path).get().rpartition("ID: ")[2]
                )

            post_item["created_at"] = post.xpath(__created_at_path).get()

            post_item["is_deleted"] = (
                __is_deleted_value is not None and "удалено" in __is_deleted_value
            )

            try:
                post_item["rating"] = (
                    int(__rating_value) if __rating_value != "\xa0" else 0
                )
            except Exception:
                post_item["rating"] = 0

            post_item["answered_posts_ids"] = [
                i.rpartition("id=")[2]
                for i in post.xpath(__answered_posts_ids_path).getall()
            ]

            post_item["text"] = (
                remove_tags(__text_value.replace("<br>", "\n"))
                if __text_value is not None
                else ""
            )

            post_item["thread"] = response.meta["thread_item"]
            yield post_item

    def parse_posts_pages(self, response):
        """Parsing of posts pages"""

        __current_posts_pages_count_path: str = (
            "//a[@class='mfd-paginator-selected']/text()"
        )

        current_posts_pages_count: int = int(
            response.xpath(__current_posts_pages_count_path).get()
        )

        __current_page_num: int = 0

        while __current_page_num < current_posts_pages_count:

            yield Request(
                url=f"{self.base_url}/forum/thread/?id={response.meta['thread_item']['id']}&page={__current_page_num}",
                callback=self.parse_posts_page,
                meta={
                    "thread_item": response.meta["thread_item"],
                },
            )
            __current_page_num += 1

    def parse_threads_page(self, response):
        """Parsing of one threads page"""

        __threads_urls_path: str = "//td[@class='mfd-item-subject']/a[1]"

        for thread_url in response.xpath(__threads_urls_path):
            thread_item_url: str = thread_url.css("a").attrib["href"].rpartition("&")[0]

            thread_item: ThreadItem = ThreadItem()
            thread_item["id"] = thread_item_url.rpartition("id=")[2]
            thread_item["name"] = thread_url.css("a::text").get()

            yield Request(
                url=f"{self.base_url}{thread_item_url}",
                callback=self.parse_posts_pages,
                meta={
                    "thread_item": thread_item,
                },
            )

    def parse(self, response):
        """Parsing of threads pages"""

        __next_page_url_path: str = "//div[@class='mfd-paginator']/a/text()"

        next_page_url: int = int(response.xpath(__next_page_url_path)[-1].get())

        __current_page_num = 0
        while __current_page_num < next_page_url:
            yield Request(
                response.urljoin(f"{self.start_urls[0]}&page={__current_page_num}"),
                callback=self.parse_threads_page,
            )
            __current_page_num += 1
