# POS System

A modern Point of Sale (POS) system built with FastAPI and Svelte, designed for local stores and small businesses.

## Features

- 🛍️ Product Management
- 💰 Order Processing
- 👥 User Management
- 📊 Order History
- 💳 Stripe Integration
- 🔐 JWT Authentication
- 📱 Responsive Design

## Tech Stack

### Backend
- FastAPI (Python)
- MongoDB (Database)
- JWT (Authentication)
- Stripe (Payment Processing)

### Frontend
- Svelte
- Bootstrap
- Font Awesome
- SweetAlert2

## Prerequisites

- Python
- Node.js
- MongoDB
- Stripe Account

## Installation

1. Clone the repository:
```bash
git clone https://github.com/willyvcodes/pos.git
cd POS-System
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the backend directory with the following variables:
```env
# MongoDB Configuration
MONGO_URI=your_mongo_uri

# JWT Configuration
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Stripe Configuration
STRIPE_SECRET_KEY=your_stripe_secret_key
DOMAIN_URL=http://localhost:8000
```

## Running the Application

### Manual Setup

1. Start MongoDB:
   - Make sure MongoDB is installed and running on your system
   - Update the MONGO_URI in your .env file to point to your MongoDB instance

2. Start the backend server:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Start the frontend development server:
```bash
cd frontend
npm run dev
```

4. Access the application:
   - Main application: http://localhost:8000
   - API documentation: http://localhost:8000/docs

### Docker Setup (Optional)

If you prefer using Docker:

1. Make sure your `.env` file is properly configured with your MongoDB connection string

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Author

William Valido
- Website: [willyv.dev](https://willyv.dev)
- GitHub: [@willyvcodes](https://github.com/willyvcodes)

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Svelte](https://svelte.dev/)
- [Bootstrap](https://getbootstrap.com/)
- [Stripe](https://stripe.com/)
