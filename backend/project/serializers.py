from rest_framework import serializers

from project.models import (
    CustomFunctionalArea,
    Industry,
    Provider,
    Service,
    CustomService,
    BusinessCycle,
    CustomBusinessCycle,
    FunctionalArea,
    GeneratedRFP,
    SubmittedRFP,
)
from authentication.models import Organization


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class CustomServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomService
        fields = "__all__"
        extra_kwargs = {"organization_id": {"required": False, "allow_null": True}}


class BusinessCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCycle
        fields = "__all__"


class CustomBusinessCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomBusinessCycle
        fields = "__all__"
        extra_kwargs = {"organization_id": {"required": False, "allow_null": True}}


class FunctionalAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FunctionalArea
        fields = "__all__"
        extra_kwargs = {
            "organization": {"required": False, "allow_null": True},
        }


class CustomFunctionalAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomFunctionalArea
        fields = "__all__"
        extra_kwargs = {"organization_id": {"required": False, "allow_null": True}}


class GeneratedRFPSerializer(serializers.ModelSerializer):
    areas = FunctionalAreaSerializer(many=True)
    business_cycles = BusinessCycleSerializer(many=True)
    services = ServiceSerializer(many=True)

    area_ids = serializers.PrimaryKeyRelatedField(
        queryset=FunctionalArea.objects.all(),
        many=True,
        source="areas",
        write_only=True,
    )
    business_cycle_ids = serializers.PrimaryKeyRelatedField(
        queryset=BusinessCycle.objects.all(),
        many=True,
        source="business_cycles",
        write_only=True,
    )
    service_ids = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), many=True, source="services", write_only=True
    )

    class Meta:
        model = GeneratedRFP
        fields = "__all__"

    def validate(self, data):
        required_fields = [
            "value_propositions",
            "user",
            "industry",
            "services",
            "business_cycles",
            "areas",
        ]
        for field in required_fields:
            if field not in data:
                raise serializers.ValidationError({field: "This field is required."})
        return data


class SubmittedRFPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedRFP
        fields = "__all__"


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = "__all__"
