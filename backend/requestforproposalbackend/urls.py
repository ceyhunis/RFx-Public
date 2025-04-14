from django.urls import path, include
from .views import *  # Tüm view'ları içe aktarır
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# -----------------------------------------------------------------------------
# API Documentation
# -----------------------------------------------------------------------------
API_DOCUMENTATION_PATTERNS = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

# -----------------------------------------------------------------------------
# CRM / People Management
# -----------------------------------------------------------------------------
PEOPLE_PATTERNS = [
    path("crm/people/add/", add_person_view, name="add_person"),
    path("crm/people/", get_all_people_view, name="get_all_people"),
    path(
        "crm/people/<str:person_uid>/",
        get_person_with_uid_view,
        name="get_person_with_uid",
    ),
    path(
        "crm/people/<str:person_uid>/update/", update_person_view, name="update_person"
    ),
    path(
        "crm/people/<str:person_uid>/delete/", delete_person_view, name="delete_person"
    ),
    path(
        "crm/people/<str:person_uid>/set-temporary-password/",
        set_temporary_password_view,
        name="set_temporary_password",
    ),
    path(
        "crm/people/forgotPassword/",
        initiate_password_reset_view,
        name="initiate_password_reset",
    ),
]

# -----------------------------------------------------------------------------
# CRM / Account Management
# -----------------------------------------------------------------------------
ACCOUNT_PATTERNS = [
    path("crm/accounts/<str:account_uid>/", account_detail_view, name="account_detail"),
    path("crm/accounts/", accounts_view, name="accounts"),
    path(
        "crm/accounts/<str:account_uid>/memberships/",
        add_membership_view,
        name="add_membership",
    ),
    path(
        "crm/accounts/<str:account_uid>/memberships/<str:membership_uid>/",
        update_person_account_membership_view,
        name="update_membership",
    ),
    path(
        "crm/accounts/<str:account_uid>/update/",
        update_account_view,
        name="update_account",
    ),
    path(
        "crm/accounts/cancellation/<str:account_uid>/",
        cancel_account_view,
        name="cancel_account",
    ),
    path(
        "crm/accounts/removecancellation/<str:account_uid>/",
        remove_cancellation_view,
        name="remove_cancellation",
    ),
    path(
        "crm/accounts/<str:account_uid>/memberships/<str:membership_uid>/",
        remove_person_from_account_view,
        name="remove_person_from_account",
    ),
    path(
        "crm/accounts/<str:account_uid>/send-confirmation-email/",
        send_confirmation_email_view,
        name="send_confirmation_email",
    ),
    # New endpoint for trial extension
    path(
        "crm/accounts/extendtrial/<str:account_uid>/<str:trial_end_date>/",
        extend_trial_view,
        name="extend_trial",
    ),
]

# -----------------------------------------------------------------------------
# CRM / Activity Management
# -----------------------------------------------------------------------------
ACTIVITY_PATTERNS = [
    path("crm/activities/", get_activities_view, name="get_activities"),
    path(
        "crm/activities/customactivity/",
        add_custom_activity_view,
        name="add_custom_activity",
    ),
]

# -----------------------------------------------------------------------------
# CRM / Deal Management
# -----------------------------------------------------------------------------
DEAL_PATTERNS = [
    path("crm/deals/", deals_view, name="deals"),
    path("crm/deals/<str:deal_uid>/", deal_detail_view, name="deal_detail"),
]

# -----------------------------------------------------------------------------
# Support Management
# -----------------------------------------------------------------------------
SUPPORT_PATTERNS = [
    path("support/cases/", get_all_cases_view, name="get_all_cases"),
    path("support/cases/person/", get_cases_by_person_view, name="get_cases_by_person"),
    path("support/cases/", add_case_view, name="add_case"),
    path(
        "support/cases/<str:case_uid>/response/",
        add_client_response_view,
        name="add_client_response",
    ),
    path(
        "support/cases/<str:case_uid>/reply/",
        add_agent_reply_view,
        name="add_agent_reply",
    ),
]

# -----------------------------------------------------------------------------
# Marketing Management
# -----------------------------------------------------------------------------
MARKETING_PATTERNS = [
    path(
        "marketing/lists/<str:list_id>/subscribers/",
        get_list_subscribers_view,
        name="get_list_subscribers",
    ),
    path(
        "marketing/lists/<str:list_id>/subscribe/new/",
        subscribe_new_person_view,
        name="subscribe_new_person",
    ),
    path(
        "marketing/lists/<str:list_id>/subscribe/existing/",
        subscribe_existing_person_view,
        name="subscribe_existing_person",
    ),
    path(
        "marketing/lists/<str:list_id>/subscriptions/<str:subscription_uid>/",
        remove_subscriber_view,
        name="remove_subscriber",
    ),
]

# -----------------------------------------------------------------------------
# Billing Management
# -----------------------------------------------------------------------------
BILLING_PATTERNS = [
    path(
        "billing/planfamilies/",
        get_all_plan_families_view,
        name="get_all_plan_families",
    ),
    path("billing/plans/", get_all_plans_view, name="get_all_plans"),
    path("billing/usage/", add_usage_for_addon_view, name="add_usage_for_addon"),
    path(
        "billing/discountcoupons/", add_discount_coupon_view, name="add_discount_coupon"
    ),
    path(
        "billing/subscriptions/<str:subscription_uid>/",
        get_subscription_view,
        name="get_subscription",
    ),
    path(
        "billing/subscriptions/compute-charge-summary/",
        compute_charge_summary_view,
        name="compute_charge_summary",
    ),
    path(
        "billing/subscriptions/firsttimesubscription/",
        add_first_time_subscription_view,
        name="add_first_time_subscription",
    ),
    path(
        "billing/subscriptions/<str:subscription_uid>/changesubscriptionpreview/",
        change_subscription_preview_view,
        name="change_subscription_preview",
    ),
    path(
        "billing/subscriptions/<str:subscription_uid>/changesubscription/",
        change_subscription_view,
        name="change_subscription",
    ),
    path(
        "billing/subscriptions/<str:subscription_uid>/setsubscriptionupgraderequired/",
        set_subscription_upgrade_required_view,
        name="set_subscription_upgrade_required",
    ),
    path(
        "billing/subscriptionaddons/",
        add_addon_to_subscription_view,
        name="add_addon_to_subscription",
    ),
    path(
        "billing/subscriptions/<str:subscription_uid>/discounts/<str:discount_uid>/",
        add_discount_to_subscription_view,
        name="add_discount_to_subscription",
    ),
    path("billing/invoices/", add_new_invoice_view, name="add_new_invoice"),
    path(
        "billing/transactions/<str:account_uid>/",
        get_transactions_by_account_view,
        name="get_transactions_by_account",
    ),
    path(
        "billing/transactions/payment/",
        add_invoice_payment_view,
        name="add_invoice_payment",
    ),
    path(
        "billing/paymentinformation/",
        update_payment_information_view,
        name="update_payment_information",
    ),
]

# -----------------------------------------------------------------------------
# User Profile Management
# -----------------------------------------------------------------------------
USER_PROFILE_PATTERNS = [
    path("profile/", get_user_profile_view, name="get_user_profile"),
    path("profile/update/", update_user_profile_view, name="update_user_profile"),
    path("profile/password/", update_user_password_view, name="update_user_password"),
]

# -----------------------------------------------------------------------------
# Authentication Management
# -----------------------------------------------------------------------------
AUTHENTICATION_PATTERNS = [
    path("tokens/", get_auth_token_view, name="get_auth_token"),
    path(
        "tokens/api-key/",
        get_auth_token_with_api_keys_view,
        name="get_auth_token_with_api_keys",
    ),
]

# -----------------------------------------------------------------------------
# Combines all URLs together with Project and Authentication URLs
# -----------------------------------------------------------------------------
urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("project/", include("project.urls")),
    *API_DOCUMENTATION_PATTERNS,
    *PEOPLE_PATTERNS,
    *ACCOUNT_PATTERNS,
    *ACTIVITY_PATTERNS,
    *DEAL_PATTERNS,
    *SUPPORT_PATTERNS,
    *MARKETING_PATTERNS,
    *BILLING_PATTERNS,
    *USER_PROFILE_PATTERNS,
    *AUTHENTICATION_PATTERNS,  # Added authentication patterns
]
