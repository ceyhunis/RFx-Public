import requests
import logging
from django.conf import settings


class EmailJSService:
    def __init__(self):
        self.service_id = settings.EMAILJS_SERVICE_ID
        self.template_id = settings.EMAILJS_TEMPLATE_ID  # Eğer varsa genel template ID
        self.url = settings.BASE_URL
        self.api_url = "https://api.emailjs.com/api/v1.0/email/send"
        self.public_key = settings.EMAILJS_PUBLIC_KEY  # Public Key eklendi
        self.private_key = settings.EMAILJS_PRIVATE_KEY  # Add private key
        self.logger = logging.getLogger(__name__)

    def send_email(self, to_email, template_id, template_params):
        email_data = {
            "service_id": self.service_id,
            "template_id": template_id,
            "user_id": self.public_key,  # Public Key / User ID parametresi eklendi
            "accessToken": self.private_key,  # Include private key
            "template_params": template_params,
        }
        try:
            headers = {
                "Content-Type": "application/json",
            }

            self.logger.info(f"Sending EmailJS request to template: {template_id}")
            self.logger.debug(f"Email data: {email_data}")

            response = requests.post(self.api_url, json=email_data, headers=headers)

            if response.status_code != 200:
                self.logger.error(
                    f"EmailJS API error: {response.status_code} - {response.text}"
                )
                return None

            response.raise_for_status()
            self.logger.info(
                f"Email sent successfully to {to_email} using template {template_id}"
            )
            return response

        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}", exc_info=True)
            return None

    def send_forget_password_email(self, name, token, email):
        template_id = "rfx_password_reset"
        template_params = {
            "to_email": email,
            "to_name": name,
            "link": f"{self.url}/forgot-password/new-password?token={token}&email={email}",
        }
        return self.send_email(email, template_id, template_params)

    def send_invitation_email(
        self, to_email, organization_name, inviter_name, hashed_token
    ):
        # First check if we're using a test/staging environment
        is_test_env = getattr(settings, "DEBUG", False)

        # Template ID'yi settings'ten alma deneyin
        template_id = getattr(settings, "EMAILJS_INVITE_TEMPLATE_ID", "invite_member")
        fallback_template_id = getattr(
            settings, "EMAILJS_PASSWORD_RESET_TEMPLATE_ID", "rfx_password_reset"
        )

        template_params = {
            "to_email": to_email,
            "organization_name": organization_name,
            "inviter_name": inviter_name,
            "link": f"{self.url}/register?token={hashed_token}",  # Only token in the URL
            "to_name": to_email.split("@")[0],  # Basit bir fallback ad
        }

        # Try with the invite_member template first
        response = self.send_email(to_email, template_id, template_params)

        # If that fails and we're in a test environment, try with a fallback template
        if response is None and is_test_env:
            self.logger.warning(
                f"Using fallback template {fallback_template_id} for invitation email"
            )
            response = self.send_email(to_email, fallback_template_id, template_params)

        return response

    def send_proposal_email(self, to_email, template_params):
        template_id = "rfx_response_invitation"
        template_params = {
            "to_email": to_email,
            "to_name": "test",
            "link": f"{self.url}/response?id={0}",
        }
        return self.send_email(to_email, template_id, template_params)

    def send_welcome_email(self, to_email, name):
        template_id = "welcome_rfxengine"
        template_params = {"email": to_email, "name": name}
        return self.send_email(to_email, template_id, template_params)
