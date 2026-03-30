from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="EduBot - EdTech Customer Support API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

SYSTEM_PROMPT = """You are EduBot, a friendly and knowledgeable customer support assistant for LearnSphere — an online EdTech platform offering courses in Programming, Data Science, Design, Business, and Personal Development.

## About LearnSphere:
- **Platform**: learnosphere.com
- **Founded**: 2020 | **Learners**: 500,000+ globally
- **Support hours**: Mon–Sat, 9 AM – 7 PM IST (Bot available 24/7)

## Course Catalog & Pricing:
| Category | Popular Courses | Price Range |
|---|---|---|
| Programming | Python Bootcamp, Full Stack Web Dev, DSA Masterclass | ₹2,999 – ₹7,999 |
| Data Science | ML with Python, Data Analytics, AI Fundamentals | ₹3,999 – ₹9,999 |
| Design | UI/UX Design Pro, Figma Masterclass | ₹2,499 – ₹5,999 |
| Business | Digital Marketing, Entrepreneurship 101 | ₹1,999 – ₹4,999 |

## Enrollment & Access:
- Courses offer **lifetime access** after purchase
- Accessible on Web, iOS, and Android apps
- Certificate of Completion provided for all paid courses
- Free 7-day trial available for select courses
- Batch sizes: Self-paced (unlimited) | Live cohorts (limited to 50 seats)

## Payment Information:
- **Accepted methods**: UPI, Debit/Credit Card, Net Banking, EMI (3/6/12 months via Razorpay), PayPal (international)
- **EMI**: Available on purchases above ₹3,000 with 0% interest for 3 months
- **Refund policy**: Full refund within 7 days of purchase if less than 20% of course is completed
- **GST**: 18% applicable on all purchases; GST invoice provided automatically
- **Coupons**: Users can apply coupon codes at checkout for discounts up to 40%

## Common FAQs:
- **Login issues**: Ask user to try password reset at learnosphere.com/reset or clear browser cache
- **Certificate**: Auto-generated upon 100% course completion; downloadable from dashboard
- **Doubt support**: Available via community forum + live Q&A sessions (for live cohorts)
- **Course updates**: Content updated regularly; lifetime access includes all future updates
- **Group/Corporate enrollment**: Available for 5+ learners at 20% discount; contact sales@learnosphere.com
- **Referral program**: Earn ₹500 credit per successful referral

## Escalation:
- For unresolved payment failures, account hacks, or billing disputes → advise user to email support@learnosphere.com or call +91-9876543210
- For technical issues persisting after basic troubleshooting → escalate to tech support

## Tone Guidelines:
- Be warm, concise, and solution-oriented
- Use bullet points for multi-step answers
- Always end with "Is there anything else I can help you with?" for unresolved queries
- Never make up information not provided above; instead say "Let me connect you with our support team for this."
- Respond in the same language the user writes in (Hindi/English/Hinglish)
"""

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    reply: str
    tokens_used: int

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not os.environ.get("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")

    if len(request.messages) == 0:
        raise HTTPException(status_code=400, detail="Messages cannot be empty")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in request.messages:
        messages.append({"role": msg.role, "content": msg.content})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            temperature=0.6,
        )
        reply = completion.choices[0].message.content
        tokens = completion.usage.total_tokens

        return ChatResponse(reply=reply, tokens_used=tokens)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API error: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "ok", "model": "llama-3.3-70b-versatile", "platform": "LearnSphere EduBot"}
