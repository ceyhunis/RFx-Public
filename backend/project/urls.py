from django.urls import path

from .views import *

urlpatterns = [
    path("industry/", IndustryListCreateAPIView.as_view(), name="industry-list-create"),
    path("industry/<int:pk>/", IndustryDetailAPIView.as_view(), name="industry-detail"),
    path("service/", ServiceListCreateAPIView.as_view(), name="service-list-create"),
    path("service/<int:pk>/", ServiceDetailAPIView.as_view(), name="service-detail"),
    path(
        "custom-service/",
        CustomServiceListCreateAPIView.as_view(),
        name="custom-service-list-create",
    ),
    path(
        "custom-service/<int:pk>/",
        CustomServiceDetailAPIView.as_view(),
        name="custom-service-detail",
    ),
    path(
        "custom-service/<int:organization_id>/",
        CombinedServiceListCreateAPIView.as_view(),
        name="custom-service-detail",
    ),
    path(
        "business-cycle/",
        BusinessCycleListCreateAPIView.as_view(),
        name="business-cycle-list-create",
    ),
    path(
        "business-cycle/<int:pk>/",
        BusinessCycleDetailAPIView.as_view(),
        name="business-cycle-detail",
    ),
    path(
        "custom-business-cycle/",
        CustomBusinessCycleListCreateAPIView.as_view(),
        name="custom-business-cycle-list-create",
    ),
    path(
        "custom-business-cycle/<int:pk>/",
        CustomBusinessCycleDetailAPIView.as_view(),
        name="custom-business-cycle-detail",
    ),
    path(
        "custom-business-cycle/<int:organization_id>/",
        CombinedBusinessCycleListCreateAPIView.as_view(),
        name="custom-business-cycle-detail",
    ),
    path(
        "functional-area/",
        FunctionalAreaListCreateAPIView.as_view(),
        name="functional-area-list-create",
    ),
    path(
        "functional-area/<int:pk>/",
        FunctionalAreaDetailAPIView.as_view(),
        name="functional-area-detail",
    ),
    path(
        "custom-functional-area/",
        CustomFunctionalAreaListCreateAPIView.as_view(),
        name="custom-functional-area-list-create",
    ),
    path("bulk-actions/", BulkActionsAPIView.as_view(), name="bulk-actions"),
    path(
        "save-with-multi-data/",
        SaveWithMultiDataAPIView.as_view(),
        name="save-with-multi-data",
    ),
    path(
        "generated-rfp/", GeneratedRFPCreateView.as_view(), name="generatedrfp-create"
    ),
    path(
        "generated-rfp/<int:pk>/",  # Ensure the trailing slash is present
        GeneratedRFPDetailAPIView.as_view(),
        name="generatedrfp-detail",
    ),
    path(
        "submitted-rfp/", SubmittedRFPCreateView.as_view(), name="submittedrfp-create"
    ),
    path(
        "submitted-rfp/<int:pk>",
        SubmittedRFPCreateView.as_view(),
        name="submittedrfp-detail",
    ),
    path(
        "proposal/",
        SubmittedRFPListCreateAPIView.as_view(),
        name="submittedrfp-list-create",
    ),
    path(
        "proposal/<int:pk>/",
        SubmittedRFPDetailAPIView.as_view(),
        name="submittedrfp-detail",
    ),
    path("accept-proposal/", accept_proposal, name="accept-proposal"),
    path("reject-proposal/", reject_proposal, name="reject-proposal"),
    path("provider/", ProviderListCreateAPIView.as_view(), name="provider-list-create"),
    path("provider/<int:pk>/", ProviderDetailAPIView.as_view(), name="provider-detail"),
    path(
        "get-information-from-website/",
        GetInformationFromWebsiteAPIView.as_view(),
        name="get-information-from-website",
    ),
    path(
        "refactor-information/",
        RefactorInformationAPIView.as_view(),
        name="refactor-information",
    ),
    path("chat/", ChatAPIView.as_view(), name="chat"),
    path("send-proposal/", SendProposalAPIView.as_view(), name="send-proposal"),
    path("outseta-support/", OutsetaSupportAPIView.as_view(), name="outseta-support"),
    path("support-tickets/", SupportTicketsAPIView.as_view(), name="support-tickets"),
    path("dashboard/", DashboardAPIView.as_view(), name="dashboard"),
]
