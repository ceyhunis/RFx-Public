# Django imports
from django.contrib.auth import authenticate as authentication_email
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from django.utils import timezone

# Rest Framework imports
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

# Third party imports
from drf_spectacular.utils import extend_schema
import requests
import logging

# Local imports
from authentication.models import *
from authentication.serializers import *
from requestforproposalbackend.api_response import api_response
from requestforproposalbackend.services.email_js import EmailJSService
from requestforproposalbackend.services.outseta import OutsetaService
import random
import string


def generate_random_token(length=16):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


class TestView(APIView):
    def get(self, request):
        data = {"message": "API works"}
        return Response(data=data, status=200)


@extend_schema(tags=["Authentication"])
class AuthenticateView(APIView):
    def post(self, request):
        try:
            print("Received data:", request.data)
            email = request.data["email"]
            password = request.data["password"]
            user = authentication_email(username=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                user = User.objects.get(pk=user.id)
                user.last_login = timezone.now()
                user.save()

                user_data = {
                    "outseta_uid": user.user_uid_outseta,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "role": user.role.name if user.role else None,
                    "role_id": user.role.id if user.role else None,
                    "organization_id": (
                        user.organization.id if user.organization else None
                    ),
                    "super_admin": user.is_superuser,
                }
                response = api_response(
                    [user_data],
                    "success",
                    message="Successfully Login",
                    status_code=200,
                )
                return Response(response, status=200)

            else:
                response = api_response(
                    None, "error", "Invalid username or password", 401
                )
                return Response(response, status=401)

        except KeyError:
            response = api_response(
                None, "error", "Email and password are required", 400
            )
            return Response(response, status=400)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


@extend_schema(tags=["Authentication"])
class SignUpView(APIView):
    def post(self, request):
        try:
            email = request.data["email"]
            password = request.data["password"]
            first_name = request.data["first_name"]
            last_name = request.data["last_name"]

            if User.objects.filter(email=email).exists():
                response = api_response(None, "error", "Email already exists", 400)
                return Response(response, status=400)

            email_domain = email.split("@")[1]
            check_organization = Organization.objects.filter(
                domain=email_domain
            ).first()
            if not check_organization:
                new_organization = Organization.objects.create(
                    domain=email_domain, name=email_domain.upper()
                )

            get_organization = (
                check_organization if check_organization else new_organization
            )

            role = Role.objects.get(name="USER")

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_superuser=False,
                organization=get_organization,
                role=role,
            )

            user_data = {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "role": user.role.name,
                "role_id": user.role.id,
                "super_admin": False,
            }
            email_service = EmailJSService()
            email_service.send_welcome_email(user.email, user.first_name.capitalize())

            # Prepare data for Outseta
            outseta_person_data = {
                "Email": user.email,
                "FirstName": user.first_name,
                "LastName": user.last_name,
                "MailingAddress": {
                    "AddressLine1": "new line",
                    "AddressLine2": "new line2",
                    "AddressLine3": None,
                    "City": "City",
                    "State": "State",

                    "PostalCode": "02446",
                },
            }

            outseta_service = OutsetaService()
            crm_service = outseta_service.CRMService()
            created_person = crm_service.add_person(outseta_person_data)
            user.user_uid_outseta = created_person.get("Uid")
            user.save()
            subscription_service = outseta_service.MarketingService()

            subscription_service.add_new_subscriber(
                list_id="y9qOl8mA",
                person_data={
                    "Email": user.email,
                    "FirstName": user.first_name,
                    "LastName": user.last_name,
                },
                send_welcome_email=True,
            )


            response = api_response(
                [user_data],
                "success",
                message="Successfully Registered",
                status_code=201,
            )
            return Response(response, status=201)

        except KeyError:
            response = api_response(None, "error", "All fields are required", 400)
            return Response(response, status=400)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)


@extend_schema(tags=["Authentication"])
class ResetPasswordView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            token = generate_random_token()
            user = User.objects.get(email=email)
            PasswordResetToken.objects.create(
                user=user, token=token, expires_at=timezone.now() + timedelta(days=1)
            )
            email_service = EmailJSService()
            email_service.send_forget_password_email(user.first_name, token, email)
            return Response(
                api_response(None, "success", "Password reset email sent", 200),
                status=200,
            )
        except Exception as e:
            return Response(
                api_response(None, "error", f"An error occurred: {str(e)}", 500),
                status=500,
            )


@extend_schema(tags=["Authentication"])
class NewPasswordView(APIView):
    def post(self, request):
        try:
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")
            if new_password != confirm_password:
                return Response(
                    api_response(None, "error", "Passwords do not match", 400),
                    status=400,
                )
            token = request.data.get("token")
            email = request.data.get("email")
            user = User.objects.get(email=email)

            reset_token = PasswordResetToken.objects.get(user=user, token=token)

            if reset_token.is_used:
                return Response(
                    api_response(None, "error", "Token already used", 400), status=400
                )
            if reset_token.expires_at < timezone.now():
                return Response(
                    api_response(None, "error", "Token expired", 400), status=400
                )
            if not PasswordResetToken.objects.filter(
                user=user, token=token, expires_at__gt=timezone.now()
            ).exists():
                return Response(
                    api_response(None, "error", "Invalid or expired token", 400),
                    status=400,
                )
            user.set_password(new_password)
            reset_token.is_used = True
            reset_token.save()
            user.save()
            return Response(
                api_response(None, "success", "Password updated successfully", 200),
                status=200,
            )
        except Exception as e:
            return Response(
                api_response(None, "error", f"An error occurred: {str(e)}", 500),
                status=500,
            )


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            query_params = request.query_params
            if query_params:
                users = User.objects.filter(**query_params)
                serializer = UserSerializer(users, many=True)
                response = api_response(
                    serializer.data,
                    "success",
                    message="Users retrieved successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                response = api_response(
                    serializer.data,
                    "success",
                    message="All users retrieved successfully",
                    status_code=200,
                )
                return Response(response, status=200)

        except ValidationError as ve:
            response = api_response(None, "error", f"Validation error: {ve}", 400)
            return Response(response, status=400)
        except Exception as e:
            response = api_response(
                None,
                "error",
                f"Unexpected error: {str(e)}",
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            user_data = request.data.copy()

            if "role" in user_data and user_data["role"]:
                try:
                    user_data["role"] = int(user_data["role"])
                except (ValueError, TypeError):
                    return Response(
                        api_response(None, "error", "Invalid role ID format", 400),
                        status=400,
                    )
            role = Role.objects.get(id=user_data["role"])
            if role.is_super_role:
                user_data["is_superuser"] = True
            else:
                user_data["is_superuser"] = False

            user_data["username"] = user_data["email"]

            serializer = self.get_serializer(data=user_data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    "User created successfully",
                    status.HTTP_201_CREATED,
                )
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    api_response(None, "error", serializer.errors, 400), status=400
                )

        except Exception as e:
            print(f"Error creating user: {str(e)}")
            return Response(api_response(None, "error", str(e), 500), status=500)


class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs["pk"])
            serializer = UserSerializer(user)
            response = api_response(
                [serializer.data],
                "success",
                message="User retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)

        except User.DoesNotExist:
            response = api_response(None, "error", "User not found", 404)
            return Response(response, status=404)

        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs["pk"])
            user_data = request.data.copy()

            if "role" in user_data and user_data["role"]:
                try:
                    user_data["role"] = int(user_data["role"])
                except (ValueError, TypeError):
                    return Response(
                        api_response(None, "error", "Invalid role ID format", 400),
                        status=400,
                    )
            role = Role.objects.get(id=user_data["role"])
            if role.is_super_role:
                user_data["is_superuser"] = True
            else:
                user_data["is_superuser"] = False

            if "organization" in user_data and user_data["organization"]:
                try:
                    user_data["organization"] = int(user_data["organization"])
                except (ValueError, TypeError):
                    return Response(
                        api_response(
                            None, "error", "Invalid organization ID format", 400
                        ),
                        status=400,
                    )

            if "password" in user_data and not user_data["password"]:
                user_data.pop("password")

            serializer = UserSerializer(user, data=user_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    [serializer.data],
                    "success",
                    message="User updated successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 400)
                return Response(response, status=400)

        except User.DoesNotExist:
            response = api_response(None, "error", "User not found", 404)
            return Response(response, status=404)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs["pk"])
            user.delete()
            response = api_response(
                None, "success", message="User deleted successfully", status_code=200
            )
            return Response(response, status=200)

        except Exception as e:
            response = api_response(None, "error", f"An error occured:{str(e)}", 500)
            return Response(response, status=500)
        pass

    @extend_schema(exclude=True)
    def patch(self, request, *args, **kwargs):
        pass


class RoleListCreateAPIView(ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get(self, request, *args, **kwargs):
        try:
            roles = Role.objects.all()
            serializer = RoleSerializer(roles, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Roles retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)

        except Exception as e:
            response = api_response(None, "error", f"An error occured:{str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = RoleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Role created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)

        except Exception as e:
            response = api_response(None, "error", f"An error occured:{str(e)}", 500)
            return Response(response, status=500)


class RoleDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get(self, request, *args, **kwargs):
        try:
            role = Role.objects.get(pk=kwargs["pk"])
            serializer = RoleSerializer(role)
            response = api_response(
                [serializer.data],
                "success",
                message="Role retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)

        except Exception as e:
            response = api_response(None, "error", f"An error occured:{str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            role = Role.objects.get(pk=kwargs["pk"])
            serializer = RoleSerializer(role, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    [serializer.data],
                    "success",
                    message="Role updated successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)

        except Exception as e:
            response = api_response(None, "error", f"An error occured:{str(e)}", 500)
            return Response(response, status=500)
        pass

    def delete(self, request, *args, **kwargs):
        try:
            role = Role.objects.get(pk=kwargs["pk"])
            role.delete()
            response = api_response(
                None, "success", message="Role deleted successfully", status_code=200
            )
            return Response(response, status=200)

        except Exception as e:
            response = api_response(None, "error", f"An error occured:{str(e)}", 500)
            return Response(response, status=500)

    @extend_schema(exclude=True)
    def patch(self, request, *args, **kwargs):
        pass


class OrganizationListCreateAPIView(ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        try:
            # Prefetch related business cycles to optimize query
            organizations = Organization.objects.all()
            serializer = OrganizationSerializer(organizations, many=True)
            response = api_response(
                serializer.data,
                "success",
                message="Organizations retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            response = api_response(None, "error", f"An error occurred: {str(e)}", 500)
            return Response(response, status=500)

    def post(self, request, *args, **kwargs):
        try:
            serializer = OrganizationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    serializer.data,
                    "success",
                    message="Organization created successfully",
                    status_code=200,
                )
                return Response(response, status=200)
            else:
                response = api_response(None, "error", serializer.errors, 500)
                return Response(response, status=500)

        except Exception as e:
            response = api_response(None, "error", f"An error occured:{str(e)}", 500)
            return Response(response, status=500)


class OrganizationDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        try:
            organization = Organization.objects.get(pk=kwargs["pk"])
            serializer = OrganizationSerializer(organization)
            response = api_response(
                [serializer.data], "success", "Organization retrieved successfully", 200
            )
            return Response(response, status=200)

        except Exception as e:
            response = api_response(None, "error", f"An error occured:{str(e)}", 500)
            return Response(response, status=500)

    def put(self, request, *args, **kwargs):
        try:
            organization = Organization.objects.get(pk=kwargs["pk"])
            serializer = OrganizationSerializer(organization, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = api_response(
                    [serializer.data],
                    "success",
                    "Organization updated successfully",
                    200,
                )
                return Response(response, status=200)

        except Exception as e:
            response = api_response(None, "error", f"An error occured:{str(e)}", 500)
            return Response(response, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            organization = Organization.objects.get(pk=kwargs["pk"])
            if organization.user_set.exists():
                return Response(
                    api_response(
                        None,
                        "error",
                        "This organization has users. Please delete the users first.",
                        400,
                    ),
                    status=400,
                )
            organization.delete()
            return Response(
                api_response(None, "success", "Organization deleted successfully", 200),
                status=200,
            )
        except Organization.DoesNotExist:
            return Response(
                api_response(None, "error", "Organization not found", 404), status=404
            )
        except Exception as e:
            print(f"Organization deletion error: {str(e)}")
            return Response(
                api_response(None, "error", f"An error occurred: {str(e)}", 500),
                status=500,
            )


class OrganizationMembersAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            user_id = request.GET.get(
                "user_id"
            )  # URL parametresi yerine query parametresi
            if not user_id:
                return Response(
                    api_response(None, "error", "User ID is required", 400), status=400
                )

            user = User.objects.get(pk=user_id)
            organization = Organization.objects.get(pk=user.organization.id)
            members = User.objects.filter(organization=organization).exclude(id=user_id)

            def get_member_data(member):
                business_cycles = UserMatchBusinessCycle.objects.filter(
                    user=member
                ).values_list("business_cycles__name", flat=True)
                member_data = UserSerializer(member).data
                member_data["business_cycles"] = list(business_cycles)
                return member_data

            members_data = list(map(get_member_data, members))

            response = api_response(
                {"members": members_data},
                "success",
                message="Members retrieved successfully",
                status_code=200,
            )
            return Response(response, status=200)
        except Exception as e:
            return Response(
                api_response(None, "error", f"An error occurred: {str(e)}", 500),
                status=500,
            )


class UserMatchBusinessCycleAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")
            business_cycle_ids = request.data.get("business_cycle_ids")

            # Retrieve the UserMatchBusinessCycle instance for the user or create a new one
            user_match, created = UserMatchBusinessCycle.objects.get_or_create(
                user_id=user_id
            )

            if business_cycle_ids is None:
                # Remove all business cycles if business_cycle_ids is null
                user_match.business_cycles.clear()
            else:
                # Update the business cycles for the user
                user_match.business_cycles.set(business_cycle_ids)

            user_match.save()

            return Response(
                api_response(
                    None, "success", "User matched to business cycles successfully", 200
                ),
                status=200,
            )
        except Exception as e:
            return Response(
                api_response(None, "error", f"An error occurred: {str(e)}", 500),
                status=500,
            )


logger = logging.getLogger(__name__)


@api_view(["GET"])
def get_people(request):
    try:
        crm_service = OutsetaService.CRMService()
        people_data = crm_service.get_all_people()

        if people_data is not None:
            return Response(people_data, status=status.HTTP_200_OK)
        else:
            logger.error("Outseta API returned no data or response is invalid")
            return Response(
                {"error": "No data received from Outseta API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except requests.exceptions.RequestException as e:
        logger.exception(f"Request error while fetching people: {str(e)}")
        return Response(
            {"error": "Failed to connect to Outseta API", "details": str(e)},
            status=status.HTTP_502_BAD_GATEWAY,
        )
    except Exception as e:
        logger.exception(f"Unexpected error fetching people: {str(e)}")
        return Response(
            {"error": "An unexpected error occurred", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def invite_member(request):
    email = request.data.get("email")
    user_id = request.data.get("user_id")

    # Generate tokens
    invitation_token = generate_random_token(32)
    hashed_token = make_password(invitation_token)

    print("------------------------TOKEN GENERATION------------------------")
    print(f"Generated plain text token (for validation): {invitation_token}")
    print(f"Hashed token (for URL): {hashed_token}")

    expires_at = timezone.now() + timedelta(hours=24)

    try:
        requesting_user = User.objects.get(pk=user_id)
        organization = requesting_user.organization

        # Create invitation record
        invite = Invite.objects.create(
            inviter_id=user_id,
            email=email,
            hashed_token=hashed_token,
            expires_at=expires_at,
        )

        # Send email with hashed token
        email_success = False
        try:
            email_service = EmailJSService()
            organization_name = organization.name if organization else "Our Platform"
            inviter_name = f"{requesting_user.first_name} {requesting_user.last_name}"

            email_response = email_service.send_invitation_email(
                email,
                organization_name,
                inviter_name,
                hashed_token,  # Send hashed token for URL
            )
            email_success = email_response is not None
            print(f"Email sent with hashed token: {email_success}")
        except Exception as email_error:
            print(f"Error sending invitation email: {str(email_error)}")

        return Response(
            api_response(
                {
                    "email": email,
                    "invitation_id": invite.id,
                    "expires_at": expires_at,
                    "email_sent": email_success,
                    "hashed_token": hashed_token,  # Always return hashed token
                    "requested_by": {
                        "user_id": user_id,
                        "username": requesting_user.username,
                        "name": f"{requesting_user.first_name} {requesting_user.last_name}",
                    },
                },
                "success",
                message=f"Invitation sent to {email}. Valid for 24 hours.",
                status_code=200,
            ),
            status=200,
        )
    except User.DoesNotExist:
        print(f"Requesting user not found: {user_id}")
        return Response(
            api_response(
                {"email": email},
                "error",
                "Requesting user not found",
                status_code=404,
            ),
            status=404,
        )
    except Exception as e:
        print(f"Error creating invitation: {str(e)}")
        return Response(
            api_response(
                {"email": email},
                "error",
                f"Error creating invitation: {str(e)}",
                status_code=500,
            ),
            status=500,
        )


logger = logging.getLogger(__name__)


@api_view(["POST"])
def validate_invitation_token(request):
    try:
        print("------------------------TOKEN VALIDATION------------------------")
        token = request.data.get("token")
        email = request.data.get("email")
        print(f"Received plain text token: {token}")
        print(f"Validating for email: {email}")

        if not token:
            print("No token provided in request")
            return Response(
                api_response(None, "error", "Token is required", 400),
                status=400,
            )

        # Find active invites by email and expiry
        invitation = Invite.objects.filter(
            email=email, is_active=True, expires_at__gt=timezone.now()
        ).first()

        print(f"Found invitation record: {invitation}")
        if invitation:
            print(f"Stored hashed token: {invitation.hashed_token}")
            if check_password(token, invitation.hashed_token):
                print("Token validation successful")
                return Response(
                    api_response(
                        {
                            "valid": True,
                            "organization_id": invitation.inviter.organization.id,
                            "organization_name": invitation.inviter.organization.name,
                            "inviter_name": f"{invitation.inviter.first_name} {invitation.inviter.last_name}",
                            "expires_at": invitation.expires_at,
                            "invite_id": invitation.id,
                        },
                        "success",
                        "Token is valid",
                        200,
                    ),
                    status=200,
                )
            else:
                print("Token validation failed - hash mismatch")
                print(f"Received token: {token}")
                print(f"Stored hash: {invitation.hashed_token}")
        else:
            print("No valid invitation found for token validation")

        return Response(
            api_response({"valid": False}, "error", "Invalid or expired token", 404),
            status=404,
        )

    except Exception as e:
        print(f"Token validation error: {str(e)}")
        return Response(
            api_response(None, "error", f"Error validating token: {str(e)}", 500),
            status=500,
        )


@extend_schema(tags=["Authentication"])
class InviteRegistrationView(APIView):
    @transaction.atomic
    def post(self, request):
        try:
            print("------------------------REGISTRATION------------------------")
            token = request.data.get("token")
            registration_email = request.data.get("email")  # Email for new user
            invitation_email = request.data.get(
                "invitation_email"
            )  # Email from invitation

            print(f"Registration request details:")
            print(f"- Token: {token}")
            print(f"- Registration Email: {registration_email}")
            print(f"- Invitation Email: {invitation_email}")

            if not token or not invitation_email:
                print("Missing required data:")
                print(f"- Token present: {'Yes' if token else 'No'}")
                print(
                    f"- Invitation email present: {'Yes' if invitation_email else 'No'}"
                )
                return Response(
                    api_response(
                        None, "error", "Missing required registration data", 400
                    ),
                    status=400,
                )

            # Find invitation using the invitation email
            invitation = Invite.objects.filter(
                email=invitation_email, is_active=True, expires_at__gt=timezone.now()
            ).first()

            print(f"Invitation lookup results:")
            print(f"- Found invitation: {'Yes' if invitation else 'No'}")
            if invitation:
                print(f"- Invitation details:")
                print(f"  * ID: {invitation.id}")
                print(f"  * Email: {invitation.email}")
                print(f"  * Active: {invitation.is_active}")
                print(f"  * Expires: {invitation.expires_at}")
            else:
                all_invites = Invite.objects.all()
                print(f"- Active invitations in system:")
                for inv in all_invites:
                    print(
                        f"  * ID: {inv.id}, Email: {inv.email}, Active: {inv.is_active}, Expires: {inv.expires_at}"
                    )

            if not invitation:
                print("No valid invitation found - returning error")
                return Response(
                    api_response(None, "error", "Invalid or expired invitation", 400),
                    status=400,
                )

            print(f"Token validation:")
            print(f"- Received token: {token}")
            print(f"- Stored hash: {invitation.hashed_token}")

            if not check_password(token, invitation.hashed_token):
                print("Token validation failed - hash mismatch")
                return Response(
                    api_response(None, "error", "Invalid token", 400),
                    status=400,
                )

            print("Token validation successful")

            # Create user with registration email
            user_data = request.data.copy()
            user_data["organization"] = invitation.inviter.organization.id
            user_data["role"] = Role.objects.get(name="USER").id
            user_data["username"] = registration_email
            user_data["email"] = registration_email

            print(f"Creating user with data:")
            print(f"- Username/Email: {registration_email}")
            print(f"- Organization ID: {user_data['organization']}")
            print(f"- Role: USER")

            # Create the user
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                user = serializer.save()
                print(f"User created successfully: {user}")

                # Mark the token as used
                invitation.is_active = False
                invitation.save()
                print(f"Invitation marked as used: {invitation}")

                response = api_response(
                    serializer.data,
                    "success",
                    "User registered successfully",
                    status.HTTP_201_CREATED,
                )
                print(f"Response data: {response}")
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                print(f"User registration failed. Errors: {serializer.errors}")
                return Response(
                    api_response(None, "error", serializer.errors, 400), status=400
                )
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            return Response(
                api_response(None, "error", f"An error occurred: {str(e)}", 500),
                status=500,
            )
