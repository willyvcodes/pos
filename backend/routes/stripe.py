import os
import stripe

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from typing import List

from pydantic import BaseModel


class CheckoutItem(BaseModel):
    name: str
    quantity: int
    price: int
    thumbnail: str


router = APIRouter(prefix="/api/stripe", tags=["Stripe"])


@router.post("/create-checkout-session", status_code=201)
def create_checkout_session(check_items: List[CheckoutItem]):
    print("Received checkout request with items:", check_items)
    stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
    if not stripe.api_key:
        print("ERROR: STRIPE_SECRET_KEY not found in environment variables")
        return {"detail": "Stripe configuration error"}

    # Get domain URL from environment variable or use default
    domain_url = os.getenv("DOMAIN_URL")
    print("Using domain URL:", domain_url)

    new_line_items = [
        {
            "price_data": {
                "currency": "usd",
                "unit_amount": product.price,  # Price should already be in cents from frontend
                "product_data": {
                    "name": product.name,
                    "images": [product.thumbnail],
                },
            },
            "quantity": product.quantity,
        }
        for product in check_items
    ]
    print("Created line items:", new_line_items)

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=new_line_items,
            mode="payment",
            success_url=f"{domain_url}/api/stripe/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{domain_url}/api/stripe/cancel?session_id={{CHECKOUT_SESSION_ID}}",
        )
        print("Created Stripe session:", session.url)
        return {"url": session.url}
    except Exception as e:
        print("Stripe error:", str(e))
        return {"detail": str(e)}


@router.get("/success")
async def stripe_success(session_id: str):
    try:
        # Verify the session exists and is valid
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status != "paid":
            return HTMLResponse(content="Invalid session", status_code=400)

        html_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Payment Success</title>
                <meta http-equiv="refresh" content="3; URL=http://localhost:8000" />
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #f0f2f5;
                    }
                    .container {
                        text-align: center;
                        padding: 2rem;
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }
                    .success-icon {
                        color: #4CAF50;
                        font-size: 48px;
                        margin-bottom: 1rem;
                    }
                    h1 {
                        color: #4CAF50;
                        margin-bottom: 1rem;
                    }
                    p {
                        color: #666;
                        margin-bottom: 1rem;
                    }
                    .redirect-text {
                        color: #999;
                        font-size: 0.9rem;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success-icon">✓</div>
                    <h1>Payment Successful!</h1>
                    <p>Thank you for your purchase. Your order has been processed successfully.</p>
                    <p class="redirect-text">Redirecting you back to the store in 3 seconds...</p>
                </div>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)
    except stripe.error.StripeError:
        return HTMLResponse(content="Invalid session", status_code=400)


@router.get("/cancel", response_class=HTMLResponse)
async def stripe_cancel(session_id: str):
    try:
        # Verify the session exists
        session = stripe.checkout.Session.retrieve(session_id)

        html_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Payment Canceled</title>
                <meta http-equiv="refresh" content="3; URL=http://localhost:8000" />
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #f0f2f5;
                    }
                    .container {
                        text-align: center;
                        padding: 2rem;
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }
                    .cancel-icon {
                        color: #f44336;
                        font-size: 48px;
                        margin-bottom: 1rem;
                    }
                    h1 {
                        color: #f44336;
                        margin-bottom: 1rem;
                    }
                    p {
                        color: #666;
                        margin-bottom: 1rem;
                    }
                    .redirect-text {
                        color: #999;
                        font-size: 0.9rem;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="cancel-icon">✕</div>
                    <h1>Payment Canceled</h1>
                    <p>Your payment was canceled. No charges were made.</p>
                    <p class="redirect-text">Redirecting you back to the store in 3 seconds...</p>
                </div>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)
    except stripe.error.StripeError:
        return HTMLResponse(content="Invalid session", status_code=400)
