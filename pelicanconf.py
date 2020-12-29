#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Tony Spiker'
SITENAME = "Tony Spiker's home"
SITEURL = 'https://www.tonyspiker.com'

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
        
         ('You can modify those links in your config file', '#'),)

# Default page
DEFAULT_CATEGORY = 'category'
USE_FOLDER_AS_CATEGORY = True
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
PAGE_PATHS = ['pages', 'Code', 'category']
PELICAN_SOBER_HOME_LISTS_ARTICLES = False
DELETE_OUTPUT_DIRECTORY = True
RELATIVE_URLS = True
PLUGINS = ["render_math"]
PAGE_PATHS=['pages']
ARTICLE_PATHS = ['category']

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
