#!/usr/bin/env python3

import psycopg2


class LogsAnalysis:
    @classmethod
    def most_popular_three_articles(cls):
        with psycopg2.connect("dbname=news") as connection:
            with connection.cursor() as cursor:
                cursor.execute('select title, views ' +
                               'from most_popular_three_articles;')
                user_data = cursor.fetchall()
                for i in user_data:
                    print("{} --- {} views".format(i[0], i[1]))

    @classmethod
    def most_popular_article_authors(cls):
        with psycopg2.connect("dbname=news") as connection:
            with connection.cursor() as cursor:
                cursor.execute('select name, views ' +
                               'from most_popular_article_authors;')
                user_data = cursor.fetchall()
                for i in user_data:
                    print("{} --- {} views".format(i[0], i[1]))

    @classmethod
    def errors_greater_than_one_percent(cls):
        with psycopg2.connect("dbname=news") as connection:
            with connection.cursor() as cursor:
                cursor.execute('select day, error_percent ' +
                               'from errors_greater_than_one_percent;')
                user_data = cursor.fetchall()
                for i in user_data:
                    print("{} --- {}% errors".format(i[0], i[1]))


print('What are the most popular three articles of all time?\n')
LogsAnalysis.most_popular_three_articles()

print('\nWho are the most popular article authors of all time?\n')
LogsAnalysis.most_popular_article_authors()

print('\nOn which days did more than 1% of requests lead to errors?\n')
LogsAnalysis.errors_greater_than_one_percent()
