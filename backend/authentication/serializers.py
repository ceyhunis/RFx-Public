from authentication.models import Organization
from rest_framework import serializers

from authentication.models import Role, User


class UserSerializer(serializers.ModelSerializer):
    organization_name = serializers.SerializerMethodField()
    organization_id = serializers.IntegerField(read_only=True)
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), required=False, allow_null=True
    )
    role = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True, "required": False}}

    ALLOWED_FIELDS = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "organization",
        "value_propositions",
    ]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        role = validated_data.pop("role", None)

        filtered_data = {
            key: validated_data[key]
            for key in self.ALLOWED_FIELDS
            if key in validated_data
        }

        user = User.objects.create(**filtered_data)

        if password:
            user.set_password(password)
        if role:
            user.role = role

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        role = validated_data.pop("role", None)

        for field in self.ALLOWED_FIELDS:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        if password:
            instance.set_password(password)
        if role:
            instance.role = role

        instance.save()
        return instance

    def get_organization_name(self, obj):
        return getattr(obj.organization, "name", None)

    def get_organization_id(self, obj):
        return obj.organization.id if obj.organization else None


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "domain"]


class OrganizationMembersSerializer(serializers.ModelSerializer):
    business_cycles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "business_cycles"]

    def get_business_cycles(self, obj):
        return [cycle.name for cycle in obj.business_cycles.all()]
