import os
import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Load configuration from the properties file
CONFIG_FILE = "config.properties"
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Directory containing the files
DIRECTORY = config.get("General", "directory")

# Email configuration
SMTP_SERVER = config.get("EmailConfig", "smtp_server")
SMTP_PORT = config.getint("EmailConfig", "smtp_port")
SENDER_EMAIL = config.get("EmailConfig", "sender_email")
SENDER_PASSWORD = config.get("EmailConfig", "sender_password")
SIGNATURE = config.get("EmailConfig", "signature")

def load_recipient_mapping():
    # Load recipients from the configuration file
    recipient_mapping = {}
    for file_name in config.options("Recipients"):
        recipient_info = config.get("Recipients", file_name).split(",")
        recipient_mapping[file_name] = {"to": recipient_info[0].strip(), "cc": recipient_info[1].strip()}
        # print(f"Loaded mapping for {file_name}: {recipient_mapping[file_name]}")
    return recipient_mapping

def send_email(recipient, cc, subject, body, attachment_path=None):
    try:
        # Create a multipart message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Cc"] = cc
        msg["Subject"] = subject

        # Attach the email body with the signature
        full_body = body + "\n"+ SIGNATURE.replace('\\n', '\n')
        msg.attach(MIMEText(full_body, "plain"))

        # Attach the file if provided
        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(attachment_path)}",
                )
                msg.attach(part)

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, [recipient] + [cc], msg.as_string())
            print(f"Email sent to {recipient} with CC {cc} and attachment {attachment_path if attachment_path else 'no attachment'}")

    except Exception as e:
        print(f"Failed to send email to {recipient} with CC {cc}: {e}")

if __name__ == "__main__":
    # Load recipient mapping
    file_recipient_mapping = load_recipient_mapping()

    # List all files in the directory and sort by the latest modified timestamp
    files = sorted(
        os.listdir(DIRECTORY),
        key=lambda f: os.path.getmtime(os.path.join(DIRECTORY, f)),
        reverse=True
    )

    for file_name in files:
        file_path = os.path.join(DIRECTORY, file_name)

        # Extract file name without extension
        file_name_without_ext = os.path.splitext(file_name)[0]

        # Check if the file has a mapped recipient
        mapping = file_recipient_mapping.get(file_name)


        if mapping:
            # Check if the file is empty
            if os.path.getsize(file_path) == 0:
                send_email(
                    recipient=mapping["to"],
                    cc=mapping["cc"],
                    subject=f"{file_name_without_ext}",
                    body=f"No data available."
                )

            else:
                send_email(
                    recipient=mapping["to"],
                    cc=mapping["cc"],
                    subject=f"{file_name_without_ext}",
                    body=f"Please find the attached file.",
                    attachment_path=file_path
                )
        else:
            print(f"No recipient found for file: {file_name}")
