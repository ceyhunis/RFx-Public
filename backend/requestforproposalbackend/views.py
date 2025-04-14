from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .services.outseta import OutsetaService

# Define common messages
ERROR_MESSAGES = {
    "api_error": {"error": "Outseta API call failed."},
    "not_found": {"error": "Resource not found."},
    "invalid_params": {"error": "Required parameters are missing."},
    "temporary_password": {"error": "Temporary password not provided."},
    "subscription_error": {"error": "Subscription operation failed."},
}

SUCCESS_MESSAGES = {
    "temp_password_set": {"message": "Temporary password set successfully."},
    "email_sent": {"message": "Confirmation email sent successfully."},
    "default": {"message": "Operation completed successfully."},
    "subscription_added": {"message": "Subscription added successfully."},
    "subscription_removed": {"message": "Subscription removed successfully."},
}


class ResponseBuilder:
    """Helper class to build consistent API responses.

    This class provides static methods to return success and error responses.
    """

    @staticmethod
    def error(
        message=ERROR_MESSAGES["api_error"],
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        """Builds an error response.

        Args:
            message (dict, optional): Error message dictionary. Defaults to API error.
            status_code (int, optional): HTTP status code. Defaults to 500.

        Returns:
            Response: DRF Response with error message and status code.
        """
        return Response(message, status=status_code)

    @staticmethod
    def success(data=None, status_code=status.HTTP_200_OK):
        """Builds a success response.

        Args:
            data (dict, optional): Data payload for success. Defaults to a default success message.
            status_code (int, optional): HTTP status code. Defaults to 200.

        Returns:
            Response: DRF Response with data and status code.
        """
        if data is None:
            data = SUCCESS_MESSAGES["default"]
        return Response(data, status=status_code)


##################################################################################################################
# ---------------------------CRM VIEWS--------------------------------
##################################################################################################################


# ------------------------------------------ People


@api_view(["GET"])
def get_all_people_view(request):
    """Retrieve all people from Outseta CRM API.

    Returns:
        Response: API response containing all people data, or an error if none found.
    """
    crm_service = OutsetaService.CRMService()
    people_data = crm_service.get_all_people()
    return (
        ResponseBuilder.success(people_data) if people_data else ResponseBuilder.error()
    )


@api_view(["GET"])
def get_person_with_uid_view(request, person_uid):
    """Retrieve a person by UID from Outseta CRM API.

    Args:
        person_uid (str): Unique identifier for the person.

    Returns:
        Response: API response containing the person data if found, otherwise an error.
    """
    crm_service = OutsetaService.CRMService()
    person_data = crm_service.get_person_by_uid(person_uid)
    if person_data is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(person_data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def add_person_view(request):
    """Add a new person or display the person form.

    GET:
        Returns a template with empty fields for person data.
    POST:
        Adds a new person using provided data.

    Returns:
        Response: API response containing the new person data or form template,
                  or an error if the operation fails.
    """
    if request.method == "GET":
        return ResponseBuilder.success(
            {
                "Email": "",
                "FirstName": "",
                "LastName": "",
                "MailingAddress": {
                    "AddressLine1": "",
                    "AddressLine2": "",
                    "AddressLine3": None,
                    "City": "",
                    "State": "",
                    "PostalCode": "",
                },
            }
        )

    crm_service = OutsetaService.CRMService()
    person_data = crm_service.add_person(request.data)
    return (
        ResponseBuilder.success(person_data, status.HTTP_201_CREATED)
        if person_data
        else ResponseBuilder.error()
    )


@api_view(["GET", "PUT"])
@permission_classes([AllowAny])
def update_person_view(request, person_uid):
    """Retrieve or update a person's details by UID.

    GET:
        Retrieves details of the specified person.
    PUT:
        Updates the person's details with provided data.

    Args:
        person_uid (str): Unique identifier for the person.

    Returns:
        Response: API response containing person data (for GET) or updated data (for PUT),
                  or an error if the person is not found or update fails.
    """
    crm_service = OutsetaService.CRMService()

    if request.method == "GET":
        person_data = crm_service.get_person_by_uid(person_uid)
        if person_data is None:
            return ResponseBuilder.error(
                ERROR_MESSAGES["not_found"], status.HTTP_404_NOT_FOUND
            )
        return ResponseBuilder.success(person_data)

    updated_data = crm_service.update_person(person_uid, request.data)
    if updated_data is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(updated_data)


@api_view(["GET", "DELETE"])
@permission_classes([AllowAny])
def delete_person_view(request, person_uid):
    """Retrieve or delete a person by UID.

    GET:
        Retrieves details of the person to be deleted.
    DELETE:
        Deletes the person.

    Args:
        person_uid (str): Unique identifier for the person.

    Returns:
        Response: API response with person data (for GET) or a confirmation of deletion (for DELETE),
                  or an error if the person is not found or deletion fails.
    """
    crm_service = OutsetaService.CRMService()

    if request.method == "GET":
        person_data = crm_service.get_person_by_uid(person_uid)
        if person_data is None:
            return ResponseBuilder.error(
                ERROR_MESSAGES["not_found"], status.HTTP_404_NOT_FOUND
            )
        return ResponseBuilder.success(person_data)

    success = crm_service.delete_person(person_uid)
    if not success:
        return ResponseBuilder.error()
    return ResponseBuilder.success(status_code=status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
@permission_classes([AllowAny])
def set_temporary_password_view(request, person_uid):
    """Set a temporary password for a user.

    The user must change this password on their next login.

    Args:
        person_uid (str): Unique identifier for the person.
        request.data (dict): Must include the key "temporaryPassword".

    Returns:
        Response: API response confirming the temporary password is set,
                  or an error if missing parameter or operation fails.
    """
    if not request.data.get("temporaryPassword"):
        return ResponseBuilder.error(
            ERROR_MESSAGES["temporary_password"], status.HTTP_400_BAD_REQUEST
        )

    crm_service = OutsetaService.CRMService()
    success = crm_service.set_temporary_password(
        person_uid, request.data["temporaryPassword"]
    )

    if not success:
        return ResponseBuilder.error()
    return ResponseBuilder.success(SUCCESS_MESSAGES["temp_password_set"])


@api_view(["POST"])
@permission_classes([AllowAny])
def initiate_password_reset_view(request):
    """Initiate a password reset via Outseta CRM API.

    Expects a query parameter "parentUrl" and a POST body with "Email".

    Query Parameters:
        parentUrl (str): URL to redirect after password reset.

    Body:
        Email (str): The email of the person.

    Returns:
        Response: API response with reset details or an error if parameters are missing or operation fails.
    """
    parent_url = request.query_params.get("parentUrl")
    email = request.data.get("Email")

    if not parent_url or not email:
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    crm_service = OutsetaService.CRMService()
    reset_response = crm_service.initiate_password_reset(parent_url, email)

    if reset_response is None:
        return ResponseBuilder.error()

    return ResponseBuilder.success(reset_response)


@api_view(["PUT"])
@permission_classes([AllowAny])
def send_confirmation_email_view(request, account_uid):
    """Send a confirmation email via Outseta CRM API.

    Depending on the query parameter "personUid", sends the email to:
        - All people in the account if personUid is "*"
        - A specific person if a UID is provided
        - The primary person if no query parameter is provided

    Args:
        account_uid (str): Unique identifier for the account.

    Returns:
        Response: API response confirming the email was sent,
                  or an error if the operation fails.
    """
    person_uid = request.query_params.get("personUid")
    crm_service = OutsetaService.CRMService()
    if person_uid == "*":
        success = crm_service.send_confirmation_email_to_all(account_uid)
    elif person_uid:
        success = crm_service.send_confirmation_email_to_specific_person(
            account_uid, person_uid
        )
    else:
        success = crm_service.send_confirmation_email_to_primary_person(account_uid)

    if not success:
        return ResponseBuilder.error()
    return ResponseBuilder.success(SUCCESS_MESSAGES["email_sent"])


# ------------------------------------------ Accounts


@api_view(["GET", "DELETE"])
@permission_classes([AllowAny])
def account_detail_view(request, account_uid):
    """Retrieve or delete an account by UID.

    GET:
        Retrieves account information.
    DELETE:
        Deletes the account record.

    Args:
        account_uid (str): Unique identifier for the account.

    Returns:
        Response: API response with account details (GET) or a deletion confirmation (DELETE),
                  or an error if operation fails.
    """
    crm_service = OutsetaService.CRMService()
    if request.method == "GET":
        account_data = crm_service.get_account(account_uid)
        if account_data is None:
            return ResponseBuilder.error()
        return ResponseBuilder.success(account_data)
    elif request.method == "DELETE":
        success = crm_service.delete_account(account_uid)
        if not success:
            return ResponseBuilder.error()
        return ResponseBuilder.success(status_code=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_account_view(request, account_uid):
    """Retrieve full account information by UID.

    Args:
        account_uid (str): Unique identifier for the account.

    Returns:
        Response: API response containing account information,
                  or an error if the account is not found.
    """
    crm_service = OutsetaService.CRMService()
    account_data = crm_service.get_account(account_uid)
    if account_data is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(account_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_accounts_view(request):
    """Retrieve all accounts or filter by account stage.

    Query Parameters:
        AccountStage (str, optional): Stage to filter accounts by.

    Returns:
        Response: API response containing accounts data,
                  or an error if no accounts are found.
    """
    account_stage = request.query_params.get("AccountStage")
    crm_service = OutsetaService.CRMService()

    if account_stage:
        accounts_data = crm_service.get_accounts_by_stage(account_stage)
    else:
        accounts_data = crm_service.get_all_accounts()

    if accounts_data is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(accounts_data)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def accounts_view(request):
    """Retrieve accounts or add a new account.

    GET:
        Retrieves accounts. Optionally, can filter by "AccountStage" query parameter.
    POST:
        Adds a new account. If "sendConfirmationEmail" query parameter is present,
        adds account with a new person; otherwise, adds account with an existing person.

    Returns:
        Response: API response with accounts data or new account details,
                  or an error if the operation fails.
    """
    crm_service = OutsetaService.CRMService()
    if request.method == "GET":
        account_stage = request.query_params.get("AccountStage")
        if account_stage:
            accounts_data = crm_service.get_accounts_by_stage(account_stage)
        else:
            accounts_data = crm_service.get_all_accounts()
        if accounts_data is None:
            return ResponseBuilder.error()
        return ResponseBuilder.success(accounts_data)
    elif request.method == "POST":
        send_confirmation_email_param = request.query_params.get(
            "sendConfirmationEmail"
        )
        if send_confirmation_email_param is not None:
            send_confirmation_email = send_confirmation_email_param.lower() == "true"
            account_data = crm_service.add_account_with_new_person(
                request.data, send_confirmation_email
            )
        else:
            account_data = crm_service.add_account_with_existing_person(request.data)
        if account_data is None:
            return ResponseBuilder.error()
        return ResponseBuilder.success(account_data, status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def add_membership_view(request, account_uid):
    """Add a person to an account (new or existing membership).

    Query Parameters:
        sendWelcomeEmail (str, optional): "true" or "false" to send a welcome email.

    Body:
        For a new person: Must include "Email", "FirstName", and "LastName".
        For an existing person: Must include "Uid".

    Args:
        account_uid (str): Unique identifier for the account.

    Returns:
        Response: API response with membership data,
                  or an error if the operation fails.
    """
    send_welcome_email_param = request.query_params.get("sendWelcomeEmail")
    send_welcome_email = None
    if send_welcome_email_param is not None:
        send_welcome_email = send_welcome_email_param.lower() == "true"
    crm_service = OutsetaService.CRMService()
    membership_data = crm_service.add_membership(
        account_uid, request.data, send_welcome_email
    )
    if membership_data is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(membership_data, status.HTTP_201_CREATED)


@api_view(["PUT"])
@permission_classes([AllowAny])
def update_account_view(request, account_uid):
    """Update account information.

    Allows updating one or multiple account properties.

    Args:
        account_uid (str): Unique identifier for the account.
        request.data (dict): Data containing account properties to update.

    Returns:
        Response: API response with updated account data,
                  or an error if the update fails.
    """
    crm_service = OutsetaService.CRMService()
    updated_account = crm_service.update_account(account_uid, request.data)
    if updated_account is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(updated_account)


@api_view(["PUT"])
@permission_classes([AllowAny])
def cancel_account_view(request, account_uid):
    """Submit a cancellation request for an account.

    The account must be in the subscribing stage.
    At subscription renewal, the subscription will end and the account will be set to expired.

    Args:
        account_uid (str): Unique identifier for the account.
        request.data (dict): Data required for cancellation.

    Returns:
        Response: API response with cancellation confirmation,
                  or an error if the cancellation fails.
    """
    crm_service = OutsetaService.CRMService()
    cancellation_response = crm_service.cancel_account(account_uid, request.data)
    if cancellation_response is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(cancellation_response)


@api_view(["PUT"])
@permission_classes([AllowAny])
def remove_cancellation_view(request, account_uid):
    """Remove a previously submitted cancellation request.

    Args:
        account_uid (str): Unique identifier for the account.

    Returns:
        Response: API response with removal confirmation,
                  or an error if the removal fails.
    """
    crm_service = OutsetaService.CRMService()
    removal_response = crm_service.remove_cancellation(account_uid)
    if removal_response is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(removal_response)


@api_view(["PUT"])
@permission_classes([AllowAny])
def update_person_account_membership_view(request, account_uid, membership_uid):
    """Update an account membership.

    This can be used to change properties such as the primary contact.

    Args:
        account_uid (str): Unique identifier for the account.
        membership_uid (str): Unique identifier for the membership.
        request.data (dict): Data containing membership properties to update.

    Returns:
        Response: API response with updated membership data,
                  or an error if the update fails.
    """
    crm_service = OutsetaService.CRMService()
    membership_response = crm_service.update_person_account_membership(
        account_uid, membership_uid, request.data
    )
    if membership_response is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(membership_response)


@api_view(["DELETE"])
@permission_classes([AllowAny])
def remove_person_from_account_view(request, account_uid, membership_uid):
    """Remove a person from an account.

    Note: The primary contact cannot be removed.

    Args:
        account_uid (str): Unique identifier for the account.
        membership_uid (str): Unique identifier for the membership.

    Returns:
        Response: API response with removal confirmation,
                  or an error if the removal fails.
    """
    crm_service = OutsetaService.CRMService()
    success = crm_service.remove_person_from_account(account_uid, membership_uid)
    if not success:
        return ResponseBuilder.error()
    return ResponseBuilder.success(status_code=status.HTTP_204_NO_CONTENT)


# ------------------------------------------ Activities


@api_view(["GET"])
@permission_classes([AllowAny])
def get_activities_view(request):
    """Retrieve all activities based on query parameters.

    The query parameters are used to filter the activities.

    Returns:
        Response: API response containing the list of activities,
                  or an error if the operation fails.
    """
    crm_service = OutsetaService.CRMService()
    activities_data = crm_service.get_all_activities(request.query_params.dict())
    return (
        ResponseBuilder.success(activities_data)
        if activities_data
        else ResponseBuilder.error()
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def add_custom_activity_view(request):
    """Record a custom activity.

    Args:
        request.data (dict): Data for the custom activity.

    Returns:
        Response: API response with the new activity data,
                  or an error if the operation fails.
    """
    crm_service = OutsetaService.CRMService()
    activity_data = crm_service.add_custom_activity(request.data)
    return (
        ResponseBuilder.success(activity_data, status.HTTP_201_CREATED)
        if activity_data
        else ResponseBuilder.error()
    )


# ------------------------------------------ Deals


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def deals_view(request):
    """Retrieve all deals or add a new deal.

    GET:
        Retrieves all deals.
    POST:
        Adds a new deal with provided data.

    Returns:
        Response: API response containing deals data or new deal details,
                  or an error if the operation fails.
    """
    crm_service = OutsetaService.CRMService()
    if request.method == "GET":
        deals_data = crm_service.get_all_deals()
        if deals_data is None:
            return ResponseBuilder.error()
        return ResponseBuilder.success(deals_data)
    elif request.method == "POST":
        new_deal = crm_service.add_deal(request.data)
        if new_deal is None:
            return ResponseBuilder.error()
        return ResponseBuilder.success(new_deal, status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def deal_detail_view(request, deal_uid):
    """Retrieve, update, or delete a single deal by UID.

    GET:
        Retrieves the deal details.
    PUT:
        Updates the deal with provided data.
    DELETE:
        Deletes the deal.

    Args:
        deal_uid (str): Unique identifier for the deal.

    Returns:
        Response: API response with deal data, updated deal, or deletion confirmation,
                  or an error if the operation fails.
    """
    crm_service = OutsetaService.CRMService()
    if request.method == "GET":
        deal_data = crm_service.get_deal(deal_uid)
        if deal_data is None:
            return ResponseBuilder.error(
                ERROR_MESSAGES["not_found"], status.HTTP_404_NOT_FOUND
            )
        return ResponseBuilder.success(deal_data)
    elif request.method == "PUT":
        updated_deal = crm_service.update_deal(deal_uid, request.data)
        if updated_deal is None:
            return ResponseBuilder.error()
        return ResponseBuilder.success(updated_deal)
    elif request.method == "DELETE":
        success = crm_service.delete_deal(deal_uid)
        if not success:
            return ResponseBuilder.error()
        return ResponseBuilder.success(status_code=status.HTTP_204_NO_CONTENT)


##################################################################################################################
# ---------------------------MARKETING VIEWS--------------------------
##################################################################################################################


@api_view(["GET"])
@permission_classes([AllowAny])
def get_list_subscribers_view(request, list_id):
    """Retrieve all subscribers for a given email list.

    Args:
        list_id (str): Unique identifier for the email list.

    Returns:
        Response: API response containing the list of subscribers,
                  or an error if the operation fails.
    """
    marketing_service = OutsetaService.MarketingService()
    subscribers_data = marketing_service.get_list_subscribers(list_id)
    if subscribers_data is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(subscribers_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def subscribe_new_person_view(request, list_id):
    """Subscribe a new person to an email list.

    Required body parameters:
        - Email (str)
        - FirstName (str)
        - LastName (str)
    Optional query parameter:
        - sendWelcomeEmail (str): "true" or "false" (default is false).

    Args:
        list_id (str): Unique identifier for the email list.

    Returns:
        Response: API response confirming subscription,
                  or an error if parameters are missing or the operation fails.
    """
    if not all(k in request.data for k in ["Email", "FirstName", "LastName"]):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    send_welcome_email = (
        request.query_params.get("sendWelcomeEmail", "false").lower() == "true"
    )

    marketing_service = OutsetaService.MarketingService()
    success = marketing_service.add_new_subscriber(
        list_id, request.data, send_welcome_email
    )

    if not success:
        return ResponseBuilder.error()
    return ResponseBuilder.success(
        SUCCESS_MESSAGES["subscription_added"], status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def subscribe_existing_person_view(request, list_id):
    """Subscribe an existing person to an email list.

    Required body parameter:
        - personUid (str)
    Optional query parameter:
        - sendWelcomeEmail (str): "true" or "false" (default is false).

    Args:
        list_id (str): Unique identifier for the email list.

    Returns:
        Response: API response confirming subscription,
                  or an error if parameters are missing or the operation fails.
    """
    person_uid = request.data.get("personUid")
    if not person_uid:
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    send_welcome_email = (
        request.query_params.get("sendWelcomeEmail", "false").lower() == "true"
    )

    marketing_service = OutsetaService.MarketingService()
    success = marketing_service.add_existing_subscriber(
        list_id, person_uid, send_welcome_email
    )

    if not success:
        return ResponseBuilder.error()
    return ResponseBuilder.success(
        SUCCESS_MESSAGES["subscription_added"], status.HTTP_201_CREATED
    )


@api_view(["DELETE"])
@permission_classes([AllowAny])
def remove_subscriber_view(request, list_id, subscription_uid):
    """Remove a subscriber from an email list.

    Args:
        list_id (str): Unique identifier for the email list.
        subscription_uid (str): Unique identifier for the subscription.

    Returns:
        Response: API response confirming removal,
                  or an error if the subscriber is not found.
    """
    marketing_service = OutsetaService.MarketingService()
    success = marketing_service.remove_subscriber(list_id, subscription_uid)
    if not success:
        return ResponseBuilder.error(
            ERROR_MESSAGES["not_found"], status.HTTP_404_NOT_FOUND
        )
    return ResponseBuilder.success(
        SUCCESS_MESSAGES["subscription_removed"], status.HTTP_204_NO_CONTENT
    )


##################################################################################################################
# ---------------------------SUPPORT VIEWS--------------------------
##################################################################################################################


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_cases_view(request):
    """Retrieve all support cases.

    Returns:
        Response: API response containing all support cases,
                  or an error if the operation fails.
    """
    support_service = OutsetaService.SupportService()
    cases_data = support_service.get_all_cases()
    if cases_data is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(cases_data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_cases_by_person_view(request):
    """Retrieve all support cases for a specific person.

    Query Parameters:
        - uid (str, optional): Person UID.
        - email (str, optional): Person email.

    Returns:
        Response: API response containing the cases for the specified person,
                  or an error if parameters are missing or the operation fails.
    """
    person_uid = request.query_params.get("uid")
    email = request.query_params.get("email")

    if not (person_uid or email):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    support_service = OutsetaService.SupportService()
    cases_data = None

    if person_uid:
        cases_data = support_service.get_cases_by_person_uid(person_uid)
    elif email:
        cases_data = support_service.get_cases_by_person_email(email)

    if cases_data is None:
        return ResponseBuilder.error()
    return ResponseBuilder.success(cases_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def add_case_view(request):
    """Create a new support case.

    Query Parameters:
        - sendAutoResponder (str, optional): "true" or "false" (default is true).

    Required Body Parameters:
        - FromPerson (dict): Must include Uid.
        - Subject (str)
        - Body (str)
        - Source (str)

    Returns:
        Response: API response with the created case details,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["FromPerson", "Subject", "Body", "Source"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    send_auto_responder = (
        request.query_params.get("sendAutoResponder", "true").lower() == "true"
    )

    support_service = OutsetaService.SupportService()
    success = support_service.add_case(request.data, send_auto_responder)

    if not success:
        return ResponseBuilder.error()
    return ResponseBuilder.success(
        SUCCESS_MESSAGES["case_added"], status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def add_client_response_view(request, case_uid):
    """Add a client response to an existing support case.

    Args:
        case_uid (str): Unique identifier for the support case.
        request.data (dict): Must include "comment" key.

    Returns:
        Response: API response confirming the response was added,
                  or an error if the comment is missing or the operation fails.
    """
    comment = request.data.get("comment")
    if not comment:
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    support_service = OutsetaService.SupportService()
    success = support_service.add_client_response(case_uid, comment)

    if not success:
        return ResponseBuilder.error()
    return ResponseBuilder.success(
        SUCCESS_MESSAGES["response_added"], status.HTTP_200_OK
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def add_agent_reply_view(request, case_uid):
    """Add an agent reply to a support case.

    Args:
        case_uid (str): Unique identifier for the support case.
        request.data (dict): Must include "agentName" and "comment" keys.

    Returns:
        Response: API response confirming the reply was added,
                  or an error if parameters are missing or the operation fails.
    """
    agent_name = request.data.get("agentName")
    comment = request.data.get("comment")

    if not all([agent_name, comment]):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    support_service = OutsetaService.SupportService()
    success = support_service.add_agent_reply(case_uid, agent_name, comment)

    if not success:
        return ResponseBuilder.error()
    return ResponseBuilder.success(SUCCESS_MESSAGES["reply_added"], status.HTTP_200_OK)


##################################################################################################################
# ---------------------------BILLING VIEWS--------------------------
##################################################################################################################


# ------------------------------------------------------------------------------------------- PLAN FAMILIES
@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_plan_families_view(request):
    """Retrieve all plan families from Outseta Billing API.

    Returns:
        Response: API response containing all plan families data, or an error if none found.
    """
    billing_service = OutsetaService.BillingService()
    plan_families_data = billing_service.get_all_plan_families()
    return (
        ResponseBuilder.success(plan_families_data)
        if plan_families_data
        else ResponseBuilder.error()
    )


# ------------------------------------------------------------------------------------------- PLANS


@api_view(["GET"])
@permission_classes([AllowAny])
def get_all_plans_view(request):
    """Retrieve all plans from Outseta Billing API.

    Returns:
        Response: API response containing all plans data, or an error if none found.
    """
    billing_service = OutsetaService.BillingService()
    plans_data = billing_service.get_all_plans()
    return (
        ResponseBuilder.success(plans_data) if plans_data else ResponseBuilder.error()
    )


# ------------------------------------------------------------------------------------------- ADD-ONS


@api_view(["POST"])
@permission_classes([AllowAny])
def add_usage_for_addon_view(request):
    """Add usage entry for an add-on that bills for usage at the end of the month.

    Required Body Parameters:
        - UsageDate (str): Date and time of usage in ISO format
        - Amount (number): Amount of usage
        - SubscriptionAddOn (object): Object containing Uid of the subscription add-on

    Returns:
        Response: API response with the created usage entry data,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["UsageDate", "Amount", "SubscriptionAddOn"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    billing_service = OutsetaService.BillingService()
    usage_data = billing_service.add_usage_for_addon(request.data)

    if not usage_data:
        return ResponseBuilder.error()
    return ResponseBuilder.success(usage_data, status.HTTP_201_CREATED)


# ------------------------------------------------------------------------------------------- DISCOUNTS


@api_view(["POST"])
@permission_classes([AllowAny])
def add_discount_coupon_view(request):
    """Add a new discount coupon.

    Required Body Parameters:
        - UniqueIdentifier (str): Unique code for the coupon
        - Name (str): Display name for the coupon
        - IsActive (bool): Whether the coupon is active
        - Either AmountOff or PercentOff (number): Discount amount or percentage
        - Duration (int): 1 for Forever, 2 for Once, 3 for Repeating

    Optional Body Parameters:
        - DurationInMonths (int): Required if Duration is 3 (Repeating)
        - MaxRedemptions (int): Maximum number of times the coupon can be redeemed
        - RedeemBy (str): Date by which the coupon must be redeemed
        - DiscountCouponPlans (array): List of plans the coupon applies to

    Returns:
        Response: API response with the created discount coupon data,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["UniqueIdentifier", "Name", "IsActive", "Duration"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Check if either AmountOff or PercentOff is provided
    if "AmountOff" not in request.data and "PercentOff" not in request.data:
        return ResponseBuilder.error(
            {"error": "Either AmountOff or PercentOff must be provided."},
            status.HTTP_400_BAD_REQUEST,
        )

    # Check if DurationInMonths is provided for Repeating duration
    if request.data.get("Duration") == 3 and "DurationInMonths" not in request.data:
        return ResponseBuilder.error(
            {"error": "DurationInMonths is required for Repeating duration."},
            status.HTTP_400_BAD_REQUEST,
        )

    billing_service = OutsetaService.BillingService()
    discount_data = billing_service.add_discount_coupon(request.data)

    if not discount_data:
        return ResponseBuilder.error()
    return ResponseBuilder.success(discount_data, status.HTTP_201_CREATED)


# ------------------------------------------------------------------------------------------- Subscriptions


@api_view(["GET"])
@permission_classes([AllowAny])
def get_subscription_view(request, subscription_uid):
    """Get subscription details by UID.

    Args:
        subscription_uid (str): Unique identifier for the subscription.

    Returns:
        Response: API response containing subscription details,
                  or an error if not found.
    """
    billing_service = OutsetaService.BillingService()
    subscription_data = billing_service.get_subscription(subscription_uid)

    if not subscription_data:
        return ResponseBuilder.error(
            ERROR_MESSAGES["not_found"], status.HTTP_404_NOT_FOUND
        )
    return ResponseBuilder.success(subscription_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def compute_charge_summary_view(request):
    """Preview charges for a subscription (first time or renewal).

    Used to see what the initial or renewal invoice would look like if an account
    were to register with this subscription.

    Query Parameters:
        - asOf (str, optional): "now" (default) or "renewal"

    Required Body Parameters:
        - Plan (object): Must include Uid of the plan
        - BillingRenewalTerm (int): 1=Monthly, 2=Yearly, 3=Quarterly, 4=OneTime
        - Account (object): Can be empty for new accounts

    Returns:
        Response: API response with invoice preview data,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["Plan", "BillingRenewalTerm", "Account"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Validate Plan has Uid
    if not request.data["Plan"].get("Uid"):
        return ResponseBuilder.error(
            {"error": "Plan must include Uid."}, status.HTTP_400_BAD_REQUEST
        )

    as_of = request.query_params.get("asOf", "now")
    billing_service = OutsetaService.BillingService()
    invoice_data = billing_service.compute_charge_summary(request.data, as_of)

    if not invoice_data:
        return ResponseBuilder.error()
    return ResponseBuilder.success(invoice_data)


@api_view(["PUT"])
@permission_classes([AllowAny])
def add_first_time_subscription_view(request):
    """Add first time subscription to an account.

    This method is used when adding a subscription to an account for the first time.

    Required Body Parameters:
        - Plan (object): Must include Uid of the plan
        - BillingRenewalTerm (int): 1=Monthly, 2=Yearly, 3=Quarterly, 4=OneTime
        - Account (object): Must include Uid of the account

    Returns:
        Response: API response with invoice details,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["Plan", "BillingRenewalTerm", "Account"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Validate Plan and Account have Uid
    if not request.data["Plan"].get("Uid") or not request.data["Account"].get("Uid"):
        return ResponseBuilder.error(
            {"error": "Plan and Account must include Uid."}, status.HTTP_400_BAD_REQUEST
        )

    billing_service = OutsetaService.BillingService()

    # Eğer SubscriptionAddOns varsa addons metodu kullanılır, yoksa standart metod
    if "SubscriptionAddOns" in request.data and request.data["SubscriptionAddOns"]:
        subscription_data = billing_service.add_first_time_subscription_with_addons(
            request.data
        )
    else:
        subscription_data = billing_service.add_first_time_subscription(request.data)

    if not subscription_data:
        return ResponseBuilder.error(
            {"error": "Failed to create subscription. Please check your parameters."},
            status.HTTP_400_BAD_REQUEST,
        )
    return ResponseBuilder.success(subscription_data)


@api_view(["PUT"])
@permission_classes([AllowAny])
def change_subscription_preview_view(request, subscription_uid):
    """Preview changes to an existing subscription.

    Args:
        subscription_uid (str): Unique identifier for the subscription.

    Required Body Parameters:
        - Plan (object): Must include Uid
        - BillingRenewalTerm (int): 1=Monthly, 2=Yearly, 3=Quarterly, 4=OneTime
        - Account (object): Must include Uid

    Returns:
        Response: API response with invoice preview data,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["Plan", "BillingRenewalTerm", "Account"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Validate Plan and Account have Uid
    if not request.data["Plan"].get("Uid") or not request.data["Account"].get("Uid"):
        return ResponseBuilder.error(
            {"error": "Plan and Account must include Uid."}, status.HTTP_400_BAD_REQUEST
        )

    billing_service = OutsetaService.BillingService()
    preview_data = billing_service.change_subscription_preview(
        subscription_uid, request.data
    )

    if not preview_data:
        return ResponseBuilder.error()
    return ResponseBuilder.success(preview_data)


@api_view(["PUT"])
@permission_classes([AllowAny])
def change_subscription_view(request, subscription_uid):
    """Change an existing subscription.

    Args:
        subscription_uid (str): Unique identifier for the subscription.

    Required Body Parameters:
        - Plan (object): Must include Uid
        - BillingRenewalTerm (int): 1=Monthly, 2=Yearly, 3=Quarterly, 4=OneTime
        - Account (object): Must include Uid

    Returns:
        Response: API response with updated subscription data,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["Plan", "BillingRenewalTerm", "Account"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Validate Plan and Account have Uid
    if not request.data["Plan"].get("Uid") or not request.data["Account"].get("Uid"):
        return ResponseBuilder.error(
            {"error": "Plan and Account must include Uid."}, status.HTTP_400_BAD_REQUEST
        )

    billing_service = OutsetaService.BillingService()
    updated_data = billing_service.change_subscription(subscription_uid, request.data)

    if not updated_data:
        return ResponseBuilder.error()
    return ResponseBuilder.success(updated_data)


@api_view(["PUT"])
@permission_classes([AllowAny])
def set_subscription_upgrade_required_view(request, subscription_uid):
    """Mark a subscription as requiring an upgrade.

    Args:
        subscription_uid (str): Unique identifier for the subscription.

    Required Body Parameters:
        - Uid (str): Subscription UID (must match the subscription_uid in the URL)
        - IsPlanUpgradeRequired (bool): Whether an upgrade is required
        - PlanUpgradeRequiredMessage (str): Message to show to the user

    Optional Body Parameters:
        - NewRequiredQuantity (int): New required quantity

    Returns:
        Response: API response with updated subscription data,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["Uid", "IsPlanUpgradeRequired", "PlanUpgradeRequiredMessage"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Ensure the Uid in the body matches the subscription_uid in the URL
    if request.data.get("Uid") != subscription_uid:
        return ResponseBuilder.error(
            {"error": "Subscription UID in body must match URL parameter."},
            status.HTTP_400_BAD_REQUEST,
        )

    billing_service = OutsetaService.BillingService()
    updated_data = billing_service.set_subscription_upgrade_required(
        subscription_uid, request.data
    )

    if not updated_data:
        return ResponseBuilder.error()
    return ResponseBuilder.success(updated_data)


@api_view(["PUT"])
@permission_classes([AllowAny])
def extend_trial_view(request, account_uid, trial_end_date):
    """Extend the trial period for an account.

    Args:
        account_uid (str): Unique identifier for the account.
        trial_end_date (str): The new trial end date in YYYY-MM-DD format.

    Returns:
        Response: API response confirming the trial extension,
                  or an error if the operation fails.
    """
    # Validate date format
    try:
        from datetime import datetime

        datetime.strptime(trial_end_date, "%Y-%m-%d")
    except ValueError:
        return ResponseBuilder.error(
            {"error": "Invalid date format. Use YYYY-MM-DD."},
            status.HTTP_400_BAD_REQUEST,
        )

    # Bu fonksiyon BillingService yerine CRMService'i kullanmalı
    crm_service = OutsetaService.CRMService()
    result = crm_service.extend_trial(account_uid, trial_end_date)

    if not result:
        return ResponseBuilder.error()
    return ResponseBuilder.success(
        {"message": f"Trial period extended to {trial_end_date}", "account": result}
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def add_addon_to_subscription_view(request):
    """Add an add-on to a subscription.

    Required Body Parameters:
        - AddOn (object): Must include Uid of the add-on
        - BillingRenewalTerm (int): 1=Monthly, 2=Yearly, 3=Quarterly, 4=OneTime
        - Quantity (int): Quantity of the add-on
        - Subscription (object): Must include Uid of the subscription

    Returns:
        Response: API response with the add-on data,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["AddOn", "BillingRenewalTerm", "Quantity", "Subscription"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Validate AddOn and Subscription have Uid
    if not request.data["AddOn"].get("Uid") or not request.data["Subscription"].get(
        "Uid"
    ):
        return ResponseBuilder.error(
            {"error": "AddOn and Subscription must include Uid."},
            status.HTTP_400_BAD_REQUEST,
        )

    billing_service = OutsetaService.BillingService()
    addon_data = billing_service.add_addon_to_subscription(request.data)

    if not addon_data:
        return ResponseBuilder.error()
    return ResponseBuilder.success(addon_data, status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def add_discount_to_subscription_view(request, subscription_uid, discount_uid):
    """Add a discount to a subscription.

    Args:
        subscription_uid (str): Unique identifier for the subscription.
        discount_uid (str): Unique identifier for the discount coupon.

    Returns:
        Response: API response confirming the discount was applied,
                  or an error if the operation fails.
    """
    billing_service = OutsetaService.BillingService()
    result = billing_service.add_discount_to_subscription(
        subscription_uid, discount_uid
    )

    if not result:
        return ResponseBuilder.error()
    return ResponseBuilder.success(
        {"message": "Discount applied successfully", "subscription": result}
    )


# ------------------------------------------------------------------------------------------- INVOICES


@api_view(["POST"])
@permission_classes([AllowAny])
def add_new_invoice_view(request):
    """Create a new ad-hoc invoice for an account.

    Required Body Parameters:
        - Subscription (object): Must include Uid of the subscription
        - InvoiceDate (str): Date in ISO format
        - InvoiceLineItems (array): List of line items with Description and Amount

    Returns:
        Response: API response with the created invoice data,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["Subscription", "InvoiceDate", "InvoiceLineItems"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Validate Subscription has Uid and InvoiceLineItems is a non-empty array
    if (
        not request.data["Subscription"].get("Uid")
        or not isinstance(request.data["InvoiceLineItems"], list)
        or len(request.data["InvoiceLineItems"]) == 0
    ):
        return ResponseBuilder.error(
            {
                "error": "Invalid parameters. Check Subscription Uid and InvoiceLineItems."
            },
            status.HTTP_400_BAD_REQUEST,
        )

    # Validate each line item has Description and Amount
    for item in request.data["InvoiceLineItems"]:
        if not all(key in item for key in ["Description", "Amount"]):
            return ResponseBuilder.error(
                {
                    "error": "Each invoice line item must include Description and Amount."
                },
                status.HTTP_400_BAD_REQUEST,
            )

    billing_service = OutsetaService.BillingService()
    invoice_data = billing_service.add_new_invoice(request.data)

    if not invoice_data:
        return ResponseBuilder.error()
    return ResponseBuilder.success(invoice_data, status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_transactions_by_account_view(request, account_uid):
    """Get all transactions for a specific account.

    Args:
        account_uid (str): Unique identifier for the account.

    Returns:
        Response: API response containing the transactions data,
                  or an error if no transactions are found.
    """
    billing_service = OutsetaService.BillingService()
    transactions_data = billing_service.get_transactions_by_account(account_uid)

    if not transactions_data:
        return ResponseBuilder.error(
            ERROR_MESSAGES["not_found"], status.HTTP_404_NOT_FOUND
        )
    return ResponseBuilder.success(transactions_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def add_invoice_payment_view(request):
    """Add a payment to an invoice.

    If the payment amount matches the outstanding amount of the invoice,
    the invoice will be marked as Paid.

    Required Body Parameters:
        - Account (object): Must include Uid of the account
        - Invoice (object): Must include Uid of the invoice
        - Amount (number): Payment amount (negative value for refunds)

    Returns:
        Response: API response with the transaction data,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["Account", "Invoice", "Amount"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Validate Account and Invoice have Uid
    if not request.data["Account"].get("Uid") or not request.data["Invoice"].get("Uid"):
        return ResponseBuilder.error(
            {"error": "Account and Invoice must include Uid."},
            status.HTTP_400_BAD_REQUEST,
        )

    billing_service = OutsetaService.BillingService()
    transaction_data = billing_service.add_invoice_payment(request.data)

    if not transaction_data:
        return ResponseBuilder.error()
    return ResponseBuilder.success(transaction_data, status.HTTP_201_CREATED)


# ------------------------------------------------------------------------------------------- PAYMENT INFORMATION


@api_view(["POST"])
@permission_classes([AllowAny])
def update_payment_information_view(request):
    """Update payment information for an account.

    Required Body Parameters:
        - Account (object): Must include Uid of the account
        - CustomerToken (str): Customer token from payment provider
        - NameOnCard (str): Name on the payment card
        - PaymentToken (str): Payment method token from payment provider

    Returns:
        Response: API response with the updated payment information,
                  or an error if parameters are missing or the operation fails.
    """
    required_fields = ["Account", "CustomerToken", "NameOnCard", "PaymentToken"]
    if not all(field in request.data for field in required_fields):
        return ResponseBuilder.error(
            ERROR_MESSAGES["invalid_params"], status.HTTP_400_BAD_REQUEST
        )

    # Validate Account has Uid
    if not request.data["Account"].get("Uid"):
        return ResponseBuilder.error(
            {"error": "Account must include Uid."}, status.HTTP_400_BAD_REQUEST
        )

    billing_service = OutsetaService.BillingService()
    payment_info = billing_service.update_payment_information(request.data)

    if not payment_info:
        return ResponseBuilder.error()
    return ResponseBuilder.success(payment_info)


##################################################################################################################
# ---------------------------USER PROFILE VIEWS--------------------------
##################################################################################################################


@api_view(["GET"])
@permission_classes([AllowAny])
def get_user_profile_view(request):
    """
    Retrieve the profile information of the authenticated user.

    This endpoint requires authentication using a bearer token obtained from the auth token endpoint.

    Headers:
        Authorization (str): Bearer token from auth endpoint

    Returns:
        Response: API response containing user profile data,
                  or an error if the authorization is missing or invalid.
    """
    # Extract auth token from request
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return ResponseBuilder.error(
            {"error": "Authorization header is required"}, status.HTTP_401_UNAUTHORIZED
        )

    # Create user profile service with the auth token
    profile_service = OutsetaService.UserProfileService(auth_token=auth_header)
    profile_data = profile_service.get_profile()

    if not profile_data:
        return ResponseBuilder.error(
            {"error": "Failed to retrieve user profile or unauthorized"},
            status.HTTP_401_UNAUTHORIZED,
        )

    return ResponseBuilder.success(profile_data)


@api_view(["PUT"])
@permission_classes([AllowAny])
def update_user_profile_view(request):
    """
    Update the profile information of the authenticated user.

    This endpoint requires authentication using a bearer token obtained from the auth token endpoint.

    Headers:
        Authorization (str): Bearer token from auth endpoint

    Body:
        - Email (str): User's email
        - FirstName (str): User's first name
        - LastName (str): User's last name
        - MailingAddress (dict, optional): User's mailing address
        - Uid (str): Must match the authenticated user's UID

    Returns:
        Response: API response containing updated user profile data,
                  or an error if the authorization is missing or invalid.
    """
    # Extract auth token from request
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return ResponseBuilder.error(
            {"error": "Authorization header is required"}, status.HTTP_401_UNAUTHORIZED
        )

    # Validate required fields
    if not all(
        key in request.data for key in ["Email", "FirstName", "LastName", "Uid"]
    ):
        return ResponseBuilder.error(
            {"error": "Required fields missing: Email, FirstName, LastName, Uid"},
            status.HTTP_400_BAD_REQUEST,
        )

    # Create user profile service with the auth token
    profile_service = OutsetaService.UserProfileService(auth_token=auth_header)
    updated_profile = profile_service.update_profile(request.data)

    if not updated_profile:
        return ResponseBuilder.error(
            {"error": "Failed to update user profile or unauthorized"},
            status.HTTP_401_UNAUTHORIZED,
        )

    return ResponseBuilder.success(updated_profile)


@api_view(["PUT"])
@permission_classes([AllowAny])
def update_user_password_view(request):
    """
    Update the password for the authenticated user.

    This endpoint requires authentication using a bearer token obtained from the auth token endpoint.

    Headers:
        Authorization (str): Bearer token from auth endpoint

    Body:
        - ExistingPassword (str): User's current password
        - NewPassword (str): User's new password

    Returns:
        Response: API response confirming password update,
                  or an error if the authorization is missing or invalid.
    """
    # Extract auth token from request
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return ResponseBuilder.error(
            {"error": "Authorization header is required"}, status.HTTP_401_UNAUTHORIZED
        )

    # Validate required fields
    if not all(key in request.data for key in ["ExistingPassword", "NewPassword"]):
        return ResponseBuilder.error(
            {"error": "Required fields missing: ExistingPassword, NewPassword"},
            status.HTTP_400_BAD_REQUEST,
        )

    # Create user profile service with the auth token
    profile_service = OutsetaService.UserProfileService(auth_token=auth_header)
    result = profile_service.update_password(
        request.data["ExistingPassword"], request.data["NewPassword"]
    )

    if result is None:
        return ResponseBuilder.error(
            {"error": "Failed to update password or unauthorized"},
            status.HTTP_401_UNAUTHORIZED,
        )

    return ResponseBuilder.success({"message": "Password updated successfully"})


##################################################################################################################
# ---------------------------AUTHENTICATION VIEWS--------------------------
##################################################################################################################


@api_view(["POST"])
@permission_classes([AllowAny])
def get_auth_token_view(request):
    """
    Get authentication token using username and password.

    This endpoint should be called from the server side to keep credentials secure.

    Required Body Parameters:
        - username (str): User's email or username
        - password (str): User's password

    Returns:
        Response: API response containing access token info,
                  or an error if credentials are invalid.
    """
    username = request.data.get("username")
    password = request.data.get("password")

    if not all([username, password]):
        return ResponseBuilder.error(
            {"error": "Username and password are required"}, status.HTTP_400_BAD_REQUEST
        )

    auth_service = OutsetaService.AuthenticationService()
    token_data = auth_service.get_auth_token(username, password)

    if not token_data:
        return ResponseBuilder.error(
            {"error": "Invalid credentials or authentication failed"},
            status.HTTP_401_UNAUTHORIZED,
        )

    return ResponseBuilder.success(token_data)


@api_view(["POST"])
@permission_classes([AllowAny])
def get_auth_token_with_api_keys_view(request):
    """
    Get authentication token for a user using API keys.

    This endpoint uses the application's API keys to generate an auth token for a specific user.
    Useful for server-side authentication or widget integration.

    Required Body Parameters:
        - username (str): User's email or username

    Returns:
        Response: API response containing access token info,
                  or an error if the username is invalid or not found.
    """
    username = request.data.get("username")

    if not username:
        return ResponseBuilder.error(
            {"error": "Username is required"}, status.HTTP_400_BAD_REQUEST
        )

    auth_service = OutsetaService.AuthenticationService()
    token_data = auth_service.get_auth_token_with_api_keys(username)

    if not token_data:
        return ResponseBuilder.error(
            {"error": "Invalid username or authentication failed"},
            status.HTTP_401_UNAUTHORIZED,
        )

    return ResponseBuilder.success(token_data)
