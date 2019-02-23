

problem 1:
What are the most popular three articles of all time? 

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

-- query used in python
select title, article_views.views from articles
    join article_views
    on articles.slug = article_views.slug
    order by article_views.views desc;
```

problem 2:
Who are the most popular article authors of all time?

```
-- create a view ...
create view author_to_articles as
    select author, title, article_views.views from articles
        join article_views
        on articles.slug = article_views.slug
        order by article_views.views desc;

-- query used in python.
select authors.name, sum(author_to_articles.views) as views from author_to_articles
    join authors
    on author_to_articles.author = authors.id
    group by authors.name
    order by views desc;
```

problem 3:
On which days did more than 1% of requests lead to errors?

```
-- create a view ...
create view good_views as
    select TO_CHAR(time, 'YYYY-MM_DD') as day, count(status) as hits 
        from log 
        group by day 
        order by hits desc

-- create a view ...
create view bad_views as
    select TO_CHAR(time, 'YYYY-MM_DD') as day, count(status) as hits 
        from log 
        where status != '200 OK' 
        group by day 
        order by hits desc

-- query used in python.
select bad_views.day, 
    ((bad_views.hits)::decimal / (good_views.hits)::decimal * 100) as views 
    from good_views
    join bad_views
    on good_views.day = bad_views.day
    order by views desc;

```


