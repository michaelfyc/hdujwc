# README

This project uses python to crawl Hangzhou Dianzi University's Administration Office and represents with Springboot and HTML. 

### Preparation:

In local database: create four tables: 'together'(汇总),'cxcy'（创新创业）,'jwgl'（教务管理）,'sj'（实践教育），which represents different sections of the Administration Office. 

For each database, create 4 fields: 

id (auto-increment,type:int,length:11), 

title(unique,type:varchar, length:255),

time(type:date, length:12), 

link(varchar, type:varchar,length:255).

That's where the name of class TTL comes from(Title, Time, Link).

In `crawler.py`, change `__db_url`,`__db_user`,`__db_password`,`__db_name` to the URL, user name,password and database name of your `MySQL`.   Configure the same thing in `application.yml` ,and in `SectionMapper.xml`, adapt **local** to your database name. 

Log file and its path also need configuration to adapt to your environment.
