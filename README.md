# Project description

This project was built during the course: *Data Engineering nanodegree (udacity)*.

The objective of this project is to apply concepts of data modeling in relational databases for data analysis purposes.

An etl was implemented to process data from a set of files and insert it into a postgres database that uses a star schema.

# Sparkify Context

Sparkify is a fantasy music streaming startup that collects music and user activity data from your app. The data analysis team does not have access to an organized structure to make analyzes such as: what are the most listened to songs? In this context arises this data engineering project with the objective of providing this structure for the data analysis team.

# Files

* **create_table.py**: drops and creates tables on sparkifydb.
* **etl.py**: reads and processes files from *song_data* and *log_data* and loads them into sparkifydb.
* **analytic_queries_test.ipynb**: example queries and results for song play analysis.
* **sql_queries.py**: contains all sql queries used in other files.
* **test.ipynb**: a jupyter notebook used to check sparkifydb.
* **etl.ipynb**: this script contains the instructions that were used for the development of *etl.py*.

# Running python scripts

To run this project it is necessary to have a postgres application running on localhost and python 3 installed. Then you can run the following commands:

    ```
    python3 create_tables.py
    python3 etl.py
    ```

# Database schema

The database schema chosen for this project was the star schema. It is a very popular schema for data analysis purposes. It is a denormalized schema that has the following advantages for the Sparkify startup context:

* Simple queries: needs less join logic than normalized schemas.
* Fast aggregations: because of the simpler queries the performance in aggregations is better.
* High performance for read-only purposes.

The main disadvantage of this scheme is the lack of flexibility for specific queries, which is possible in normalized databases.

# Tables description

## Fact table

* **songplays**: records in log data associated with song plays.

## Dimension tabels

* **users**: app users info.
* **songs**: songs info.
* **artists**: artists info.
* **time**: timestamps of records in songplays broken down into specific time units (hour, day, week, month, year, weekday).

# Analytical queries examples

1. What are the most listened to songs?
    ```
    SELECT sp."song_id", s."title", a."name", count(*) AS "total_song_plays" FROM songplays sp
    LEFT JOIN songs s ON s."song_id" = sp."song_id"
    LEFT JOIN artists a ON s."artist_id" = a."artist_id"
    GROUP BY sp."song_id", s."title", a."name"
    ORDER BY "total_song_plays" DESC
    LIMIT 10
    ```

2. What are the most listened to artists?
    ```
    SELECT a."artist_id", a."name", count(*) AS "total_artist_plays" FROM songplays sp
    LEFT JOIN artists a ON sp."artist_id" = a."artist_id"
    GROUP BY a."artist_id", a."name"
    ORDER BY "total_artist_plays" DESC
    LIMIT 10
    ```

3. On which day of the week do users listen to music the most?
    ```
    SELECT "weekday", count(*) FROM songplays sp
    JOIN time t ON t."start_time" = sp."start_time"
    GROUP BY "weekday"
    ORDER BY "weekday" DESC
    LIMIT 10
    ```