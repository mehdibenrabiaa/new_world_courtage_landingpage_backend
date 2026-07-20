import json
import urllib.request

from core.config import settings

INSURANCE_LABELS = {
    "vtc": "VTC",
    "taxi": "Taxi",
    "poids_lourd": "Poids lourd",
}


def notify_new_lead(name: str, phone: str, insurance_type: str | None):
    if not settings.WHATSAPP_PHONE_NUMBER_ID or not settings.WHATSAPP_ACCESS_TOKEN or not settings.WHATSAPP_NOTIFY_TO:
        return

    label = INSURANCE_LABELS.get(insurance_type, insurance_type or "—")
    text = f"Nouveau lead New World Courtage\n{name}\n{phone}\nType : {label}"

    url = f"https://graph.facebook.com/v20.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    body = json.dumps({
        "messaging_product": "whatsapp",
        "to": settings.WHATSAPP_NOTIFY_TO.lstrip("+"),
        "type": "text",
        "text": {"body": text},
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass  # best-effort — a notification failure shouldn't affect lead capture
