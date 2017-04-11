# Students database management application

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

It allows you to track attendance of your students. Manage exams, add or edit students, groups, etc.

## Technical Stack

- Python 3.5.2, Django 1.10.5, PostgreSQL 
- Twitter Bootstrap 3.3.5, jQuery 2.1.1

## Installation

### Clone project

```sh
$ virtualenv stdb
$ source stdb/bin/activate
(stdb)$ git clone https://github.com/hddn/studentsdb.git
```

### Install requirements

```sh
(stdb)$ pip install -r requirements.txt
```

### Run application

```sh
(stdb)$ python manage.py makemigrations
(stdb)$ python manage.py migrate
(stdb)$ python manage.py createsuperuser
(stdb)$ python manage.py runserver
```

### Run tests

```sh
(stdb)$ python manage.py test students studentsdb
```

