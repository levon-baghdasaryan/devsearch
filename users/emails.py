from django.template.loader import render_to_string
from django.core.mail import send_mail


def register_user_email(profile, from_email):
    subject = 'Welcome to DevSearch'
    message = f'''Hello {profile.username}!
Congratulations, you successfully registered on our platform.

If you did not create an account, no further action is required.

Best Regards,
DevSearch Team
            '''
    send_mail(
        subject=subject,
        html_message=render_to_string(
            'emails/register.html',
            context={'username': profile.username}
        ),
        message=message,
        from_email=from_email,
        recipient_list=[profile.email],
        fail_silently=False
    )
