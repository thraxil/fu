from django.db import models

class Author(models.Model):
    """
    name
    slug
    bio
    """

class Issue(models.Model):
    """
    date
    status
    """

class Article(models.Model):
    """
    title
    slug
    lede
    issue
    author
    content
    """


