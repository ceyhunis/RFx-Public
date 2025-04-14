from django.contrib.auth.models import AbstractUser
from django.db import models
from requestforproposalbackend.base_model import BaseModel
from project.models import BusinessCycle
from datetime import datetime, timedelta
from django.utils import timezone


class Organization(BaseModel):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100, default="none")


class Role(BaseModel):
    name = models.CharField(max_length=100)
    is_super_role = models.BooleanField(default=False)


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    value_propositions = models.CharField(default="system", max_length=100)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )
    user_uid_outseta = models.CharField(max_length=100, null=True, blank=True)


class PasswordResetToken(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)


class UserMatchBusinessCycle(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_cycles = models.ManyToManyField(BusinessCycle)


class Invite(BaseModel):
    inviter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_invites"
    )
    email = models.EmailField()
    hashed_token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        """Check if the invitation is still valid (active and not expired)"""
        return self.is_active and self.expires_at > timezone.now()

    def deactivate(self):
        """Mark invitation as inactive"""
        self.is_active = False
        self.save()
