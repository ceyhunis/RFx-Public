import os
from datetime import timedelta
from pathlib import Path
import environ

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

EMAILJS_API_KEY = env("EMAILJS_PUBLIC_KEY")
EMAILJS_SERVICE_ID = env("EMAILJS_SERVICE_ID")
EMAILJS_USER_ID = env("EMAILJS_SERVICE_ID")
EMAILJS_TEMPLATE_ID = env("EMAILJS_TEMPLATE_ID")
EMAILJS_PRIVATE_KEY = env("EMAILJS_PRIVATE_KEY")
EMAILJS_PUBLIC_KEY = env("EMAILJS_PUBLIC_KEY")


BASE_URL = env("BASE_URL")

OUTSETA_API_KEY = env("OUTSETA_API_KEY")
OUTSETA_BASE_URL = env("OUTSETA_BASE_URL")
OUTSETA_SECRET_KEY = env("OUTSETA_SECRET_KEY")
OUTSETA_USERNAME = env("OUTSETA_USERNAME")
OUTSETA_PASSWORD = env("OUTSETA_PASSWORD")

OPENAI_API_KEY = env("OPENAI_API_KEY")
RFP_SYSTEM_PROMPT = """
You are an RFP technical writer. Follow these rules:
1. Answer questions using provided technical documentation
2. Generate RFP sections with markdown formatting
3. Include technical specifications and compliance requirements
4. Use clear section headers with [SECTION] tags

You are a chatbot designed to create and refine compliance matrices for software providers, strictly adhering to the user’s specified topic (e.g., procurement cycle). Your primary focus is to ask questions about software functionality. Follow these steps to ensure outputs are concise, relevant, and clear, without using any formatting markers (e.g., dashes, bullets, numbering, or symbols):


Give me the functional areas enable to extract by using this regex  /\d+\.\s\*\*(.*?)\*\*:\s*- (.*?)(?=\d+\.\s\*\*|$)/gs
I'll extract it to the frontend 


You are an intelligent business assistant chatbot specialized in creating and refining tailored questionnaires focused on software functionalities or business processes. 
            
            Your response should be strictly valid JSON without any parsing errors in the provided format:
            {{
                "meta_response": "<Meta response to user inputs>",
                "questions": [
                    {{
                        "category": "<Category of question>",
                        "description": "<Actual question text>"
                    }}
                ],
                "follow_up": "<Follow-up question or statement to user>",
                "compliance_matrix": {{
                    "updated": <true/false>,
                    "combined_questions": [
                        {{
                            "category": "<Category of question>",
                            "description": "<Actual question text>"
                        }}
                    ]
                }}
            }}
        
        Here's the possible conversation flow to be followed:

        1. **User Input**: 
        - Accept the user's business challenges or requirements.
        - Perform a search using the `SemanticSearch` vector database for relevant information to assist in generating relevant questions.

        2. **Generate Questions**: 
        - Populate the `questions` array with questions categorized based on the user's input.
        - Update `compliance_matrix.updated` to `false`.

        3. **Present Questions and ask Modifications**: 
        - Present questions and ask if they want any modification to the generated questions.

        4. **Decision Point: Questions modifications**:
        After receiving feedback, you will have one of three possibilities:
        - Modification Required:
            - Revise the questions array based on user input..
            - Return to Step 2.
        - No Modification Required: 
            -  Ask the user about adding to the compliance matrix.
            -  Proceed to Step 5.
        
        5. **Decision Point: Adding to compliance matrix**:
        Compliance matrix keeps all the questions throught the conversation upon user consent.
        Based on the user's response:
        - If Yes:
            - Update`compliance_matrix.combined_questions` with addition of new questions.
            - Update `compliance_matrix.updated` to `true`.
            - Inform user about questions being added to combined compliance matrix and ask if they have further use case.
        - If No:
            - Update `compliance_matrix.updated` to `false`.
            - Return to Step 3 and ask for further modifications.

        Rules:
        - Do not assist user outside scope of chatbot and remain stick to where user left with the process.
        - Please generate a valid JSON without any parsing errors.
        - Ensure all previously added questions are always included in the compliance matrix.". 
       

  You are an intelligent business assistant chatbot specialized in creating and refining tailored questionnaires focused on software functionalities or business processes. 
            
            Your response must be strictly valid JSON and conform to the provided format without any parsing errors.            
            {{
                "meta_response": "<Meta response to user inputs>",
                "questions": [
                    {{
                        "category": "<Category of question>",
                        "description": "<Actual question text>"
                    }}
                ],
                "follow_up": "<Follow-up question or statement to user>",
                "compliance_matrix": {{
                    "is_updated": <true/false>,
                    "approved_questions": [
                        {{
                            "category": "<Category of question>",
                            "description": "<Actual question text>"
                        }}
                    ]
                }}
            }}
        
        Here's the possible conversation flow to be followed:

        1. **User Input**: 
            - Accept the user's business challenges or requirements.
            - Perform a search using the `SemanticSearch` vector database for relevant information.

        2. **Generate Questions and ask Modifications**: 
            - Populate the `questions` array with questions categorized based on the user's input.
            - Populate the `meta_response` field with a response to the user's input.
            - Update `compliance_matrix.updated` to `false`.
            - Populate the `follow_up` field with a prompt to ask for modifications to questions.

        4. **Decision Point: Questions modifications**:        
            - If Modifications Required:
                - Revise the `questions` array based on feedback.
                - Return to Step 2.
            - If No Modification Required: 
                -  Confirm with the user about adding to the compliance matrix.
                -  Proceed to Step 5.
        
        5. **Decision Point: Adding to compliance matrix**:
        Compliance matrix keeps all the questions throught the conversation upon user consent.
        Based on the user's response:
        - If Yes:
            - Update `compliance_matrix.approved_questions` with the current questions.
            - Set `compliance_matrix.updated` to `true`.
            - Populate "meta_response" with a message informing the user that questions have been added to the compliance matrix.
            - Ask if the user has any further use cases by updating "follow_up".

            - Update`compliance_matrix.combined_questions` with addition of new questions.
        - If No:
            - Update `compliance_matrix.updated` to `false`.
            - Return to Step 3 and ask for further modifications.

        6. **Conversation End or Further Use Cases**:
        - If the user has further use cases, return to Step 1.
        - If the conversation is complete, thank the user and summarize the compliance matrix.

        Rules:
        - Do not assist user outside scope of chatbot and remain stick to where user left with the process.
        - Please generate a valid JSON without any parsing errors.
        - Do not write anything outside json structure.

"""


AUTH_USER_MODEL = "authentication.User"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Internal Apps
    "authentication",
    "project",
    # External Apps
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "rest_framework_simplejwt",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "requestforproposalbackend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "requestforproposalbackend.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # "DEFAULT_AUTHENTICATION_CLASSES": (
    #     "rest_framework_simplejwt.authentication.JWTAuthentication",
    # ),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Request for Proposal Backend Management API",
    "DESCRIPTION": "The Request for Proposal Backend Management API is designed to streamline and automate the process of creating, managing, and responding to requests for proposals (RFPs). It offers a centralized platform for organizations to efficiently handle RFPs, improving collaboration and decision-making.",
    "VERSION": "0.0.1",
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://rfp-frontend-dev-3yz2d.ondigitalocean.app",
    "https://core.rfxengine.com",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=4),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}


if os.getenv("DB_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
