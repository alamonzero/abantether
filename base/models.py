from django.db import models

#                                                                       MANAGERS
#----------------------------------------------------------------------------------------------

class SoftDeleteCustomManager(models.Manager):
    def get_queryset(self) -> models.query.QuerySet:
        return super().get_queryset().filter(is_deleted=False)




#                                                                        MODELS
#----------------------------------------------------------------------------------------------

class TimestampBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, null=False, db_index=True)
    custom_objects = SoftDeleteCustomManager()

    class Meta:
        abstract = True