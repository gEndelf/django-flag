from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User

from flag.models import FlaggedContent


class ModelWithoutAuthor(models.Model):
    name = models.CharField(max_length=50)
    flagged = GenericRelation(FlaggedContent)

    def __unicode__(self):
        return self.name


class ModelWithAuthor(models.Model):
    name = models.CharField(max_length=50)
    author = models.ForeignKey(User)
    flagged = GenericRelation(FlaggedContent)

    def __unicode__(self):
        return self.name
