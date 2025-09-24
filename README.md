# MyFlat - Property Rental & Flatmate Finding Platform

A web application where local people can post about flats (1RK, 2BHK, 3BHK, 4BHK, etc.) and find flatmates. People can connect to purchase flats or find compatible flatmates.

## Features

- **Property Listings**: Post different types of flats (1RK, 2BHK, 3BHK, 4BHK, 5BHK, Studio)
- **Flatmate Finding**: Users can post to find compatible flatmates
- **Public Information**: Images, location, rent, and videos are publicly visible
- **Private Contact Details**: Only administrators can view contact information
- **User Authentication**: Secure registration and login system
- **Admin Panel**: Comprehensive admin interface for managing listings
- **Search & Filter**: Advanced search functionality with multiple filters
- **Responsive Design**: Mobile-friendly interface

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (can be easily changed to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **File Upload**: Support for images and videos

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aloksingh1818/MyFlat.git
cd MyFlat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## Default Admin Account

- **Username**: admin
- **Password**: admin123

## Usage

### For Regular Users:
1. Register for an account
2. Login to access posting features
3. Post flats or search for flatmates
4. Browse available listings
5. View public information (images, location, rent, videos)

### For Administrators:
1. Login with admin credentials
2. Access the Admin Panel
3. View all contact details of posters
4. Manage property listings
5. Monitor platform activity

## Project Structure

```
MyFlat/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── post_flat.html
│   ├── search.html
│   └── admin.html
└── static/           # Static files
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── uploads/      # User uploaded files
        ├── images/
        └── videos/
```

## Security Features

- Password hashing using Werkzeug
- File upload security with secure filenames
- SQL injection protection via SQLAlchemy ORM
- Admin-only access to sensitive contact information
- Session management with Flask-Login

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

For any questions or support, please contact the development team.