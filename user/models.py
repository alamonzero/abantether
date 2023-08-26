from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

from user.utils.validators import NationalCodeValidator
from base.models import TimestampBaseModel, SoftDeleteModel, SoftDeleteCustomManager


class UserCustomManager(SoftDeleteCustomManager):
    def get_queryset(self) -> models.query.QuerySet:
        return super().get_queryset().prefetch_related("accounts", "addresses")


class UserManager(BaseUserManager):
    def create_user(self, mobile_number, password, **extra_fields):
        if not mobile_number:
            raise ValueError(_("The mobile number must be set"))
        mobile_number = mobile_number
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(mobile_number, password, **extra_fields)


class User(AbstractBaseUser, TimestampBaseModel, SoftDeleteModel):
    mobile_number = models.CharField(
        max_length=13,
        db_index=True,
        unique=True,
        null=False,
        blank=False,
        validators=(MinLengthValidator(11),),
    )
    first_name = models.CharField(max_length=128, null=False, blank=True, default="")
    last_name = models.CharField(max_length=128, null=False, blank=True, default="")
    national_code = models.CharField(
        max_length=10,
        db_index=True,
        null=False,
        blank=False,
        validators=(NationalCodeValidator,),
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    custome_object = UserCustomManager()

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []


class UserAddressCustomManager(SoftDeleteCustomManager):
    def get_queryset(self) -> models.query.QuerySet:
        return super().get_queryset().select_related("user")


class UserAddress(TimestampBaseModel, SoftDeleteModel):
    province = models.CharField(max_length=128, null=False, blank=False)
    city_title = models.CharField(max_length=128, null=False, blank=False)
    address = models.CharField(max_length=1024, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="addresses")
    custom_objects = UserAddressCustomManager()
