from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *
from .views import InviteRegistrationView

urlpatterns = [
    path("test/", TestView.as_view(), name="test"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("authenticate/", AuthenticateView.as_view(), name="authenticate"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("new-password/", NewPasswordView.as_view(), name="new-password"),
    path("user/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("user/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("role/", RoleListCreateAPIView.as_view(), name="role-list-create"),
    path("role/<int:pk>/", RoleDetailAPIView.as_view(), name="role-detail"),
    path(
        "organization/",
        OrganizationListCreateAPIView.as_view(),
        name="organization-list-create",
    ),
    path(
        "organization/<int:pk>/",
        OrganizationDetailAPIView.as_view(),
        name="organization-detail",
    ),
    path(
        "organization-members/",
        OrganizationMembersAPIView.as_view(),
        name="organization-members",
    ),
    path(
        "user-match-business-cycle/",
        UserMatchBusinessCycleAPIView.as_view(),
        name="user-match-business-cycle",
    ),
    path("get-people/", get_people, name="get-people"),
    path(
        "invite-member/",
        invite_member,  # Ensure this maps to the correct invite_member function
        name="invite-member",
    ),
    path(
        "validate-invitation/",
        validate_invitation_token,  # Ensure this maps to the correct validation function
        name="validate-invitation",
    ),
    path(
        "invite-register/",
        InviteRegistrationView.as_view(),
        name="invite-register",
    ),
]
