from django.conf import settings
from django.db import models
from requestforproposalbackend.base_model import BaseModel


class Industry(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=100, blank=True, null=True)


class Service(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()


class CustomService(BaseModel):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization_id = models.ForeignKey(
        "authentication.Organization", on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField()


class BusinessCycle(BaseModel):
    order = models.IntegerField(default=1)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class CustomBusinessCycle(BaseModel):
    order = models.IntegerField(default=1)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization_id = models.ForeignKey(
        "authentication.Organization", on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class FunctionalArea(BaseModel):
    business_cycle_id = models.ForeignKey(BusinessCycle, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    name = models.CharField(max_length=180)
    description = models.TextField()


class CustomFunctionalArea(BaseModel):
    business_cycle_id = models.ForeignKey(BusinessCycle, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    name = models.CharField(max_length=180)
    description = models.TextField()
    organization = models.ForeignKey(
        "authentication.Organization", on_delete=models.CASCADE, null=True, blank=True
    )


class GeneratedRFP(BaseModel):
    status = models.CharField(
        max_length=100, default="in-progress", null=True, blank=True
    )
    start_date = models.DateField(auto_now_add=True, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    rfp_name = models.CharField(max_length=100)
    rfp_description = models.TextField()
    company_url = models.CharField(max_length=100, blank=True, null=True)
    value_propositions = models.CharField(max_length=260)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)
    questionnaires = models.JSONField(default=list)
    business_cycles = models.ManyToManyField(BusinessCycle)
    areas = models.ManyToManyField(FunctionalArea)
    descriptions = models.JSONField(default=list)


class SubmittedRFP(BaseModel):
    rfp_id = models.IntegerField()
    user_id = models.IntegerField()
    status = models.CharField(
        max_length=100, default="in-progress", null=True, blank=True
    )
    last_login_to_rfp = models.DateField(auto_now_add=True, blank=True, null=True)
    last_login_ip_address = models.CharField(max_length=100, blank=True, null=True)
    pdf_link = models.CharField(max_length=10000, blank=True, null=True)
    is_opened = models.BooleanField(default=False)
    recived_person = models.CharField(max_length=100)
    recived_person_email = models.CharField(max_length=100)


class Provider(BaseModel):
    company_name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=100)
    contact_email = models.CharField(max_length=100)


class FunctionalAreaEmbedding(models.Model):
    area_name = models.CharField(max_length=255)
    text = models.TextField()
    embedding = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class ResponseRFP(BaseModel):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    rfp = models.ForeignKey(GeneratedRFP, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    submitted_rfp = models.ForeignKey(SubmittedRFP, on_delete=models.CASCADE)
    completed_fields = models.JSONField(default=list)
    response_fields = models.JSONField(default=list)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    status = models.CharField(
        max_length=100, default="in-progress", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectFunctionalAreaSession(BaseModel):
    session_id = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    functional_area = models.ForeignKey(FunctionalArea, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
