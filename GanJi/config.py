# -*- coding: utf-8 -*-

BASE_URL = 'http://cd.ganji.com'

MYSQL_HOST = 'localhost'

MYSQL_PORT = 3306

MYSQL_USER = 'root'

MYSQL_PASSWORD = '123456'

MYSQL_DATABASE = 'ganjiDB'

NEXT_PAGE_NUM = 0





"""
-- 删除数据库
DROP DATABASE IF EXISTS ganjiDB;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS ganjiDB DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

USE ganjiDB;

-- 创建分类url表
CREATE TABLE types_url (
    id INT(11) NOT NULL AUTO_INCREMENT,
    url VARCHAR(2000) NOT NULL,
    typename VARCHAR(1000) NOT NULL,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建职位url表
CREATE TABLE jobs_url (
    id INT(11) NOT NULL AUTO_INCREMENT,
    url VARCHAR(2000) NOT NULL,
    jobname VARCHAR(1000) NOT NULL,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建职位信息表
CREATE TABLE jobs_info (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(1000) NOT NULL,
    salary VARCHAR(1000) NOT NULL,
    company VARCHAR(1000) NOT NULL,
    location VARCHAR(1000) NOT NULL,
    PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

"""