# Unified Travel Reservation System (UTRS)

## Overview
The Unified Travel Reservation System (UTRS) is a Django-based web application that provides a comprehensive platform for booking various travel and entertainment services. Users can register, log in, and book services such as train tickets, bus tickets, movie tickets, hotel rooms, and more. The system includes separate interfaces for guests and administrators, with OTP-based authentication for security.

## Features
- **User Registration and Login**: OTP-based verification for secure account creation and login.
- **Service Booking**: Support for multiple service types including trains, buses, movies, hotels, and restaurants.
- **Admin Panel**: Administrators can manage users, services, and view dashboards.
- **Seat Selection**: Interactive seat selection for movies and buses.
- **Payment Integration**: Simulated payment processing with confirmation emails.
- **Responsive Design**: User-friendly templates for a seamless experience.

## Technologies Used
- **Backend**: Django (Python)
- **Database**: SQLite (default Django database)
- **Frontend**: HTML, CSS (via Django templates)
- **Email**: Django's email backend for OTP and confirmations
- **Authentication**: Django's built-in auth system with OTP verification

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Django 4.x
- Git

### Steps
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd unifiedtrsdemo
   ```

2. **Create a Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```
   (Note: If requirements.txt is not present, install Django: `pip install django`)

4. **Apply Migrations**:
   ```
   python manage.py migrate
   ```

5. **Create Superuser (for Admin Access)**:
   ```
   python manage.py createsuperuser
   ```

6. **Run the Server**:
   ```
   python manage.py runserver
   ```

7. **Access the Application**:
   - Guest Interface: http://127.0.0.1:8000/
   - Admin Login: http://127.0.0.1:8000/adminapp/admin_login/

## Project Structure
```
unifiedtrsdemo/
├── adminapp/          # Admin application
│   ├── models.py      # Service, HotelRoom, etc.
│   ├── views.py       # Admin views
│   └── ...
├── guestapp/          # Guest application
│   ├── models.py      # Booking models, OTPVerification
│   ├── views.py       # Guest views
│   └── ...
├── templates/         # HTML templates
├── media/             # Uploaded files
├── db.sqlite3         # Database
└── manage.py          # Django management script
```

## Functions in the Project

### Admin App (adminapp/views.py)
- `admin_login(request)`: Handles admin login with authentication and staff check. Parameters: request (HttpRequest). Returns: HttpResponse.
- `admin_dashboard(request)`: Displays admin dashboard with user statistics. Parameters: request (HttpRequest). Returns: HttpResponse.
- `admin_logout(request)`: Logs out the admin user. Parameters: request (HttpRequest). Returns: HttpResponse.
- `admin_users(request)`: Lists all non-staff users with search functionality. Parameters: request (HttpRequest). Returns: HttpResponse.
- `delete_user(request, user_id)`: Deletes a user account (admin only). Parameters: request (HttpRequest), user_id (int). Returns: HttpResponse.
- `admin_services(request)`: Lists all services with optional filtering by type. Parameters: request (HttpRequest). Returns: HttpResponse.
- `add_service(request)`: Adds a new service with validation. Parameters: request (HttpRequest). Returns: HttpResponse.
- `delete_service(request, service_id)`: Deletes a service. Parameters: request (HttpRequest), service_id (int). Returns: HttpResponse.
- `toggle_service(request, service_id)`: Toggles the active status of a service. Parameters: request (HttpRequest), service_id (int). Returns: HttpResponse.

### Guest App (guestapp/views.py)
- `index(request)`: Renders the home page. Parameters: request (HttpRequest). Returns: HttpResponse.
- `register(request)`: Handles user registration with OTP generation and email sending. Parameters: request (HttpRequest). Returns: HttpResponse.
- `verify_otp(request)`: Verifies OTP for registration. Parameters: request (HttpRequest). Returns: HttpResponse.
- `register_success(request)`: Displays registration success page. Parameters: request (HttpRequest). Returns: HttpResponse.
- `login_user(request)`: Handles user login with OTP generation. Parameters: request (HttpRequest). Returns: HttpResponse.
- `verify_login_otp(request)`: Verifies OTP for login. Parameters: request (HttpRequest). Returns: HttpResponse.
- `services_home(request)`: Displays the services home page. Parameters: request (HttpRequest). Returns: HttpResponse.
- `services_by_category(request, code)`: Lists services by category (e.g., train, bus). Parameters: request (HttpRequest), code (str). Returns: HttpResponse.
- `service_detail(request, service_id)`: Shows details of a specific service. Parameters: request (HttpRequest), service_id (int). Returns: HttpResponse.
- `book_service(request, service_id)`: Routes to appropriate booking page based on service type. Parameters: request (HttpRequest), service_id (int). Returns: HttpResponse.
- `select_show(request, service_id)`: Selects show date and time for movie booking. Parameters: request (HttpRequest), service_id (int). Returns: HttpResponse.
- `get_seat_price(seat)`: Calculates seat price based on row (utility function). Parameters: seat (str). Returns: int.
- `select_seats(request, service_id)`: Handles seat selection for movies. Parameters: request (HttpRequest), service_id (int). Returns: HttpResponse.
- `train_booking(request, service_id)`: Handles train ticket booking. Parameters: request (HttpRequest), service_id (int). Returns: HttpResponse.
- `hotel_booking(request, service_id)`: Handles hotel room booking. Parameters: request (HttpRequest), service_id (int). Returns: HttpResponse.
- `bus_booking(request, service_id)`: Handles bus ticket booking with seat selection. Parameters: request (HttpRequest), service_id (int). Returns: HttpResponse.
- `payment_page(request)`: Displays payment page with booking details. Parameters: request (HttpRequest). Returns: HttpResponse.
- `complete_booking(request)`: Processes payment and creates booking records, sends confirmation email. Parameters: request (HttpRequest). Returns: HttpResponse.

### Models
- **Service** (`adminapp/models.py`): Represents services like trains, buses, etc. Methods: `__str__(self)`: Returns the service name.
- **HotelRoom** (`adminapp/models.py`): Represents hotel rooms. Methods: `__str__(self)`: Returns formatted room description.
- **HotelBooking** (`adminapp/models.py`): Represents hotel bookings. Methods: `__str__(self)`: Returns formatted booking description.
- **Movie** (`adminapp/models.py`): Represents movies. Methods: `__str__(self)`: Returns the movie title.
- **SeatBooking** (`adminapp/models.py`): Represents movie seat bookings. Methods: `__str__(self)`: Returns formatted seat booking description.
- **OTPVerification** (`guestapp/models.py`): Handles OTP storage. Methods: `__str__(self)`: Returns the email.
- **TrainBooking** (`guestapp/models.py`): Represents train bookings. Methods: `__str__(self)`: Returns formatted train booking description.
- **HotelBooking** (`guestapp/models.py`): Represents hotel bookings. Methods: `__str__(self)`: Returns formatted hotel booking description.
- **SeatBooking** (`guestapp/models.py`): Represents seat bookings. Methods: `__str__(self)`: Returns formatted seat booking description.
- **BusBooking** (`guestapp/models.py`): Represents bus bookings. Methods: `__str__(self)`: Returns formatted bus booking description.

## Usage
1. **Register/Login**: Users register with email and OTP verification.
2. **Browse Services**: Navigate through categories like trains, buses, movies, hotels.
3. **Book Services**: Select services, choose options (seats, dates), and complete payment.
4. **Admin Management**: Admins can add/edit/delete services and manage users.

## Contributing
1. Fork the repository.
2. Create a feature branch.
3. Make changes and test.
4. Submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For questions or support, contact the development team.