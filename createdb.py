#! /usr/bin/env python
import sqlite3

connect=sqlite3.connect("IIITMK.db")
cursor=connect.cursor()

cursor.execute('create table IIITMKLogin(id integer primary key not null, username varchar(15),password varchar(15),account_type integer)')
cursor.execute('create table UserDetails(id integer primary key not null,username varchar(15),fullname varchar(15),email varchar(15),account_type varchar(15),designation varchar(15),age integer,batch varchar(15),profilepic BLOB)')


cursor.execute('create table OpinionPoll(id integer primary key not null ,topic TEXT,content TEXT,posted_on DATETIME,for_vote integer,against_vote integer)')


connect.commit()
cursor.close()
