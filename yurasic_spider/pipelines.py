# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

authors_file = '/home/dima/PycharmProjects/yurasic_spider/authors.txt'

import sys
sys.path += "main-package"

from yurasic_spider.models import models


class YurasicSpiderPipeline(object):
    def __init__(self):
        import os
        import psycopg2
        import urllib.parse

        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "../../yurasic.settings")

        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.authors = set()
        self.songs = set()
        # self.cur = self.conn.cursor()
        # self.inserts = 0

    def process_item(self, item, spider):
        author = item['author']
        if author not in self.authors:
            self.authors.add(author)
            author_object = models.Author(name=author)
            author_object.save()
        else:
            # todo if database is not empty
            author_object = models.Author.objects.first(name=author)

        title = item['title']
        song_object = models.Song(title=title)
        song_object.authors.add(author_object)
        song_object.save()

        content = item['content']
        realization_object = models.Realization(content=content)
        realization_object.song = song_object
        realization_object.save()

        return item


        # def insert_item(self, table_name, item):
        #     # print_item(item)
        #     keys = item.keys()
        #     data = [item[k] for k in keys]  # make a list of each key
        #     instr = 'INSERT INTO {table} ({keys}) VALUES ({placeholders});'.format(
        #         # Assemble query string
        #         table=table_name,  # table to insert into, provided as method's argument
        #         keys=", ".join(keys),  # iterate through keys, seperated by comma
        #         placeholders=", ".join("%s" for d in data)  # create a %s for each key
        #     )
        #     self.cur.execute(instr, data)  # Combine the instructions and data
        #     self.conn.commit()
        #     # log.msg("Successfully inserted \"%s - %s\" into database." % (
        #     #     item['artist'], item['songtitle']), level=log.DEBUG)
        #     #     print
        #     # "Successfully inserted \"%s: %s - %s\" into database table \"%s\"." % (
        #     # item['playid'], item['artist'], item['songtitle'], self.databaseTable)
        #
        #     self.inserts += 1
