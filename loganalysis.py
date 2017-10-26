# !/usr/bin/env python
#
# Log Analysis Project -
# Find the view counts for articles and authors
# Display the days with more than 1% error requests

import calendar
import psycopg2
from flask import Flask, request, redirect, url_for
app = Flask(__name__)


def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("error message")


def search_results(db, c):
    # Finds the view count for the top 3 articles
    query_1 = (
        "select articles.title, count(*) from log join articles "
        "on log.path = concat('/article/',articles.slug) "
        "group by articles.title "
        "order by count(*) desc "
        "limit 3;"
    )

    # Finds the view count for each author
    query_2 = (
        "select authors.name, count(*) "
        "from ((log join articles on log.path = "
        "concat('/article/',articles.slug)) "
        "join authors on articles.author = authors.id) "
        "group by authors.id "
        "order by count(*) desc;"
    )

    # Finds the days with more than 1% of requests that lead to errors
    query_3 = (
        "With good as (select cast(time as date), count(*) "
        "from log group by cast(time as date)), "
        "bad as (select cast(time as date), count(*) "
        "from log where status like '%404%' group by cast(time as date)) "
        "select bad.time, "
        "(cast(bad.count as float)/cast(good.count as float)*100) "
        "as Percentage "
        "from bad, good where bad.time = good.time "
        "and (cast(bad.count as float)/cast(good.count as float)*100) >= 1 "
        "order by "
        "(cast(bad.count as float)/cast(good.count as float)*100) desc;"
    )

    c.execute(query_1)

    # Displays the results for article view count
    print("Most popular three articles of all time")
    for a in c:
        print("\"" + str(a[0]) + "\" -- " + str(a[1]) + " views")
    print("\n")

    c.execute(query_2)

    # Displays the results for author view count
    print("Most popular article authors of all time")
    for a in c:
        print(str(a[0]) + " -- " + str(a[1]) + " views")
    print("\n")

    c.execute(query_3)

    # Displays the results for the days with more than 1% errors
    print("Days with more than 1% request errors")
    for a in c:
        problem_date = str(a[0]).split("-")
        print(
            calendar.month_name[int(problem_date[1])] + " " +
            problem_date[2]+", "+problem_date[0] + " -- " +
            str("{0:.2f}".format(a[1])) +
            "% errors"
        )
    print("\n")

    db.close()


db_data = connect()
search_results(db_data[0], db_data[1])
