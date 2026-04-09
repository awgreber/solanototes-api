import os
import uuid
from typing import Optional

import anthropic
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="SolanoTotes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── MODELS ──
class BookingRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    package: str
    delivery_date: str
    city: str

class PaymentRequest(BaseModel):
    booking_id: str
    amount_cents: int
    email: str

# ── HEALTH ──
@app.get("/")
def root():
    return {"status": "SolanoTotes API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

# ── AVAILABILITY ──
@app.get("/availability")
def check_availability(date: str, package: Optional[str] = None):
    # Stub — will connect to Airtable
    return {"date": date, "available": True, "message": "Date is available"}

# ── BOOKING ──
@app.post("/booking")
def create_booking(req: BookingRequest):
    # Stub — will connect to Airtable
    booking_id = str(uuid.uuid4())[:8].upper()
    return {
        "booking_id": booking_id,
        "status": "confirmed",
        "message": f"Booking confirmed for {req.delivery_date}"
    }

# ── PAYMENT ──
@app.post("/payment")
def create_payment(req: PaymentRequest):
    # Stub — will connect to Stripe
    return {
        "status": "pending",
        "message": "Payment integration coming soon"
    }

# ── CASSIE CHAT ──
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

@app.post("/cassie")
def cassie_chat(req: ChatMessage):
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=500,
        system="""You are Cassie, the friendly AI assistant for SolanoTotes — a reusable moving bin rental service in Solano County, CA.

You help customers:
- Learn about pricing ($75 studio, $95 2-bed, $125 3-bed, $149 4-bed+)
- Check availability
- Book a delivery
- Answer questions about the service

Service area: Vacaville, Fairfield, Suisun City, Dixon, Benicia, Vallejo, Rio Vista, Winters.
Every order includes delivery, pickup, and 2 dollies.
Rental period: up to 1 week.

Be warm, concise, and helpful. If they want to book, collect: name, email, phone, package, delivery date, city.""",
        messages=[{"role": "user", "content": req.message}]
    )

    return {"response": response.content[0].text}
