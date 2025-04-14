from enum import IntEnum
import logging
from functools import wraps
from typing import Optional, Dict, Any
import requests
from django.conf import settings


def handle_api_errors(func):
    """Decorator to handle API errors consistently"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"API Error in {func.__name__}: {str(e)}")
            return None

    return wrapper


logger = logging.getLogger(__name__)


class OutsetaService:
    # API endpoint constants
    ENDPOINTS = {
        "PEOPLE": "people",
        "ACCOUNTS": "accounts",
        "DEALS": "deals",
        "ACTIVITIES": "activities",
    }

    # Common HTTP status codes
    HTTP_STATUS = {
        "OK": [200, 204],
        "CREATED": 201,
        "BAD_REQUEST": 400,
        "NOT_FOUND": 404,
        "SERVER_ERROR": 500,
    }

    def __init__(self):
        self._init_credentials()
        self._init_urls()

    def _init_credentials(self):
        """Initialize API credentials"""
        self.api_key = getattr(settings, "OUTSETA_API_KEY", None)
        self.secret_key = getattr(settings, "OUTSETA_SECRET_KEY", None)

    def _init_urls(self):
        """Initialize API URLs"""
        self.base_url = getattr(
            settings, "OUTSETA_BASE_URL", "https://api.outseta.com/v1/"
        )
        self.base_url = self.base_url.rstrip("/") + "/"

    def get_headers(self, is_client_auth=False, token=None):
        """
        Generate headers for Outseta API requests

        Args:
            is_client_auth (bool): Whether to use client-side authentication
            token (str): Bearer token for client-side authentication

        Returns:
            dict: Headers for API request
        """
        headers = {"Content-Type": "application/json"}

        if is_client_auth and token:
            headers["Authorization"] = token
        else:
            headers["Authorization"] = f"Outseta {self.api_key}:{self.secret_key}"

        return headers

    def make_request(
        self, endpoint, method="GET", data=None, params=None, headers=None
    ):
        """
        Make a request to the Outseta API

        Args:
            endpoint (str): API endpoint to call
            method (str): HTTP method (GET, POST, PUT, DELETE)
            data (dict): Data to send in the request body
            params (dict): URL parameters
            headers (dict, optional): Custom headers to include in the request

        Returns:
            Response object
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Use custom headers if provided, otherwise use default authentication
        request_headers = headers or self.get_headers()
        if headers and "Content-Type" not in headers:
            request_headers["Content-Type"] = "application/json"

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=request_headers, params=params)
            elif method.upper() == "POST":
                response = requests.post(
                    url, headers=request_headers, json=data, params=params
                )
            elif method.upper() == "PUT":
                response = requests.put(
                    url, headers=request_headers, json=data, params=params
                )
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=request_headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response

        except Exception as e:
            logging.error(f"API Error: {str(e)}")
            return None

    def get_client_auth_token(self, username, password):
        """
        Get client-side authentication token using username and password

        Args:
            username (str): Outseta username
            password (str): Outseta password

        Returns:
            str: Bearer token for client-side authentication
        """
        url = f"{self.base_url.rstrip('/')}/tokens"

        payload = f"username={username}&password={password}"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()
            token_data = response.json()
            return f"bearer {token_data['access_token']}"
        except Exception as e:
            # Log the error or handle it as needed
            return None

    class ServiceBase:
        def __init__(self, service_name):
            self.outseta_service = OutsetaService()
            self.service_name = service_name

        def get_service_endpoint(self, resource=None, resource_id=None):
            """
            Build the service endpoint path

            Args:
                resource (str): Resource name (e.g., 'people')
                resource_id (str): Resource ID for specific resource

            Returns:
                str: Endpoint path
            """
            endpoint = f"{self.service_name}"

            if resource:
                endpoint = f"{endpoint}/{resource}"

                if resource_id:
                    endpoint = f"{endpoint}/{resource_id}"

            return endpoint

        def make_service_request(
            self, resource=None, resource_id=None, method="GET", data=None, params=None
        ):
            """
            Make a request to a specific service endpoint

            Args:
                resource (str): Resource name
                resource_id (str): Resource ID
                method (str): HTTP method
                data (dict): Request data
                params (dict): URL parameters

            Returns:
                Response object or parsed JSON
            """
            endpoint = self.get_service_endpoint(resource, resource_id)
            return self.outseta_service.make_request(endpoint, method, data, params)

    ##################################################################################################################
    ##################################################################################################################
    # ---------------------------CRM SERVICE------------------------------
    ##################################################################################################################
    ##################################################################################################################

    class CRMService(ServiceBase):
        ENDPOINTS = {
            "PEOPLE": "people",
            "ACCOUNTS": "accounts",
            "DEALS": "deals",
            "ACTIVITIES": "activities",
        }

        def __init__(self):
            super().__init__("crm")
            self._init_token()

        def _init_token(self):
            """Initialize authentication token"""
            try:
                self.token = self.outseta_service.get_client_auth_token(
                    settings.OUTSETA_USERNAME, settings.OUTSETA_PASSWORD
                )
            except Exception as e:
                logging.error(f"Failed to get token: {str(e)}")
                self.token = None

        # -------------------------------------------------------------------------------------------  PEOPLE

        def get_all_people(self):
            """
            Get all people from Outseta CRM

            Returns:
                dict: JSON response containing people data or None if request fails
            """
            response = self.make_service_request(resource="people")
            if response:
                return response.json()
            return None

        def get_person_by_uid(self, person_uid):
            """
            Get a specific person from Outseta CRM by their UID

            Args:
                person_uid (str): The unique identifier of the person

            Returns:
                dict: JSON response containing person data or None if request fails
            """
            response = self.make_service_request(
                resource="people", resource_id=person_uid
            )
            if response:
                return response.json()
            return None

        def add_person(self, data):
            """
            Add a new person to Outseta CRM

            Args:
            data (dict): Data of the person to add

            Returns:
            dict: JSON response containing the added person data or None if request fails
            """
            response = self.make_service_request(
                resource="people", method="POST", data=data
            )
            if response:
                return response.json()
            return None

        def update_person(self, person_uid, data):
            """
            Update an existing person in Outseta CRM

            Args:
                person_uid (str): The unique identifier of the person
                data (dict): Updated data of the person

            Returns:
                dict: JSON response containing the updated person data or None if request fails
            """
            response = self.make_service_request(
                resource="people", resource_id=person_uid, method="PUT", data=data
            )
            if response:
                return response.json()
            return None

        def delete_person(self, person_uid):
            """
            Delete a person from Outseta CRM

            Args:
                person_uid (str): The unique identifier of the person

            Returns:
                bool: True if deletion was successful, False otherwise
            """
            response = self.make_service_request(
                resource="people", resource_id=person_uid, method="DELETE"
            )
            return response is not None

        def set_temporary_password(self, person_uid, temporary_password):
            """
            Sets a temporary password for a user

            Args:
                person_uid (str): The unique identifier of the user
                temporary_password (str): The temporary password to be set

            Returns:
                bool: True if successful, False otherwise
            """
            try:
                # First check if token exists
                if not self.token:
                    logging.error("Token not found")
                    return False

                # Validate required parameters
                if not person_uid or not temporary_password:
                    logging.error("Invalid parameters")
                    return False

                response = self.make_service_request(
                    resource="people",
                    resource_id=f"{person_uid}/setTemporaryPassword",
                    method="PUT",
                    data={"temporaryPassword": temporary_password},
                )

                # Check response
                if not response:
                    logging.error("API did not respond")
                    return False

                if hasattr(response, "status_code") and response.status_code != 200:
                    logging.error(f"API returned error: {response.status_code}")
                    return False

                return True

            except Exception as e:
                logging.error(f"Error setting temporary password: {str(e)}")
                return False

        def initiate_password_reset(self, parent_url, email):
            """
            Initiates password reset process for the specified email address.

            Args:
                parent_url (str): URL to redirect to the password reset page (sent as query parameter).
                email (str): Email address of the user to reset password.

            Returns:
                dict: JSON response containing API return data, or None if request fails.
            """
            params = {"parentUrl": parent_url}
            data = {"Email": email}
            response = self.make_service_request(
                resource="people/forgotPassword",
                method="POST",
                data=data,
                params=params,
            )
            if response:
                return response.json()
            return None

        def send_confirmation_email_to_primary_person(self, account_uid):
            """
            Sends confirmation email to the primary person for the specified account.

            Args:
                account_uid (str): The unique identifier of the account.

            Returns:
                bool: True if successful, False otherwise.
            """
            try:
                response = self.make_service_request(
                    resource="accounts",
                    resource_id=f"{account_uid}/send-confirmation-email",
                    method="PUT",
                )
                if response and response.status_code in (200, 204):
                    return True
                else:
                    error_message = (
                        response.text if response else "No response received"
                    )
                    logging.error(f"Failed to send confirmation email: {error_message}")
                    return False
            except Exception as e:
                logging.error(f"Error sending confirmation email: {str(e)}")
                return False

        def send_confirmation_email_to_specific_person(self, account_uid, person_uid):
            """
            Sends confirmation email to a specific person in the specified account.

            Args:
                account_uid (str): The unique identifier of the account.
                person_uid (str): The unique identifier of the person to send the confirmation email to.

            Returns:
                bool: True if successful, False otherwise.
            """
            try:
                params = {"personUid": person_uid}
                response = self.make_service_request(
                    resource="accounts",
                    resource_id=f"{account_uid}/send-confirmation-email",
                    method="PUT",
                    params=params,
                )
                if response and response.status_code in (200, 204):
                    return True
                else:
                    error_message = (
                        response.text if response else "No response received"
                    )
                    logging.error(
                        f"Failed to send confirmation email to specified person: {error_message}"
                    )
                    return False
            except Exception as e:
                logging.error(
                    f"Error sending confirmation email to specified person: {str(e)}"
                )
                return False

        def send_confirmation_email_to_all(self, account_uid):
            """
            Sends confirmation email to all people in the account.
            This is done by sending personUid="*" as a query parameter.

            Args:
                account_uid (str): The unique identifier of the account.

            Returns:
                bool: True if successful, False otherwise.
            """
            try:
                params = {"personUid": "*"}
                response = self.make_service_request(
                    resource="accounts",
                    resource_id=f"{account_uid}/send-confirmation-email",
                    method="PUT",
                    params=params,
                )
                if response and response.status_code in (200, 204):
                    return True
                else:
                    error_message = (
                        response.text if response else "No response received"
                    )
                    logging.error(
                        f"Failed to send confirmation email to all people: {error_message}"
                    )
                    return False
            except Exception as e:
                logging.error(
                    f"Error sending confirmation email to all people: {str(e)}"
                )
                return False

        # -------------------------------------------------------------------------------------------  ACCOUNTS

        def get_account(self, account_uid):
            """
            Retrieve all the information related to an account.

            Args:
                account_uid (str): The unique identifier of the account.

            Returns:
                dict: JSON response containing account data or None if request fails.
            """
            response = self.make_service_request(
                resource="accounts", resource_id=account_uid, method="GET"
            )
            if response:
                return response.json()
            return None

        def get_all_accounts(self):
            """
            Retrieve all account information from Outseta.

            Returns:
                dict: JSON response containing account data or None if request fails.
            """
            response = self.make_service_request(resource="accounts", method="GET")
            if response:
                return response.json()
            return None

        def get_accounts_by_stage(self, account_stage):
            """
            Retrieve account information filtered by account stage.

            Args:
                account_stage (str): Account stage to filter by (e.g., "2" for trialing accounts).

            Returns:
                dict: JSON response containing account data or None if request fails.
            """
            params = {"AccountStage": account_stage}
            response = self.make_service_request(
                resource="accounts", method="GET", params=params
            )
            if response:
                return response.json()
            return None

        def add_account_with_existing_person(self, data):
            """
            Add a new account with an existing person.

            Args:
                data (dict): Account data containing existing person information.
                            (Example: The Person object within PersonAccount should contain "Uid".)

            Returns:
                dict: JSON response containing the added account data or None if request fails.
            """
            response = self.make_service_request(
                resource="accounts", method="POST", data=data
            )
            if response:
                return response.json()
            return None

        def add_account_with_new_person(self, data, send_confirmation_email=False):
            """
            Add a new account with a new person.

            Args:
                data (dict): Account data containing new person information.
                            (Example: The Person object within PersonAccount should contain "Email", "FirstName", and "LastName".)
                send_confirmation_email (bool): Whether to send a confirmation email when adding the account.
                                                Controlled by the query parameter "sendConfirmationEmail".

            Returns:
                dict: JSON response containing the added account data or None if request fails.
            """
            params = {"sendConfirmationEmail": str(send_confirmation_email).lower()}
            response = self.make_service_request(
                resource="accounts", method="POST", data=data, params=params
            )
            if response:
                return response.json()
            return None

        def add_account_with_subscription(self, data):
            """
            Add a new account with subscription.
            Endpoint: POST /crm/accounts
            Body includes Subscriptions field.
            """
            response = self.make_service_request(
                resource="accounts", method="POST", data=data
            )
            if response:
                return response.json()
            return None

        def add_membership(self, account_uid, data, send_welcome_email=None):
            """
            Add a new person or an existing person to an existing account.
            Endpoints:
              - POST /crm/accounts/{account_uid}/memberships?sendWelcomeEmail={true/false} for new person
              - POST /crm/accounts/{account_uid}/memberships for existing person
            """
            endpoint = f"accounts/{account_uid}/memberships"
            params = {}
            if send_welcome_email is not None:
                params["sendWelcomeEmail"] = str(send_welcome_email).lower()
            response = self.outseta_service.make_request(
                endpoint, method="POST", data=data, params=params
            )
            if response:
                return response.json()
            return None

        def update_account(self, account_uid, data):
            """
            # PUT Update account
            Update account information. Any property included in the JSON schema will be updated.
            Endpoint: PUT /crm/accounts/{account_uid}
            """
            response = self.make_service_request(
                resource="accounts", resource_id=account_uid, method="PUT", data=data
            )
            if response:
                return response.json()
            return None

        def cancel_account(self, account_uid, data):
            """
            # PUT Cancel account
            Add a cancellation request to an account. The account must be in subscribing stage.
            Endpoint: PUT /crm/accounts/cancellation/{account_uid}
            """
            response = self.make_service_request(
                resource="accounts/cancellation",
                resource_id=account_uid,
                method="PUT",
                data=data,
            )
            if response:
                return response.json()
            return None

        def remove_cancellation(self, account_uid):
            """
            # PUT Remove cancellation
            Remove a previous cancellation request.
            Endpoint: PUT /crm/accounts/removecancellation/{account_uid}
            """
            response = self.make_service_request(
                resource="accounts/removecancellation",
                resource_id=account_uid,
                method="PUT",
                data={},
            )
            if response:
                try:
                    # If response is empty, return empty dict.
                    return response.json() if response.content else {}
                except Exception:
                    return {}
            return None

        def update_person_account_membership(self, account_uid, membership_uid, data):
            """
            # PUT Update person account membership
            Update an account membership. This method is used to change the primary contact of an account.
            Endpoint: PUT /crm/accounts/{account_uid}/memberships/{membership_uid}
            """
            endpoint = f"crm/accounts/{account_uid}/memberships/{membership_uid}"
            response = self.outseta_service.make_request(
                endpoint, method="PUT", data=data
            )
            if response:
                return response.json()
            return None

        def delete_account(self, account_uid):
            """
            # DELETE Delete account
            Delete an account record.
            Endpoint: DELETE /crm/accounts/{account_uid}
            """
            response = self.make_service_request(
                resource="accounts", resource_id=account_uid, method="DELETE"
            )
            return response is not None

        def remove_person_from_account(self, account_uid, membership_uid):
            """
            # DELETE Remove person from account
            Remove a person from an account.
            Note: You cannot remove the primary contact of an account.
            Endpoint: DELETE /crm/accounts/{account_uid}/memberships/{membership_uid}
            """
            endpoint = f"accounts/{account_uid}/memberships/{membership_uid}"
            response = self.outseta_service.make_request(endpoint, method="DELETE")
            return response is not None

        @handle_api_errors
        def extend_trial(self, account_uid, trial_end_date):
            """
            Extend the trial period for an account.

            Args:
                account_uid (str): The unique identifier of the account.
                trial_end_date (str): The new trial end date in YYYY-MM-DD format.

            Returns:
                dict: JSON response containing the account data with extended trial,
                      or None if the operation fails.
            """
            endpoint = f"crm/accounts/extendtrial/{account_uid}/{trial_end_date}"
            response = self.outseta_service.make_request(endpoint, method="PUT")
            return response.json() if response and response.ok else None

        # -------------------------------------------------------------------------------------------  ACTIVITIES

        def get_all_activities(self, params):
            """
            # GET Get all activities
            Retrieves all the activities filtered by provided query parameters.

            Args:
                params (dict): Query parameters
                    - ActivityType: For example, 100 (AccountCreated)
                    - EntityType: For example, 1 (Account)
                    - offset: Page offset (e.g., 0)
                    - orderBy: Example "ActivityDateTime DESC"

            Returns:
                dict: JSON response containing activities data or None if request fails
            """
            response = self.make_service_request(
                resource="activities", method="GET", params=params
            )
            if response:
                return response.json()
            return None

        def add_custom_activity(self, data):
            """
            # POST Add custom activity
            Record a custom activity for an account, person, or deal.

            Args:
                data (dict): Activity data including:
                    - Title: Activity title
                    - Description: Activity description
                    - ActivityData: Additional information
                    - EntityType: Related entity type (1: Account, 2: Person, 3: Deal)
                    - EntityUid: UID of the related entity

            Returns:
                dict: JSON response containing the created activity or None if request fails
            """
            response = self.make_service_request(
                resource="activities/customactivity", method="POST", data=data
            )
            if response:
                return response.json()
            return None

        # -------------------------------------------------------------------------------------------  DEALS

        def get_all_deals(self, params=None):
            """
            GET Get all deals
            Retrieves all the deals associated with your account.
            """
            response = self.outseta_service.make_request(
                "deals", method="GET", params=params
            )
            if response:
                return response.json()
            return None

        def get_deal(self, deal_uid, params=None):
            """
            GET Get deal
            Retrieves one deal associated with your account.
            """
            endpoint = f"deals/{deal_uid}"
            response = self.outseta_service.make_request(
                endpoint, method="GET", params=params
            )
            if response:
                return response.json()
            return None

        def add_deal(self, data):
            """
            POST Add deal
            Adds a new deal.
            """
            response = self.outseta_service.make_request(
                "deals", method="POST", data=data
            )
            if response:
                return response.json()
            return None

        def update_deal(self, deal_uid, data):
            """
            PUT Update deal
            Updates the specified deal.
            """
            endpoint = f"deals/{deal_uid}"
            response = self.outseta_service.make_request(
                endpoint, method="PUT", data=data
            )
            if response:
                return response.json()
            return None

        def delete_deal(self, deal_uid):
            """
            DELETE Delete deal
            Deletes the specified deal.
            """
            endpoint = f"deals/{deal_uid}"
            response = self.outseta_service.make_request(endpoint, method="DELETE")
            return response is not None

    ##################################################################################################################
    ##################################################################################################################
    # ------------------------MARKETING SERVICE---------------------------
    ##################################################################################################################
    ##################################################################################################################

    class MarketingService(ServiceBase):
        """Service class to handle Outseta Marketing API operations"""
        def __init__(self):
            super().__init__(service_name="marketing")
            
            

        def get_list_subscribers(self, list_id):
            """
            Retrieves all subscribers for a given email list.
            """
            try:
                response = self.outseta_service.make_request(
                    f"/email/lists/{list_id}/subscriptions", method="GET"
                )
                return response.json() if response and response.ok else None
            except Exception as e:
                logger.error(f"Error getting list subscribers: {str(e)}")
                return None

        def add_new_subscriber(self, list_id, person_data, send_welcome_email=False):
            """
            Subscribes a new person to an email list.
            """
            payload = {
                "EmailList": {"Uid": list_id},
                "Person": person_data,
                "SendWelcomeEmail": str(send_welcome_email).lower(),
            }

            try:
                response = self.outseta_service.make_request(
                    f"/email/lists/{list_id}/subscriptions", method="POST", data=payload
                )
                return response is not None and response.ok
            except Exception as e:
                logger.error(f"Error adding new subscriber: {str(e)}")
                return False

        def add_existing_subscriber(
            self, list_id, person_uid, send_welcome_email=False
        ):
            """
            Subscribes an existing person to an email list.
            """
            payload = {
                "EmailList": {"Uid": list_id},
                "Person": {"Uid": person_uid},
                "SendWelcomeEmail": str(send_welcome_email).lower(),
            }

            try:
                response = self.outseta_service.make_request(
                    f"/email/lists/{list_id}/subscriptions", method="POST", data=payload
                )
                return response is not None and response.ok
            except Exception as e:
                logger.error(f"Error adding existing subscriber: {str(e)}")
                return False

        def remove_subscriber(self, list_id, subscription_uid):
            """
            Removes a subscriber from an email list.
            """
            try:
                response = self.outseta_service.make_request(
                    f"/email/lists/{list_id}/subscriptions/{subscription_uid}",
                    method="DELETE",
                )
                return response is not None and response.ok
            except Exception as e:
                logger.error(f"Error removing subscriber: {str(e)}")
                return False

    ##################################################################################################################
    ##################################################################################################################
    # -----------------------SUPPORT SERVICE------------------------------
    ##################################################################################################################
    ##################################################################################################################

    class CaseStatus(IntEnum):
        """Enum for case statuses"""

        OPEN = 1
        CLOSED = 2

    class CaseSource(IntEnum):
        """Enum for case sources"""

        WEBSITE = 1
        EMAIL = 2
        FACEBOOK = 3
        TWITTER = 4

    class SupportService(ServiceBase):
        def __init__(self):
            super().__init__(service_name="support")

        """Service class to handle Outseta Support API operations"""

        @handle_api_errors
        def get_all_cases(self):
            """
            Retrieves all support cases.
            """
            response = self.outseta_service.make_request("/support/cases", method="GET")
            return response.json() if response and response.ok else None

        def get_cases_by_person_uid(self, person_uid):
            """Get all cases for a specific person by UID"""
            try:
                response = self.outseta_service.make_request(
                    "/support/cases",
                    method="GET",
                    params={"FromPerson.Uid": person_uid},
                )
                return response.json() if response and response.ok else None
            except Exception as e:
                logger.error(f"Error getting cases by person UID: {str(e)}")
                return None

        def get_cases_by_person_email(self, email):
            """Get all cases for a specific person by email"""
            try:
                response = self.outseta_service.make_request(
                    "/support/cases", method="GET", params={"FromPerson.Email": email}
                )
                return response.json() if response and response.ok else None
            except Exception as e:
                logger.error(f"Error getting cases by person email: {str(e)}")
                return None

        def add_case(self, case_data, send_auto_responder=True):
            """Add a new support case"""
            try:
                params = {"sendAutoResponder": str(send_auto_responder).lower()}
                response = self.outseta_service.make_request(
                    "/support/cases", method="POST", data=case_data, params=params
                )
                return response is not None and response.ok
            except Exception as e:
                logger.error(f"Error adding case: {str(e)}")
                return False

        def add_client_response(self, case_uid, comment):
            """Add a client response to an existing case"""
            try:
                response = self.outseta_service.make_request(
                    f"/support/cases/{case_uid}/clientresponse/{comment}", method="POST"
                )
                return response is not None and response.ok
            except Exception as e:
                logger.error(f"Error adding client response: {str(e)}")
                return False

        def add_agent_reply(self, case_uid, agent_name, comment):
            """
            Adds an agent reply to a support case.
            """
            payload = {
                "AgentName": agent_name,
                "Case": {"Uid": case_uid},
                "Comment": comment,
            }

            try:
                response = self.outseta_service.make_request(
                    f"/support/cases/{case_uid}/replies", method="POST", data=payload
                )
                return response is not None and response.ok
            except Exception as e:
                logger.error(f"Error adding agent reply: {str(e)}")
                return False

    ##################################################################################################################
    ##################################################################################################################
    # -----------------------BILLING SERVICE------------------------------
    ##################################################################################################################
    ##################################################################################################################

    class BillingService(ServiceBase):
        """Service class to handle Outseta Billing API operations"""

        def __init__(self):
            super().__init__(service_name="billing")

        # ------------------------------------------------------------------------------------------- PLAN FAMILIES

        @handle_api_errors
        def get_all_plan_families(self):
            """
            Get all plan families from Outseta Billing API

            Returns:
                dict: JSON response containing plan families data or None if request fails
            """
            response = self.outseta_service.make_request(
                "billing/planfamilies", method="GET"
            )
            return response.json() if response and response.ok else None

        # ------------------------------------------------------------------------------------------- PLANS
        @handle_api_errors
        def get_all_plans(self):
            """
            Get all plans from Outseta Billing API

            Returns:
                dict: JSON response containing plans data or None if request fails
            """
            response = self.outseta_service.make_request("billing/plans", method="GET")
            return response.json() if response and response.ok else None

        # ------------------------------------------------------------------------------------------- ADD-ONS
        @handle_api_errors
        def add_usage_for_addon(self, usage_data):
            """
            Add usage entry for an add-on that bills for usage

            Args:
                usage_data (dict): Usage data containing UsageDate, Amount, and SubscriptionAddOn

            Returns:
                dict: JSON response containing the added usage data or None if request fails
            """
            response = self.outseta_service.make_request(
                "billing/usage", method="POST", data=usage_data
            )
            return response.json() if response and response.ok else None

        # ------------------------------------------------------------------------------------------- DISCOUNTS

        @handle_api_errors
        def add_discount_coupon(self, discount_data):
            """
            Add a new discount coupon

            Args:
                discount_data (dict): Discount coupon data containing properties like:
                    - UniqueIdentifier
                    - Name
                    - IsActive
                    - AmountOff or PercentOff
                    - Duration
                    - DurationInMonths (optional)
                    - MaxRedemptions (optional)
                    - RedeemBy (optional)
                    - DiscountCouponPlans (optional)

            Returns:
                dict: JSON response containing the created discount coupon or None if request fails
            """
            response = self.outseta_service.make_request(
                "billing/discountcoupons", method="POST", data=discount_data
            )
            return response.json() if response and response.ok else None

        # ------------------------------------------------------------------------------------------- SUBSCRIPTIONS

        @handle_api_errors
        def get_subscription(self, subscription_uid):
            """
            Get subscription details by UID

            Args:
                subscription_uid (str): Unique identifier for the subscription

            Returns:
                dict: JSON response containing subscription data or None if request fails
            """
            response = self.outseta_service.make_request(
                f"billing/subscriptions/{subscription_uid}", method="GET"
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def compute_charge_summary(
            self, subscription_data, as_of="now"
        ):  # = POST Add first time subscription (preview)
            """
            Preview the charge for a subscription (first time or renewal)

            This method is used to see what the initial or renewal invoice would look like
            if an account were to register with this subscription. Returns an invoice preview.

            Args:
                subscription_data (dict): Subscription data containing:
                    - Plan (object): With Uid of the plan
                    - BillingRenewalTerm (int): 1=Monthly, 2=Yearly, 3=Quarterly, 4=OneTime
                    - Account (object): Can be empty for new accounts
                as_of (str): When to calculate the charge - "now" (default) or "renewal"

            Returns:
                dict: JSON response containing invoice preview data or None if request fails
            """
            params = {"asOf": as_of} if as_of != "now" else None
            response = self.outseta_service.make_request(
                "billing/subscriptions/compute-charge-summary",
                method="POST",
                data=subscription_data,
                params=params,
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def add_first_time_subscription(self, subscription_data):
            """
            Add first time subscription to an account

            This method is used when adding a subscription to an account for the first time.
            Returns an invoice object with information about the amount outstanding.

            Args:
                subscription_data (dict): Subscription data containing:
                    - Plan (object): With Uid of the plan
                    - BillingRenewalTerm (int): 1=Monthly, 2=Yearly, 3=Quarterly, 4=OneTime
                    - Account (object): With Uid of the account

            Returns:
                dict: JSON response containing invoice details or None if request fails
            """
            response = self.outseta_service.make_request(
                "billing/subscriptions/firsttimesubscription",
                method="PUT",
                data=subscription_data,
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def add_first_time_subscription_with_addons(self, subscription_data):
            """
            Add first time subscription with add-ons to an account

            This method is used when adding a subscription with add-ons to an account for the first time.
            Returns an invoice object with information about the amount outstanding.

            Args:
                subscription_data (dict): Subscription data containing:
                    - Plan (object): With Uid of the plan
                    - BillingRenewalTerm (int): 1=Monthly, 2=Yearly, 3=Quarterly, 4=OneTime
                    - Account (object): With Uid of the account
                    - SubscriptionAddOns (array): List of add-ons, each containing AddOn object with Uid

            Returns:
                dict: JSON response containing invoice details or None if request fails
            """
            # Bu endpoint de aslında firsttimesubscription ile aynıdır,
            # sadece request body'de SubscriptionAddOns alanı eklenmiştir.
            response = self.outseta_service.make_request(
                "billing/subscriptions/firsttimesubscription",
                method="PUT",
                data=subscription_data,
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def change_subscription_preview(self, subscription_uid, subscription_data):
            """
            Preview changes to an existing subscription

            Args:
                subscription_uid (str): Unique identifier for the subscription
                subscription_data (dict): Updated subscription data

            Returns:
                dict: JSON response containing invoice preview data or None if request fails
            """
            response = self.outseta_service.make_request(
                f"billing/subscriptions/{subscription_uid}/changesubscriptionpreview",
                method="PUT",
                data=subscription_data,
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def change_subscription(self, subscription_uid, subscription_data):
            """
            Change an existing subscription

            Args:
                subscription_uid (str): Unique identifier for the subscription
                subscription_data (dict): Updated subscription data

            Returns:
                dict: JSON response containing updated subscription data or None if request fails
            """
            response = self.outseta_service.make_request(
                f"billing/subscriptions/{subscription_uid}/changesubscription",
                method="PUT",
                data=subscription_data,
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def set_subscription_upgrade_required(self, subscription_uid, upgrade_data):
            """
            Mark a subscription as requiring an upgrade

            Args:
                subscription_uid (str): Unique identifier for the subscription
                upgrade_data (dict): Data containing upgrade requirements:
                    - Uid (str): Subscription UID
                    - NewRequiredQuantity (int, optional): New required quantity
                    - IsPlanUpgradeRequired (bool): Whether an upgrade is required
                    - PlanUpgradeRequiredMessage (str): Message to show to the user

            Returns:
                dict: JSON response containing updated subscription data or None if request fails
            """
            response = self.outseta_service.make_request(
                f"billing/subscriptions/{subscription_uid}/setsubscriptionupgraderequired",
                method="PUT",
                data=upgrade_data,
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def add_addon_to_subscription(self, addon_data):
            """
            Add an add-on to a subscription

            Args:
                addon_data (dict): Data containing:
                    - AddOn (object): With Uid
                    - BillingRenewalTerm (int): 1=Monthly, 2=Yearly, 3=Quarterly, 4=OneTime
                    - Quantity (int): Quantity of the add-on
                    - Subscription (object): With Uid

            Returns:
                dict: JSON response containing the add-on data or None if request fails
            """
            response = self.outseta_service.make_request(
                "billing/subscriptionaddons", method="POST", data=addon_data
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def add_discount_to_subscription(self, subscription_uid, discount_uid):
            """
            Add a discount to a subscription

            Args:
                subscription_uid (str): Unique identifier for the subscription
                discount_uid (str): Unique identifier for the discount coupon

            Returns:
                dict: JSON response containing the updated subscription data or None if request fails
            """
            endpoint = (
                f"billing/subscriptions/{subscription_uid}/discounts/{discount_uid}"
            )
            response = self.outseta_service.make_request(endpoint, method="POST")
            return response.json() if response and response.ok else None

        # ------------------------------------------------------------------------------------------- INVOICES

        @handle_api_errors
        def add_new_invoice(self, invoice_data):
            """
            Create a new ad-hoc invoice for an account

            Args:
                invoice_data (dict): Invoice data containing:
                    - Subscription (object): With Uid
                    - InvoiceDate (str): Date in ISO format
                    - InvoiceLineItems (array): List of line items with Description and Amount

            Returns:
                dict: JSON response containing the created invoice data or None if request fails
            """
            response = self.outseta_service.make_request(
                "billing/invoices", method="POST", data=invoice_data
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def get_transactions_by_account(self, account_uid):
            """
            Get all transactions for a specific account

            Args:
                account_uid (str): Unique identifier for the account

            Returns:
                dict: JSON response containing the transactions data or None if request fails
            """
            response = self.outseta_service.make_request(
                f"billing/transactions/{account_uid}", method="GET"
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def add_invoice_payment(self, payment_data):
            """
            Add a payment to an invoice

            Args:
                payment_data (dict): Payment data containing:
                    - Account (object): With Uid of the account
                    - Invoice (object): With Uid of the invoice
                    - Amount (number): Payment amount (negative value for refunds)

            Returns:
                dict: JSON response containing transaction data or None if request fails
            """
            response = self.outseta_service.make_request(
                "billing/transactions/payment", method="POST", data=payment_data
            )
            return response.json() if response and response.ok else None

        # ------------------------------------------------------------------------------------------- PAYMENT INFORMATION

        @handle_api_errors
        def update_payment_information(self, payment_info_data):
            """
            Update payment information for an account

            Args:
                payment_info_data (dict): Payment information containing:
                    - Account (object): With Uid
                    - CustomerToken (str): Customer token from payment provider
                    - NameOnCard (str): Name on the payment card
                    - PaymentToken (str): Payment method token from payment provider

            Returns:
                dict: JSON response containing updated payment information or None if request fails
            """
            response = self.outseta_service.make_request(
                "billing/paymentinformation", method="POST", data=payment_info_data
            )
            return response.json() if response and response.ok else None

    ##################################################################################################################
    ##################################################################################################################
    # -----------------------USER PROFILE SERVICE------------------------
    ##################################################################################################################
    ##################################################################################################################

    class UserProfileService(ServiceBase):
        """Service class to handle Outseta User Profile API operations"""

        def __init__(self, auth_token=None):
            super().__init__(service_name="")  # Base URL is used directly
            self.auth_token = auth_token

        def get_profile(self):
            """
            Get the profile information of the authenticated user

            This method requires user authentication token

            Returns:
                dict: JSON response containing user profile data or None if request fails
            """
            if not self.auth_token:
                logger.error("Auth token is required for getting user profile")
                return None

            headers = {"Authorization": self.auth_token}
            try:
                response = self.outseta_service.make_request(
                    "profile", method="GET", headers=headers
                )
                return response.json() if response and response.ok else None
            except Exception as e:
                logger.error(f"Error getting user profile: {str(e)}")
                return None

        @handle_api_errors
        def update_profile(self, profile_data):
            """
            Update the profile information of the authenticated user

            This method requires user authentication token and the profile data must include
            the UID that matches the authenticated user.

            Args:
                profile_data (dict): User profile data including:
                    - Email (str): User's email
                    - FirstName (str): User's first name
                    - LastName (str): User's last name
                    - MailingAddress (dict, optional): User's mailing address
                    - Uid (str): Must match the authenticated user's UID

            Returns:
                dict: JSON response containing updated user profile data or None if request fails
            """
            if not self.auth_token:
                logger.error("Auth token is required for updating user profile")
                return None

            headers = {"Authorization": self.auth_token}
            response = self.outseta_service.make_request(
                "profile", method="PUT", data=profile_data, headers=headers
            )
            return response.json() if response and response.ok else None

        @handle_api_errors
        def update_password(self, existing_password, new_password):
            """
            Update the password for the authenticated user

            This method requires user authentication token

            Args:
                existing_password (str): User's current password
                new_password (str): User's new password

            Returns:
                dict: JSON response confirming password update or None if request fails
            """
            if not self.auth_token:
                logger.error("Auth token is required for updating password")
                return None

            headers = {"Authorization": self.auth_token}
            data = {"ExistingPassword": existing_password, "NewPassword": new_password}

            response = self.outseta_service.make_request(
                "profile/password", method="PUT", data=data, headers=headers
            )
            # Usually returns empty response on success
            return {} if response and response.ok else None


##################################################################################################################
##################################################################################################################
# -----------------------AUTHENTICATION SERVICE---------------------
##################################################################################################################
##################################################################################################################


    class AuthenticationService(ServiceBase):
        """Service class to handle Outseta Authentication API operations"""

        def __init__(self):
            super().__init__(service_name="")  # Base URL is used directly

        @handle_api_errors
        def get_auth_token(self, username, password):
            """
            Get authentication token using username and password

            This method is for user authentication. It should be called server-side to keep
            credentials secure.

            Args:
                username (str): User's email or username
                password (str): User's password

            Returns:
                dict: JSON response containing access token, token type and expiration,
                    or None if authentication fails
            """
            url = f"{self.outseta_service.base_url.rstrip('/')}/tokens"

            payload = f"username={username}&password={password}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}

            try:
                response = requests.post(url, headers=headers, data=payload)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Error getting auth token: {str(e)}")
                return None

        @handle_api_errors
        def get_auth_token_with_api_keys(self, username):
            """
            Get authentication token for a user using API keys

            This method allows generating an authentication token for a specific user
            using the API keys of the application. Useful for server-side authentication
            or widget integration.

            Args:
                username (str): User's email or username

            Returns:
                dict: JSON response containing access token, token type and expiration,
                    or None if authentication fails
            """
            url = f"{self.outseta_service.base_url.rstrip('/')}/tokens"

            # Create the authorization header using API keys
            auth_header = (
                f"Outseta {self.outseta_service.api_key}:{self.outseta_service.secret_key}"
            )
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": auth_header,
            }

            payload = f"username={username}"

            try:
                response = requests.post(url, headers=headers, data=payload)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                logger.error(f"Error getting auth token with API keys: {str(e)}")
                return None
