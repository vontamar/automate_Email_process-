import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def get_sorted_files(directory):
    """Get files in the directory sorted by last modified date."""
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    sorted_files = sorted(files, key=os.path.getmtime, reverse=True)
    return sorted_files

def send_email_with_attachments(smtp_server, port, sender_email, sender_password, recipient_email, cc_email, files):
    """Send an email with the sorted file list and attachments, or an error message if files are empty."""
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['CC'] = cc_email  # Add CC field
    msg['Subject'] = "Sorted Files from C Drive"

    # Check if files exist and have content
    if not files:
        body = "Error: No files found to attach."
        msg.attach(MIMEText(body, 'plain'))
    else:
        body = "Attached are the files sorted by their last modified date from the C drive."
        msg.attach(MIMEText(body, 'plain'))

        # Attach each file
        for file in files[:5]:  # Limit to first 5 files for practicality
            if os.path.exists(file) and os.path.getsize(file) > 0:
                with open(file, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file)}')
                msg.attach(part)
            else:
                body = f"Error: File {os.path.basename(file)} is empty or does not exist."
                msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Directory to scan (C drive)
    directory = "C:/Amar/scriptfiles"

    # Get sorted files
    sorted_files = get_sorted_files(directory)
    print("Sorted files:", sorted_files)

    # Email configuration
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "rkomireddy.90@gmail.com"
    sender_password = "pnwx pnze saxs uodt"
    recipient_email = "vontamar@gmail.com"
    cc_email = "amarnadhj2ee@gmail.com"  # CC recipient

    # Send email with sorted files or error message
    send_email_with_attachments(smtp_server, port, sender_email, sender_password, recipient_email, cc_email, sorted_files)
