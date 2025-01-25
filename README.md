# automate_Email_process-
1. Overview
  This script automates the process of sending emails with attachments to specific recipients based on file names in a directory. It supports handling empty files by sending a     notification email with a pre-defined message. The script retrieves configuration details, including recipient mappings, SMTP settings, and email templates, from a     config.properties file.
2. Features
  Dynamic Recipient Mapping: Reads recipient email addresses and CCs from the configuration file.
  File Handling: Scans a directory for files and processes them based on their last modified timestamps.
  Customizable Email Content: Supports appending a signature from the configuration file.
  Error Handling: Captures errors during the email-sending process.
  Scheduling with Cron: Designed to be scheduled as a cron job for automation.
3. Key Components
  Configuration File (config.properties):
  Stores SMTP details, sender credentials, directory path, and recipient mappings.
  Python Script (script.py):
  The main logic for sending emails based on files.
  Cron Job:
  Automates the script execution at scheduled intervals.
4. Execution Flow
  Initialization:
    Load configuration from config.properties.
  Recipient Mapping:
    Map file names to recipient email addresses (To/CC).
  File Processing:
    Scan the directory for files, sort them by the latest modified timestamp, and check their sizes.
  Email Construction:
    Prepare the email content, append the signature, and attach the file if applicable.
  Email Sending:
    Use the smtplib module to send emails via the configured SMTP server.
  Error Logging:
    Log and print errors if email sending fails.
