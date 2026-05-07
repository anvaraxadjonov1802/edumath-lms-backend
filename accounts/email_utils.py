import requests
from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(to_email: str, code: str, is_resend: bool = False) -> bool:
    subject = (
        "EduMath LMS yangi tasdiqlash kodi"
        if is_resend
        else "EduMath LMS email tasdiqlash kodi"
    )

    text_message = (
        "EduMath LMS verification code\n\n"
        f"Sizning tasdiqlash kodingiz: {code}\n\n"
        "Kod 15 daqiqa amal qiladi."
    )

    html_message = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #0f172a;">
        <h2 style="margin-bottom: 8px;">EduMath LMS</h2>

        <p>Assalomu alaykum!</p>
        <p>Sizning tasdiqlash kodingiz:</p>

        <div style="
            display: inline-block;
            padding: 14px 22px;
            background: #eef2ff;
            border-radius: 12px;
            color: #4f46e5;
            font-size: 32px;
            font-weight: 700;
            letter-spacing: 6px;
        ">
            {code}
        </div>

        <p style="margin-top: 18px;">Ushbu kod 15 daqiqa amal qiladi.</p>

        <p style="color: #64748b; font-size: 14px;">
            Agar siz EduMath LMS platformasida ro‘yxatdan o‘tmagan bo‘lsangiz,
            ushbu xabarni e’tiborsiz qoldiring.
        </p>
    </div>
    """

    if settings.EMAIL_PROVIDER == "resend":
        return send_with_resend(
            to_email=to_email,
            subject=subject,
            html_message=html_message,
            text_message=text_message,
        )

    send_mail(
        subject=subject,
        message=text_message,
        from_email=None,
        recipient_list=[to_email],
        fail_silently=False,
    )
    return True


def send_with_resend(
    to_email: str,
    subject: str,
    html_message: str,
    text_message: str,
) -> bool:
    if not settings.RESEND_API_KEY:
        raise ValueError("RESEND_API_KEY is not configured")

    if not settings.RESEND_FROM_EMAIL:
        raise ValueError("RESEND_FROM_EMAIL is not configured")

    payload = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "html": html_message,
        "text": text_message,
    }

    if settings.RESEND_REPLY_TO:
        payload["reply_to"] = settings.RESEND_REPLY_TO

    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://api.resend.com/emails",
        json=payload,
        headers=headers,
        timeout=15,
    )

    response.raise_for_status()
    return True