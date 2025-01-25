# Finance Tracker API

A Django REST API for tracking personal finances, expenses, and budgets.

## Features
- User authentication with JWT
- Expense tracking and categorization
- Budget management
- Financial goals
- Export to CSV and PDF
- Currency conversion
- Spending analysis

## Setup
1. Clone the repository

2. Create virtual environment and install dependencies

3. Set up environment variables
Create a `.env` file in the root directory and add:

4. Run migrations

## API Documentation

The API documentation is available at `/api/docs/` when the server is running.

### Main Endpoints
- `/api/auth/` - Authentication endpoints
- `/api/expenses/` - Expense management
- `/api/budgets/` - Budget tracking
- `/api/goals/` - Financial goals
- `/api/reports/` - Financial reports and analysis

## Testing
Run the test suite:
```bash
python manage.py test
```

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please open an issue in the GitHub repository or contact the maintainers.