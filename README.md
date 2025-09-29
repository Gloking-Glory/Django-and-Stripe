# Django Stripe Payments

This is a Django backend project demonstrating a robust integration with Stripe for processing payments. It is designed to be associated with an `Appointment` model, but uses Django's ContentType framework to allow the `Payment` model to be generically linked to any model in the project.

The application provides two primary payment flows through a RESTful API:
1.  **Payment Intents**: For use with custom payment forms integrated into a frontend application (e.g., using Stripe Elements).
2.  **Checkout Sessions**: For redirecting users to a secure, Stripe-hosted payment page.

## Features

- **Generic Payment Model**: The `Payment` model can be linked to any other model (e.g., `Appointment`, `Order`, etc.) using a `GenericForeignKey`.
- **Stripe Integration**:
    - Create `PaymentIntents` to build custom payment flows.
    - Create `Checkout Sessions` for a quick and secure payment experience.
- **RESTful API**: Endpoints built with Django REST Framework for easy integration with frontend applications.
- **Idempotency**: Built-in idempotency key generation in the `Payment` model to prevent duplicate operations.
- **Error Handling**: Graceful handling of Stripe API errors.
- **Environment-based Configuration**: Securely manage keys and settings using environment variables.

## Technologies Used

- Python 3
- Django
- Django REST Framework
- Stripe Python SDK (`stripe`)
- `python-dotenv` for environment variable management

## Setup and Installation

Follow these steps to get the project running locally.

### 1. Prerequisites

- Python 3.8+
- `pip` and `venv`

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd djangoAssessment
```

### 3. Set Up a Virtual Environment

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Create a `requirements.txt` file with the following content:

```txt
Django
djangorestframework
stripe
python-dotenv
```

Then, install the packages:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the project's root directory (`djangoAssessment/`) and add your Stripe API keys and frontend URLs.

```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
FRONTEND_SUCCESS_URL=http://localhost:3000/success
FRONTEND_CANCEL_URL=http://localhost:3000/cancel
```

### 6. Run Database Migrations

Apply the database migrations to create the necessary tables.

```bash
python manage.py migrate
```

### 7. Run the Development Server

Start the Django development server.

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

The following endpoints are available under the `/api/` path prefix.

### Appointments

Endpoints for managing appointments.

-   **URL**: `/api/appointments/`
-   **Methods**:
    -   `GET`: List all appointments.
    -   `POST`: Create a new appointment.
-   **`POST` Body**:
    ```json
    {
        "provider_name": "Dr. Smith",
        "appointment_time": "2024-10-28T10:00:00Z",
        "client_email": "patient@example.com",
        "amount": 5000
    }
    ```
    *Note: `amount` should be in the smallest currency unit (e.g., cents).*

-   **URL**: `/api/appointments/<id>/`
-   **Methods**:
    -   `GET`: Retrieve a specific appointment.

### Payments

### Create Payment Intent

- **URL**: `/api/payments/create-payment-intent/`
- **Method**: `POST`
- **Body**:
  ```json
  {
      "appointment_id": "<uuid-of-the-appointment>"
  }
  ```
- **Success Response (201 CREATED)**:
  ```json
  {
      "payment_id": "<uuid-of-the-payment-object>",
      "client_secret": "<stripe-client-secret>"
  }
  ```

### Create Checkout Session

- **URL**: `/api/payments/create-checkout-session/`
- **Method**: `POST`
- **Body**:
  ```json
  {
      "appointment_id": "<uuid-of-the-appointment>"
  }
  ```
- **Success Response (201 CREATED)**:
  ```json
  {
      "checkout_url": "https://checkout.stripe.com/c/pay/..."
  }
  ```