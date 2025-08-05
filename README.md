# Advanced Password Checker

A Django web application that implements scientifically-backed password strength validation using entropy calculations, pattern detection, and dictionary checking.

## Features

### 🔐 Advanced Password Validation
- **Entropy Calculation**: Uses mathematical entropy to measure true password strength
- **Pattern Detection**: Identifies repeated characters, sequential patterns, and keyboard patterns
- **Dictionary Checking**: Compares against common password databases (RockYou dataset)
- **Smart Feedback**: Provides specific, actionable suggestions for password improvement

### 🎯 User Authentication
- User registration with advanced password validation
- Secure login/logout functionality
- Session management
- User-friendly error messages

### 💻 Interactive Features
- Real-time password strength checking
- Visual strength meter
- Dynamic feedback system
- Responsive design

## Technical Implementation

### Password Strength Algorithm

The password strength is calculated using:

1. **Base Entropy**: `length × log2(character_pool_size)`
2. **Pattern Penalties**: Deductions for:
   - Repeated characters (3+ in sequence): -10 points
   - Sequential patterns (abc, 123): -5 points
   - Keyboard patterns (qwerty, asdf): -10 points
   - Common passwords: Major penalty
3. **Effective Entropy**: `max(base_entropy - penalties, 0)`

### Strength Categories
- **Very Weak**: < 28 bits
- **Weak**: 28-35 bits
- **Moderate**: 36-59 bits
- **Strong**: 60-127 bits
- **Very Strong**: 128+ bits

## Installation & Setup

### Prerequisites
- Python 3.8+
- Django 5.1+

### Quick Start

1. **Clone and Navigate**
   ```bash
   cd /path/to/advanced-password
   ```

2. **Install Dependencies**
   ```bash
   pip install django
   ```

3. **Setup Database**
   ```bash
   python3 manage.py migrate
   ```

4. **Create Sample Users**
   ```bash
   python3 manage.py create_sample_users
   ```

5. **Run Development Server**
   ```bash
   python3 manage.py runserver
   ```

6. **Access Application**
   - Home: http://127.0.0.1:8000/
   - Register: http://127.0.0.1:8000/register/
   - Login: http://127.0.0.1:8000/login/
   - Admin: http://127.0.0.1:8000/admin/

## Project Structure

```
advanced-password/
├── manage.py                     # Django management script
├── db.sqlite3                   # SQLite database
├── setup.sh                     # Automated setup script
├── README.md                    # This file
├── PROJECT_SUMMARY.md           # Project completion summary
├── advanced_password/           # Main project settings
│   ├── settings.py             # Django settings
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI configuration
├── accounts/                    # User authentication app
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── forms.py                # Form definitions
│   ├── validators.py           # Custom password validator
│   ├── advanced_password_checker.py  # Core algorithm
│   ├── rockyou.txt            # Common passwords database
│   └── management/             # Django management commands
│       └── commands/
│           └── create_sample_users.py
├── templates/                   # HTML templates
│   ├── home.html               # Homepage with demo
│   ├── register.html           # Registration form
│   └── login.html              # Login form
└── static/                      # Static assets
    ├── css/
    └── js/
```

## API Endpoints

### Password Checking API
- **URL**: `/api/check-password/`
- **Method**: POST
- **Content-Type**: application/json
- **Body**: `{"password": "your_password"}`
- **Response**:
  ```json
  {
    "password": "example123",
    "length": 10,
    "base_entropy": 59.54,
    "penalty": 10,
    "effective_entropy": 49.54,
    "strength": "Moderate",
    "feedback": [
      "Consider using a longer password for increased security.",
      "Adding uppercase letters can improve strength."
    ]
  }
  ```

## Security Features

### Password Validation Rules
- Minimum 8 characters (configurable)
- Minimum 60 bits effective entropy (configurable)
- Protection against common passwords
- Pattern detection and penalties
- User attribute similarity checking

### Django Security
- CSRF protection enabled
- Secure session management
- Password hashing with PBKDF2
- SQL injection protection via ORM

## Configuration

### Customizing Password Requirements

Edit `advanced_password/settings.py`:

```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'accounts.validators.AdvancedPasswordValidator',
        'OPTIONS': {
            'min_entropy': 60,  # Adjust minimum entropy requirement
        },
    },
    # ... other validators
]
```

### Adding More Common Passwords

Replace or extend `accounts/rockyou.txt` with additional password lists.

## Testing

### Manual Testing
1. Register a new account with various password strengths
2. Test the real-time password checker on the homepage
3. Verify login/logout functionality
4. Check admin interface access

### Test Cases
- Weak passwords (e.g., "123456", "password")
- Strong passwords (e.g., "Tr0ub4dor&3")
- Passwords with patterns (e.g., "abcdef", "qwerty")
- Very long passwords
- Special character combinations

## Common Issues & Solutions

### Issue: ModuleNotFoundError
```bash
pip install django
```

### Issue: Database not found
```bash
python3 manage.py migrate
```

### Issue: Static files not loading
Check `STATIC_URL` and `STATICFILES_DIRS` in settings.py

### Issue: RockYou file not found
Ensure `accounts/rockyou.txt` exists with common passwords (one per line)

## Performance Considerations

- Password checking is optimized for real-time feedback
- Common password lookup uses set data structure (O(1) lookup)
- Database queries are minimized
- Static files are efficiently served

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Credits

- Password entropy calculation based on NIST guidelines
- RockYou password list for common password detection
- Django framework for web application structure
- Modern CSS for responsive design

---

**Note**: This is a demonstration project. For production use, consider additional security measures such as rate limiting, HTTPS enforcement, and comprehensive logging.
