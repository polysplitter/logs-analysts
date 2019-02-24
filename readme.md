


## What are the most popular three articles of all time? 

```
-- create a helper function to pass a parameter into a query.
create function path_params(param character)
    returns table (param character)
    as
    $body$
        select path from log where path like '%' || $1 || '%'
    $body$
    language sql

-- create a view to pull the total views.
create view article_views as
    select articles.slug, 
    ((select count(param) as views from path_params(articles.slug)) - COUNT(log.status)) + COUNT(log.status) as views 
    from articles
        join log
        on articles.slug = split_part(log.path, '/', 3)
        group by articles.slug
        order by views desc;

-- create a view to store the query.
create view most_popular_three_articles as
    select title, article_views.views from articles
        join article_views
        on articles.slug = article_views.slug
        order by article_views.views desc
        limit 3;

-- query for python.
select title, views from most_popular_three_articles;
```

## Who are the most popular article authors of all time?

```
-- create a view to join adjust tables for joining to authors.
create view author_to_articles as
    select author, title, article_views.views from articles
        join article_views
        on articles.slug = article_views.slug
        order by article_views.views desc;

-- create a view to join to authors.
create view most_popular_article_authors as
    select authors.name, sum(author_to_articles.views) as views from author_to_articles
        join authors
        on author_to_articles.author = authors.id
        group by authors.name
        order by views desc;

-- query used in python.
select name, views from most_popular_article_authors;
```

## On which days did more than 1% of requests lead to errors?

```
-- create a view to hold the none 200 http status.
create view good_views as
    select TO_CHAR(time, 'Month DD, YYYY') as day, count(status) as hits 
        from log 
        group by day 
        order by hits desc;

-- create a view to hold the none 200 http status.
create view bad_views as
    select TO_CHAR(time, 'Month DD, YYYY') as day, count(status) as hits 
        from log 
        where status != '200 OK' 
        group by day 
        order by hits desc;

-- create a view to store the query.
create view errors_greater_than_one_percent as
    select bad_views.day, 
        round(((bad_views.hits)::decimal / (good_views.hits)::decimal * 100), 2) as error_percent 
        from good_views
        join bad_views
        on good_views.day = bad_views.day
        where ((bad_views.hits)::decimal / (good_views.hits)::decimal * 100) > 1.0
        order by error_percent desc;

-- query used in python.
select day, error_percent from errors_greater_than_one_percent;
```


