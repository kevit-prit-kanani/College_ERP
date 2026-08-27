# College ERP System

A comprehensive Enterprise Resource Planning (ERP) system designed for college management. This system handles student information, staff management, department administration, intake tracking, and analytics for educational institutions.

## Overview

The College ERP System is a modern web application built with **FastAPI** and **MongoDB** that provides a centralized platform for managing college operations including student records, staff information, department management, and analytics reporting.

## Features

- **Authentication & Authorization**: Secure login system with role-based access control (Admin, Staff, Student)
- **Student Management**: Create, retrieve, update, and delete student records with enrollment tracking
- **Staff Management**: Manage staff information with role-based permissions
- **Department Administration**: Organize and manage college departments and branches
- **Intake Management**: Track and manage student intakes across years and branches
- **Analytics**: Generate analytics reports including student counts by year and branch
- **RESTful API**: Complete REST API with comprehensive documentation via Swagger/OpenAPI
- **MongoDB Integration**: NoSQL database for flexible data management
- **Security**: Password hashing with pwdlib and JWT token-based authentication

## Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: MongoDB with Motor (async driver)
- **Authentication**: JWT with role-based access control
- **Password Hashing**: pwdlib
- **Server**: Uvicorn
- **Configuration**: Pydantic Settings with environment variables

## Project Structure

```
College_ERP/
├── main.py                          # Application entry point
├── pyproject.toml                   # Project dependencies and metadata
├── .env                             # Environment variables (not included in repo)
├── apps/
│   └── src/
│       ├── main.py                  # API router configuration
│       ├── api/                      # API endpoint modules
│       │   ├── Student.py           # Student management endpoints
│       │   ├── Staff.py             # Staff management endpoints
│       │   ├── Department.py        # Department management endpoints
│       │   ├── Intakes.py           # Intake management endpoints
│       │   └── Analytics.py         # Analytics endpoints
│       └── auth/
│           └── LoginAndRegister.py  # Authentication endpoints
├── libs/
│   ├── services/
│   │   └── openapi_customization.py # OpenAPI/Swagger customization
│   └── utils/
│       ├── logging_config.py        # Logging configuration
│       ├── config/                  # Configuration management
│       │   └── __init__.py          # Environment & config variables
│       ├── db/
│       │   └── mongodb/
│       │       ├── base_repository.py # Base database operations
│       │       ├── lifespan.py       # Application lifespan management
│       │       └── schemas/         # Database schemas
│       └── comman/                  # Common utilities
│           ├── auth/                # Authentication utilities
│           │   └── token_generation.py
│           ├── customs/             # Custom utilities
│           │   ├── HashPass.py      # Password hashing functions
│           │   └── variables.py     # Common variables
│           ├── exceptions/          # Custom exceptions
│           │   └── responses.py     # Exception responses
│           └── models/              # Pydantic data models
│               ├── User.py
│               ├── Student.py
│               ├── Staff.py
│               ├── Department.py
│               ├── Intakes.py
│               ├── Auth.py
│               └── APIResponse.py
├── logs/                            # Application logs
└── uploads/                         # File uploads directory
```

## Installation

### Prerequisites

- Python 3.12 or higher
- MongoDB (local or Atlas)
- pip or uv for package management

### Setup Steps

1. **Clone the repository**
   ```bash
   cd /path/to/College_ERP
   ```

2. **Create and configure environment file**
   ```bash
   cp .env.example .env
   ```

3. **Configure environment variables** in `.env`:
   ```
   AUTH_USERNAME=your_auth_user
   AUTH_PASSWORD=your_auth_password
   HOST=localhost
   FASTAPI_PORT=8000
   MONGODB_URL=mongodb://localhost:27017
   FASTAPI_DATABASE_NAME=ERP
   FILE_PATH=./uploads
   USERS_COLLECTION=users
   SECRET_KEY=your_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. **Install dependencies**
   ```bash
   pip install -e .
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

The application will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /auth/login` - User login (returns JWT token)
- `POST /auth/register/staff` - Staff registration

### Student Management
- `GET /student` - Get all students (Admin/Staff only)
- `POST /student` - Create a new student
- `GET /student/{id}` - Get student details
- `PUT /student/{id}` - Update student information
- `DELETE /student/{id}` - Delete student record

### Staff Management
- `GET /staff` - Get all staff (Admin only)
- `POST /staff` - Create new staff member
- `GET /staff/{id}` - Get staff details
- `PUT /staff/{id}` - Update staff information
- `DELETE /staff/{id}` - Delete staff record

### Department Management
- `GET /department` - List all departments
- `POST /department` - Create new department
- `GET /department/{id}` - Get department details
- `PUT /department/{id}` - Update department
- `DELETE /department/{id}` - Delete department

### Intake Management
- `GET /intakes` - List all intakes
- `POST /intakes` - Create new intake
- `GET /intakes/{id}` - Get intake details
- `PUT /intakes/{id}` - Update intake
- `DELETE /intakes/{id}` - Delete intake

### Analytics
- `GET /analytics/student-count` - Get student count by year and branch (Admin only)

### Health Check
- `GET /ping` - MongoDB health check endpoint
- `GET /` - Redirects to API documentation

## Authentication & Authorization

The system uses JWT (JSON Web Tokens) for authentication with three roles:

- **Admin**: Full access to all features
- **Staff**: Limited access to student and staff data
- **Student**: Access to personal information and shared resources

Authentication flow:
1. User provides credentials via `POST /auth/login`
2. System validates credentials against MongoDB
3. JWT token is returned with user ID and role embedded
4. Token is included in subsequent requests via `Authorization: Bearer <token>` header

## Database

The system uses MongoDB with the following collections:

- **Users**: Base user information
- **Students**: Student-specific information (extends User)
- **Staff**: Staff-specific information (extends User)
- **Departments**: College departments and branches
- **Intakes**: Student intake cycles
- **Analytics**: Aggregated data for reporting

## Configuration

Configuration is managed through environment variables defined in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `AUTH_USERNAME` | Authentication username | - |
| `AUTH_PASSWORD` | Authentication password | - |
| `HOST` | Server host | localhost |
| `FASTAPI_PORT` | Server port | 8000 |
| `MONGODB_URL` | MongoDB connection string | localhost |
| `FASTAPI_DATABASE_NAME` | Database name | ERP |
| `FILE_PATH` | Upload directory path | ./uploads |
| `SECRET_KEY` | JWT secret key | This_is_the_secrate_key_ |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Logging

The application includes comprehensive logging configured in `libs/utils/logging_config.py`. Logs are stored in the `logs/` directory for debugging and monitoring.

## File Uploads

Uploaded files are stored in the `uploads/` directory. Ensure this directory has appropriate permissions and sufficient storage space.

## Development

### Running Tests
```bash
pytest
```

### Code Style
The project follows PEP 8 standards. Use the following for linting:
```bash
pylint apps/ libs/
```

## Security Considerations

1. **Environment Variables**: Never commit `.env` file to version control
2. **MongoDB**: Use connection strings with authentication in production
3. **JWT Secret**: Use a strong, randomly generated secret key
4. **HTTPS**: Enable HTTPS in production environments
5. **Password Policy**: Implement strong password requirements

## Performance Optimization

- **Async/Await**: All database operations use async patterns via Motor
- **Connection Pooling**: MongoDB connection pooling is configured for optimal performance
- **Indexing**: Ensure appropriate indexes on frequently queried fields
- **Caching**: Consider implementing caching for frequently accessed data

## Future Enhancements

- [ ] Role-based data access control (RBAC) refinement
- [ ] Advanced reporting and dashboards
- [ ] Integration with external authentication systems (LDAP, OAuth)
- [ ] Bulk import/export functionality
- [ ] Email notifications
- [ ] SMS alerts
- [ ] Mobile application

## Authors

- **Prit Kanani** - kevit-prit-kanani (prit.kanani@kevit.io)

## License

This project is part of a college assessment. Contact the author for licensing information.

## Support

For issues, questions, or contributions, please contact the development team or submit an issue through the project repository.
