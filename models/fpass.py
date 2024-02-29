import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string


def send_reset_password_email(user_id, email):
  # Sender's email and password
  sender_email = "me@abdelrahman-nasr.tech"
  sender_password = "Cat9199@"  # Replace with the actual password

  # Email content
  subject = "Reset Your Password"

  reset_link = f"http://127.0.0.1:30/reset_password/{user_id}"
  print(reset_link,email)
  # HTML content for a more stylized email
  html_body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f7f7f7;
                text-align: center;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 60%;
                margin: 0 auto;
                padding: 40px;
                background-color: #fff;
                border-radius: 15px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                font-size: 28px;
                margin-bottom: 20px;
            }}
            p {{
                color: #555;
                line-height: 1.6em;
                font-size: 16px;
                margin-bottom: 15px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
                text-decoration: none;
                background-color: #4caf50;
                color: #fff;
                border-radius: 8px;
                transition: background-color 0.3s;
            }}
            .button:hover {{
                background-color: #45a049;
            }}
            .footer {{
                margin-top: 30px;
                color: #777;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Password Reset</h1>
            <p>Hello,</p>
            <p>We received a request to reset your password. Click the button below to reset it:</p>
            <a class="button" href="{reset_link}" target="_blank">Reset Your Password</a>
            <p>If you didn't request a password reset, please ignore this email.</p>
            <p class="footer">Best regards,<br>Your Company Name</p>
        </div>
    </body>
    </html>
    """

  # Create the MIME object
  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = email
  message["Subject"] = subject

  # Attach the HTML body to the email
  message.attach(MIMEText(html_body, "html"))

  # Connect to the SMTP server
  with smtplib.SMTP("smtp.abdelrahman-nasr.tech", 587) as server:
    server.starttls()  # Use this line if using the STARTTLS protocol
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, email, message.as_string())

  print(f"Reset password email sent successfully to {email}")
