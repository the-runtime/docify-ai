from typing import Any
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from docifyai.core import logger

logger = logger.Logger(__name__)


def send_limit_exceeded(api_key: str, user_name: str, email: str):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    sender = {"name": "docify-ai", "email": "docify@tabish.tech"}
    reply_to = {"name": "Tabish", "email": "tabishhassan1oo@gmail.com"}

    subject = "Limit Exceeded"
    html_content = f"""<html><body>
                <h1>Document generation successful </h1>
                <p>You can only generate maximum of three documents.
                Request to increase limit <a href=mailto:tabishhassan1oo@gmail.com>tabishhassan1oo@gmail.com </a></p>
            </body></html>
            """
    to = [{"email": email, "name": user_name}]
    # params = {"parameter": "My param value", "subject": "New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, reply_to=reply_to,
                                                   subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info(api_response)
    except ApiException as e:
        logger.error("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


def added_to_queue(api_key: str, user_name: str, email: str):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender = {"name": "docify-ai", "email": "docify@tabish.tech"}
    reply_to = {"name": "Tabish", "email": "tabishhassan1oo@gmail.com"}
    subject = "Request added to queue"
    html_content = f"""<html><body>
                    <h1>Your doc generation work is in queue</h1>
                    <p>We will let you know when it is completed.
                    <body></html>
                """
    to = [{"email": email, "name": user_name}]
    # params = {"parameter": "My param value", "subject": "New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, reply_to=reply_to,
                                                   subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info(api_response)
    except ApiException as e:
        logger.error("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


def send_mail_to_user(is_success: bool, api_key: str, user_name: str, user_email: str, file_name: str = ""):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = api_key

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    sender = {"name": "docify-ai", "email": "docify@tabish.tech"}
    reply_to = {"name": "Tabish", "email": "tabishhassan1oo@gmail.com"}
    if is_success:
        file_url = f"https://docify.tabish.tech/api/getdoc/?blob_name={file_name}"
        subject = "Document successfully generated"
        html_content = f"""<html><body>
            <h1>Document generation successful </h1>
            <p><a href={file_url}>Download document </a>or copy and paste the below link in browser</p>
        <a href="{file_url}"> {file_url} </a>
        </body></html>
        """
    else:
        subject = "Document generation unsuccessful"
        html_content = """
            <html><body>
                <h1>Document generation unsuccessful </h1>
                <p>Document generation failed, retry after some time or reply to this mail if problem persists.</p>
            </body></html>
            """
    to = [{"email": user_email, "name": user_name}]
    # params = {"parameter": "My param value", "subject": "New Subject"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, reply_to=reply_to,
                                                   subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info(api_response)
    except ApiException as e:
        logger.error("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
