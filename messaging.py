
#App builder
#Wingman

#Home




#Credits
#30% more


#Meet Your Advisor

#User Avatar


#Preview

#Manage

#Republish
#Loading...
#$ cd /app && git diff HEAD -- backend/storage.py; ...
#Oct 31, 10:23 AM

#$ cd /app && API=$(grep REACT_APP_BACKEND_URL fron...
#Oct 31, 10:23 AM

#Took a screenshot
Screenshots
#Image 1
#Oct 31, 10:24 AM

$ cd /app/backend && set -a && . ./.env && set +a ...
Oct 31, 10:24 AM

$ cd /app && python3 -m py_compile backend/*.py ba...
Oct 31, 10:24 AM

Deployment finished
Oct 31, 10:29 AM
Edited
/app/memory/PRD.md
Oct 31, 10:25 AM

Source code download + Publish പ്രശ്നം പരിഹരിച്ചു

Code chat-ൽ വലിയ ഫയലുകൾ പകർപ്പത് പ്രായോഗികമല്ല (237 files, 5 MB) - പകരം Settings  Backup & Restore  Code download ബട്ടൺ ചേർത്തിട്ടുണ്ട്: മുഴുവൻ frontend + backend കോഡ് ഒരു ZIP ആയി (password/key ഇല്ലാതെ .env.example ഉൾപ്പെടെ) admin-ന് ഡൗൺലോഡ് ചെയ്യാം  Google Drive-ൽ സൂക്ഷിക്കുക. 237 ഫയലുകൾ ടെസ്റ്റുചെയ്‌തു, admin അല്ലാത്തവർക്ക് 401 എറർ ലഭിക്കും. ദയവായി കോഡ് എഡിറ്ററിൽ് ബ്രൗസ് ചെയ്ത് എഡിറ്റ് ചെയ്യുന്നതിൽ നിന്ന് മറികടക്കുക.
#:ശ്രദ്ധിക്കുക ഡാറ്റാബേസിൽ ഇപ്പോൾ വീടുകൾ/അംഗങ്ങൾ/payments 0 ആണ് - വീട് 001 ഒക്ടോബർ 3-നും 10-നും ഇടയിൽ ഡിലീറ്റായിട്ടുണ്ട് (ടെസ്റ്റ് ഡാറ്റ നീക്കം ചെയ്തതാണോ?). ആവശ്യമായി വന്നാൽ Settings Backup-ലെ ഒക്ടോബർ 3 സ്നാപ്ഷോട്ട് "Restore" ചെയ്ത് വീണ്ടെടുക്കാം.
നിങ്ങളുടെ ഉൾക്കാഴ്ചയും പരിശോധനകളും കൂടി ഘടിപ്പിച്ചുണ്ടാക്കിയ ശ്രമം മുന്നോട്ട് പോവാൻ സഹായകരമാകും. ദയവായി പുതിയ ലിങ്ക് സന്ദർശിച്ച് പ്രവർത്തനം പരിശോദിക്കുകയും, എന്തെങ്കിലും പ്രശ്‌നങ്ങൾ ഉണ്ടെങ്കിൽ അറിയിക്കുമെന്നുമാണ് അഭ്യർത്ഥിക്കുന്നത്.


Custom domain

Security audit
Oct 31, 10:25 AM




Agent Finished
Oct 31, 10:25 AM
sever.py,core.py,messaging.py

Oct 31, 10:28 AM

Viewing
3
paths
Oct 31, 10:28 AM

ഈ മൂന്ന് files-ഉം ഇപ്പോൾ പൂർണ്ണമായി restore ആയി server-ൽ പ്രവർത്തിക്കുന്നുണ്ട് (ഇവയാണ് നേരത്തെ ശൂന്യമായിപ്പോയത്). മുഴുവൻ code ഇതാ - ഇവ copy ചെയ്യാൻ മാത്രം; editor-ൽ cut/edit ചെയ്യരുത്.

1. backend/server.py
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import os
import asyncio
import logging
from datetime import datetime, timezone
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from core import client, db
from routes.auth_routes import router as auth_router, users_router
from routes.houses import router as houses_router
from routes.finance import router as finance_router
from routes.content import router as content_router
from routes.notifications import router as notifications_router, auto_reminder_loop
from routes.files import router as files_router
from routes.public import router as public_router
from routes.collections import router as collections_router
from routes.events import router as events_router, event_notify_loop
from routes.ledger import router as ledger_router
from routes.chat import router as chat_router
from routes.suggestions import router as suggestions_router
from routes.backup import router as backup_router, backup_loop
from routes.assistant import router as assistant_router
from storage import init_storage
from seed import seed_admin, ensure_member_numbers, ensure_login_ids

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Mahal App API")
api_router = APIRouter(prefix="/api")


@api_router.get("/")
async def root():
    return {"message": "Mahal App API"}


BUILD_ID = os.environ.get("BUILD_ID") or datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


@api_router.get("/version")
async def version():
    """Changes on every backend start/deploy — the app uses it to drop stale caches on old phones."""
    return {"build": BUILD_ID}


api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(houses_router)
api_router.include_router(finance_router)
api_router.include_router(content_router)
api_router.include_router(notifications_router)
api_router.include_router(files_router)
api_router.include_router(public_router)
api_router.include_router(collections_router)
api_router.include_router(events_router)
api_router.include_router(ledger_router)
api_router.include_router(chat_router)
api_router.include_router(suggestions_router)
api_router.include_router(backup_router)
api_router.include_router(assistant_router)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await db.users.create_index("phone", unique=True)
    await db.houses.create_index("house_no", unique=True)
    await db.members.create_index("house_id")
    await db.payments.create_index("house_id")
    await db.payments.create_index("months")
    await db.donations.create_index("fund_id")
    await db.members.create_index("member_no")
    await db.otps.create_index("phone")
    await db.users.create_index("login_id", sparse=True)
    await db.login_attempts.create_index("key")
    await db.book_entries.create_index("book_id")
    await db.chat_messages.create_index("created_at")
    await seed_admin()
    await ensure_member_numbers()
    await ensure_login_ids()
    asyncio.create_task(auto_reminder_loop())
    asyncio.create_task(event_notify_loop())
    asyncio.create_task(backup_loop())
    try:
        init_storage()
        logger.info("Storage initialized")
    except Exception as exc:
        logger.error("Storage init failed: %s", exc)
    logger.info("Startup complete")


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
2. backend/core.py
import os
import uuid
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, Request, Depends
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.environ["MONGO_URL"])
db = client[os.environ["DB_NAME"]]

JWT_ALGORITHM = "HS256"
NO_ID = {"_id": 0}


def new_id() -> str:
    return str(uuid.uuid4())


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def current_month() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, os.environ["JWT_SECRET"], algorithm=JWT_ALGORITHM)


async def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, os.environ["JWT_SECRET"], algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user = await db.users.find_one({"id": payload["sub"]}, {"_id": 0, "password_hash": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


async def require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


async def can_finance(user: dict) -> bool:
    if user.get("role") == "admin":
        return True
    s = await db.settings.find_one({"key": "main"}, {"_id": 0, "finance_manager_id": 1}) or {}
    manager = s.get("finance_manager_id")
    return bool(manager) and user["id"] == manager


async def ledger_scope(user: dict) -> str:
    """all = admin/treasurer; salath = appointed Salath committee member; none = read-only."""
    if await can_finance(user):
        return "all"
    s = await db.settings.find_one({"key": "main"}, {"_id": 0, "salath_manager_ids": 1}) or {}
    return "salath" if user["id"] in (s.get("salath_manager_ids") or []) else "none"


async def require_finance(user: dict = Depends(get_current_user)) -> dict:
    if not await can_finance(user):
        raise HTTPException(status_code=403, detail="Only the appointed treasurer can manage collections")
    return user


async def next_receipt_no(kind: str) -> str:
    settings = await db.settings.find_one({"key": "main"}, {"_id": 0}) or {}
    prefix = settings.get("receipt_prefix", "RCT")
    if kind == "donation":
        prefix = settings.get("donation_prefix", "DON")
    counter = await db.counters.find_one_and_update(
        {"key": kind}, {"$inc": {"seq": 1}}, upsert=True, return_document=True
    )
    return f"{prefix}-{counter['seq']:05d}"


def months_between(start: str, end: str) -> list:
    sy, sm = map(int, start.split("-"))
    ey, em = map(int, end.split("-"))
    out = []
    y, m = sy, sm
    while (y, m) <= (ey, em):
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


async def house_units(house: dict) -> dict:
    """Dues are charged per paying member: head + every second member (working man 18+). Students / women / children pay nothing."""
    from routes.houses import classify
    subs = 0
    async for m in db.members.find({"house_id": house["id"]}, {"_id": 0, "name": 1, "relation": 1, "dob": 1, "gender": 1, "status": 1}):
        if classify(m, house)["member_type"] == "sub":
            subs += 1
    return {"units": 1 + subs, "sub": subs}


def member_filter(member_id):
    """member_id=None → whole house; 'head' → payments not tagged to a sub-member; else that member's own payments."""
    if member_id is None:
        return {}
    if member_id == "head":
        return {"$and": [{"$or": [{"member_id": {"$exists": False}}, {"member_id": None}, {"member_id": ""}]}]}
    return {"member_id": member_id}


async def house_dues(house: dict, member_id=None) -> dict:
    """Amount-based monthly dues (× paying members): any partial amount reduces the balance; months are covered in order.
    With member_id the share of one paying member (1 unit, his own payments) is returned."""
    start = house.get("start_month") or current_month()
    all_months = months_between(start, current_month())
    units = 1 if member_id else (await house_units(house))["units"]
    rate = float(house.get("subscription_amount", 0) or 0) * units
    paid_amount = 0.0
    async for p in db.payments.find({"house_id": house["id"], "$or": [{"type": "varisankhya"}, {"type": {"$exists": False}}], **member_filter(member_id)}, {"_id": 0, "amount": 1}):
        paid_amount += float(p.get("amount", 0) or 0)
    covered = int(paid_amount // rate) if rate > 0 else len(all_months)
    paid_months = all_months[:covered]
    pending = all_months[covered:] if rate > 0 else []
    due = len(all_months) * rate
    return {
        "pending_months": pending,
        "pending_count": len(pending),
        "pending_amount": max(0.0, due - paid_amount),
        "paid_months": paid_months,
        "paid_amount": paid_amount,
        "due_amount": due,
        "advance": max(0.0, paid_amount - due),
    }
3. backend/messaging.py
import os
import asyncio
import logging
from typing import Optional
from urllib.parse import quote
from core import db, new_id, now_iso

logger = logging.getLogger("messaging")


_provider_cache = {"at": 0.0, "value": None}


def _creds(settings: dict) -> dict:
    """Twilio credentials: Settings (entered by admin in the app) override .env."""
    return {
        "sid": (settings.get("twilio_sid") or os.environ.get("TWILIO_ACCOUNT_SID", "")).strip(),
        "token": (settings.get("twilio_token") or os.environ.get("TWILIO_AUTH_TOKEN", "")).strip(),
        "sms_from": (settings.get("twilio_sms_from") or os.environ.get("TWILIO_SMS_FROM", "")).strip(),
        "whatsapp_from": (settings.get("twilio_whatsapp_from") or os.environ.get("TWILIO_WHATSAPP_FROM", "")).strip(),
        "provider": settings.get("notify_provider") or "phone",
    }


def provider_status(settings: Optional[dict] = None) -> dict:
    c = _creds(settings or {})
    live = c["provider"] == "twilio" and bool(c["sid"] and c["token"])
    return {
        "mode": "live" if live else "phone",
        "provider": c["provider"],
        "sms_enabled": live and bool(c["sms_from"]),
        "whatsapp_enabled": live and bool(c["whatsapp_from"]),
        "configured": bool(c["sid"] and c["token"]),
    }


async def provider_status_async() -> dict:
    import time
    if time.time() - _provider_cache["at"] > 5 or _provider_cache["value"] is None:
        s = await db.settings.find_one({"key": "main"}, {"_id": 0, "twilio_sid": 1, "twilio_token": 1, "twilio_sms_from": 1, "twilio_whatsapp_from": 1, "notify_provider": 1}) or {}
        _provider_cache.update({"at": time.time(), "value": (provider_status(s), s)})
    return _provider_cache["value"]


def wa_link(to_e164: str, body: str) -> str:
    return f"https://wa.me/{to_e164.lstrip('+')}?text={quote(body)}"


def sms_link(to_e164: str, body: str) -> str:
    return f"sms:{to_e164}?body={quote(body)}"


def with_links(log: dict) -> dict:
    if log.get("to", "").startswith("+"):
        log["wa_link"] = wa_link(log["to"], log["body"])
        log["sms_link"] = sms_link(log["to"], log["body"])
    return log


def e164(phone: str) -> str:
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    if not digits:
        return ""
    if len(digits) == 10:
        return f"+91{digits}"
    return f"+{digits}"


def _twilio_send(to: str, body: str, channel: str, c: dict) -> str:
    from twilio.rest import Client
    client = Client(c["sid"], c["token"])
    if channel == "whatsapp":
        frm = c["whatsapp_from"] if c["whatsapp_from"].startswith("whatsapp:") else f"whatsapp:{c['whatsapp_from']}"
        msg = client.messages.create(from_=frm, to=f"whatsapp:{to}", body=body)
    else:
        msg = client.messages.create(from_=c["sms_from"], to=to, body=body)
    return msg.sid


async def send_message(to: str, body: str, channel: str, kind: str, ref: str = "", recipient_name: str = "", house_id: str = "") -> dict:
    to_e164 = e164(to)
    status, s = await provider_status_async()
    log = {
        "id": new_id(), "to": to_e164 or (to or ""), "recipient_name": recipient_name, "channel": channel,
        "kind": kind, "body": body, "ref": ref, "house_id": house_id, "status": "queued", "error": "", "provider_sid": "", "created_at": now_iso(),
    }
    if not to_e164:
        log.update({"status": "failed", "error": "No phone number"})
    elif status["mode"] == "live" and status.get(f"{channel}_enabled"):
        try:
            log["provider_sid"] = await asyncio.to_thread(_twilio_send, to_e164, body, channel, _creds(s))
            log["status"] = "sent"
        except Exception as exc:
            log.update({"status": "failed", "error": str(exc)[:300]})
            logger.warning("Twilio send failed: %s", exc)
    else:
        logger.info("[QUEUED %s] to %s: %s", channel.upper(), to_e164, body[:80])
    await db.messages.insert_one(log)
    log.pop("_id", None)
    return with_links(log)


SALAAM = "അസ്സലാമു അലൈക്കും"
SALAAM_KN = "ಅಸ್ಸಲಾಮು ಅಲೈಕುಂ"
LABELS_ML = {"varisankhya": "വരിസംഖ്യ", "eid_fitr": "ചെറിയ പെരുന്നാൾ", "eid_adha": "വലിയ പെരുന്നാൾ", "nabidinam": "നബിദിനം", "building": "Building Fund", "special": "പ്രത്യേക പിരിവ്", "auction": "ലേലം", "pledge": "വാഗ്ദാനം / മറ്റ്", "old_balance": "പഴയ ബാക്കി", "donation": "സംഭാവന"}
LABELS_KN = {"varisankhya": "ವರಿಸಂಖ್ಯೆ", "eid_fitr": "ಚಿಕ್ಕ ಪೆರುನ್ನಾಳ್", "eid_adha": "ದೊಡ್ಡ ಪೆರುನ್ನಾಳ್", "nabidinam": "ನಬಿದಿನ", "building": "Building Fund", "special": "ವಿಶೇಷ ಸಂಗ್ರಹ", "auction": "ಹರಾಜು", "pledge": "ವಾಗ್ದಾನ / ಇತರ", "old_balance": "ಹಳೆಯ ಬಾಕಿ", "donation": "ದೇಣಿಗೆ"}

# Message templates per notification language (settings.notify_language: ml | kn)
TXT = {
    "ml": {
        "address": "ബഹുമാനപ്പെട്ട മഹല്ല് അംഗം {who},", "son_of": " ({father}-ന്റെ മകൻ)", "sign": "ജസാക്കല്ലാഹ് ഖൈർ — {name}",
        "receipt": "{label}-ലേക്ക് ₹{amount}{period} {date}-ന് സ്വീകരിച്ചു. രസീത് നമ്പർ: {no}.", "head": "\n{label}: ആകെ ₹{due} · ഇതുവരെ അടച്ചത് ₹{paid} · ", "head_pending": "ബാക്കി ₹{pending}", "head_clear": "ഈ വക പൂർണ്ണമായി അടച്ചു ✔",
        "breakdown": "\nഇനി ബാക്കിയുള്ളത്:", "line": "\n• {label}: ₹{amount}", "all_clear": "\nനിങ്ങളുടെ കുടിശ്ശിക മുഴുവൻ അടച്ചു തീർത്തിരിക്കുന്നു. വളരെ നന്ദി! അല്ലാഹു അനുഗ്രഹിക്കട്ടെ.", "total_pending": "\nഎല്ലാ വകകളിലും കൂടി ഇനി ബാക്കി: ₹{total}",
        "balance": "വീട് {no} — നിങ്ങളുടെ ആകെ ബാക്കി ₹{amount} ({parts}). എത്രയും വേഗം അടച്ചു തീർക്കാൻ അഭ്യർത്ഥിക്കുന്നു.",
        "statement": "കമ്മിറ്റി പരിശോധിച്ച നിങ്ങളുടെ വീട് {no}-ന്റെ {year} വർഷത്തെ കണക്ക് ({date}):", "st_line": "\n• {label}: ആകെ ₹{due} · അടച്ചത് ₹{paid} · ബാക്കി ₹{pending}", "st_total": "\nആകെ അടച്ചത്: ₹{paid} · ആകെ ബാക്കി: ₹{pending}", "st_app": "\nApp-ൽ 'എന്റെ ബാക്കി' തുറന്ന് വിശദമായി കാണാം; QR scan ചെയ്ത് അടയ്ക്കാം.",
        "dues": "വീട് {no} — {n} മാസത്തെ വരിസംഖ്യ ({months}) ₹{amount} അടയ്ക്കാൻ ബാക്കിയുണ്ട്. എത്രയും വേഗം അടച്ചു തീർക്കാൻ അഭ്യർത്ഥിക്കുന്നു.",
        "ack": "₹{amount} ({label}) UPI payment വിവരം ലഭിച്ചു{ref}. ട്രഷറർ പരിശോധിച്ച് confirm ചെയ്ത ശേഷം രസീത് WhatsApp-ൽ ലഭിക്കും.",
        "reject": "₹{amount} ({label}) UPI payment വിവരം സ്ഥിരീകരിക്കാനായില്ല.{reason} ദയവായി ട്രഷററെ ബന്ധപ്പെടുക.", "reason": " കാരണം: {reason}",
    },
    "kn": {
        "address": "ಗೌರವಾನ್ವಿತ ಮಹಲ್ ಸದಸ್ಯ {who},", "son_of": " ({father} ಅವರ ಮಗ)", "sign": "ಜಝಾಕಲ್ಲಾಹು ಖೈರ್ — {name}",
        "receipt": "{label} ಗೆ ₹{amount}{period} {date} ರಂದು ಸ್ವೀಕರಿಸಲಾಗಿದೆ. ರಸೀದಿ ಸಂಖ್ಯೆ: {no}.", "head": "\n{label}: ಒಟ್ಟು ₹{due} · ಇದುವರೆಗೆ ಪಾವತಿ ₹{paid} · ", "head_pending": "ಬಾಕಿ ₹{pending}", "head_clear": "ಈ ಬಾಬ್ತು ಪೂರ್ಣ ಪಾವತಿಯಾಗಿದೆ ✔",
        "breakdown": "\nಇನ್ನೂ ಬಾಕಿ ಇರುವುದು:", "line": "\n• {label}: ₹{amount}", "all_clear": "\nನಿಮ್ಮ ಎಲ್ಲಾ ಬಾಕಿ ಪಾವತಿಯಾಗಿದೆ. ತುಂಬಾ ಧನ್ಯವಾದಗಳು! ಅಲ್ಲಾಹ್ ಆಶೀರ್ವದಿಸಲಿ.", "total_pending": "\nಎಲ್ಲಾ ಬಾಬ್ತುಗಳಲ್ಲಿ ಇನ್ನೂ ಬಾಕಿ: ₹{total}",
        "balance": "ಮನೆ {no} — ನಿಮ್ಮ ಒಟ್ಟು ಬಾಕಿ ₹{amount} ({parts}). ಆದಷ್ಟು ಬೇಗ ಪಾವತಿಸಿ ತೀರಿಸಲು ವಿನಂತಿ.",
        "statement": "ಸಮಿತಿ ಪರಿಶೀಲಿಸಿದ ನಿಮ್ಮ ಮನೆ {no} ರ {year} ವರ್ಷದ ಲೆಕ್ಕ ({date}):", "st_line": "\n• {label}: ಒಟ್ಟು ₹{due} · ಪಾವತಿ ₹{paid} · ಬಾಕಿ ₹{pending}", "st_total": "\nಒಟ್ಟು ಪಾವತಿ: ₹{paid} · ಒಟ್ಟು ಬಾಕಿ: ₹{pending}", "st_app": "\nಆಪ್‌ನಲ್ಲಿ 'ನನ್ನ ಬಾಕಿ' ತೆರೆದು ವಿವರ ನೋಡಿ; QR scan ಮಾಡಿ ಪಾವತಿಸಬಹುದು.",
        "dues": "ಮನೆ {no} — {n} ತಿಂಗಳ ವರಿಸಂಖ್ಯೆ ({months}) ₹{amount} ಪಾವತಿಸಲು ಬಾಕಿ ಇದೆ. ಆದಷ್ಟು ಬೇಗ ಪಾವತಿಸಿ ತೀರಿಸಲು ವಿನಂತಿ.",
        "ack": "₹{amount} ({label}) UPI ಪಾವತಿ ಮಾಹಿತಿ ಬಂದಿದೆ{ref}. ಖಜಾಂಚಿ ಪರಿಶೀಲಿಸಿ confirm ಮಾಡಿದ ನಂತರ ರಸೀದಿ WhatsApp-ನಲ್ಲಿ ಬರುತ್ತದೆ.",
        "reject": "₹{amount} ({label}) UPI ಪಾವತಿ ಮಾಹಿತಿ ದೃಢೀಕರಿಸಲಾಗಲಿಲ್ಲ.{reason} ದಯವಿಟ್ಟು ಖಜಾಂಚಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.", "reason": " ಕಾರಣ: {reason}",
    },
}


def msg_lang(settings: dict) -> str:
    return "kn" if (settings or {}).get("notify_language") == "kn" else "ml"


def tx(settings: dict, key: str, **kw) -> str:
    return TXT[msg_lang(settings)][key].format(**kw)


def label_for(settings: dict, typ: str) -> str:
    custom = next((h.get("name") for h in (settings or {}).get("custom_heads") or [] if isinstance(h, dict) and h.get("id") == typ), None)
    return custom or (LABELS_KN if msg_lang(settings) == "kn" else LABELS_ML).get(typ, typ)


def with_salaam(name: str, body: str, father: str = "", respectful: bool = True, settings: dict = None) -> str:
    """Every message starts with Salaam, then a respectful address ('ബഹുമാനപ്പെട്ട മഹല്ല് അംഗം <name> (<father>-ന്റെ മകൻ)' / Kannada), then the content."""
    head = body.lstrip()
    if head.startswith(SALAAM) or head.startswith(SALAAM_KN) or head.lower().startswith("assalamu"):
        return body
    salaam = SALAAM_KN if msg_lang(settings) == "kn" else SALAAM
    if not (name and name.strip()):
        return f"{salaam},\n{body}"
    who = name.strip() + (tx(settings, "son_of", father=father.strip()) if father and father.strip() else "")
    return f"{salaam},\n{tx(settings, 'address', who=who)}\n{body}" if respectful else f"{salaam} {who},\n{body}"


def sign(settings: dict) -> str:
    return "\n" + tx(settings, "sign", name=settings.get("short_name") or settings.get("mahal_name", "Mahal"))


def channels_for(setting: str) -> list:
    if setting == "both":
        return ["sms", "whatsapp"]
    return [setting or "whatsapp"]


async def sub_members_with_phone(house: dict) -> list:
    """Working adult sons (member_type 'sub') who have their own mobile — they get every house notification too."""
    from routes.houses import classify
    out = []
    async for m in db.members.find({"house_id": house.get("id", "")}, {"_id": 0}):
        m = classify(m, house)
        if m.get("member_type") == "sub" and (m.get("phone") or "").strip():
            out.append(m)
    return out


async def notify_house(house: dict, body: str, kind: str, ref: str = "", channel_setting: str = "whatsapp"):
    results = []
    s = await db.settings.find_one({"key": "main"}, {"_id": 0, "notify_language": 1}) or {}
    head_body = with_salaam(house.get("head_name", ""), body, house.get("father_name", ""), settings=s)
    subs = await sub_members_with_phone(house)
    for ch in channels_for(channel_setting):
        to = house.get("whatsapp") or house.get("phone") if ch == "whatsapp" else house.get("phone")
        sent_to = set()
        if to:
            sent_to.add(e164(to))
            results.append(await send_message(to, head_body, ch, kind, ref, house.get("head_name", ""), house.get("id", "")))
        for m in subs:
            if e164(m["phone"]) in sent_to:
                continue
            sent_to.add(e164(m["phone"]))
            results.append(await send_message(m["phone"], with_salaam(m.get("name", ""), body, settings=s), ch, kind, f"{ref}:{m['id']}" if ref else "", m.get("name", ""), house.get("id", "")))
    return results


async def statement_text(house: dict, settings: dict) -> str:
    """Committee-verified year statement sent when a house's account is released to the member."""
    from routes.collections import house_collections
    from datetime import date
    c = await house_collections(house, settings)
    heads = [(k, v) for k, v in c.items() if isinstance(v, dict) and v.get("kind") != "free" and (v.get("due", 0) > 0 or v.get("paid", 0) > 0)]
    text = tx(settings, "statement", no=house.get("house_no", ""), year=date.today().year, date=date.today().strftime("%d-%m-%Y"))
    text += "".join(tx(settings, "st_line", label=label_for(settings, k), due=f"{v['due']:.0f}", paid=f"{v['paid']:.0f}", pending=f"{v['pending']:.0f}") for k, v in heads)
    text += tx(settings, "st_total", paid=f"{sum(v['paid'] for _, v in heads):.0f}", pending=f"{c['total_pending']:.0f}")
    text += tx(settings, "all_clear") if c["total_pending"] <= 0 else ""
    return text + tx(settings, "st_app") + sign(settings)


async def receipt_text(house: dict, doc: dict, settings: dict):
    """Receipt notification; thanks the house when the whole balance is cleared."""
    from routes.collections import house_collections
    period = ", ".join(doc.get("months") or doc.get("years") or [])
    label = label_for(settings, doc.get("type", "varisankhya"))
    c = await house_collections(house, settings)
    head = c.get(doc.get("type", "varisankhya")) or {}
    period = f" {period}" if period else ""
    text = tx(settings, "receipt", label=label, amount=f"{doc['amount']:.0f}", period=period, date=doc["date"], no=doc["receipt_no"])
    if not house.get("statement_released"):
        # Committee has not released this house's statement yet — acknowledge the payment only, no balance figures.
        return await notify_house(house, text + sign(settings), "receipt", doc["id"], settings.get("notify_channel", "whatsapp"))
    if head.get("kind") != "free":
        text += tx(settings, "head", label=label, due=f"{head.get('due', 0):.0f}", paid=f"{head.get('paid', 0):.0f}")
        text += tx(settings, "head_pending", pending=f"{head['pending']:.0f}") if head.get("pending", 0) > 0 else tx(settings, "head_clear")
    if c["total_pending"] <= 0:
        text += tx(settings, "all_clear")
    else:
        text += tx(settings, "breakdown") + "".join(tx(settings, "line", label=label_for(settings, k), amount=f"{v['pending']:.0f}") for k, v in c.items() if isinstance(v, dict) and v.get("pending", 0) > 0)
        text += tx(settings, "total_pending", total=f"{c['total_pending']:.0f}")
    await notify_house(house, text + sign(settings), "receipt", doc["id"], settings.get("notify_channel", "whatsapp"))
ഇവ മൂന്നും മാത്രമല്ല - ബാക്കി 230+ files-ഉം (routes, frontend) Settings  Backup & Restore Code download button-ൽ ഒറ്റ ZIP ആയി കിട്ടും; അതാണ് മുഴുവൻ code സൂക്ഷിക്കാൻ എളുപ്പം.





