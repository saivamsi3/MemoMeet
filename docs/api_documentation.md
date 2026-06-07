# API Documentation

## Chat API
- `POST /chat/ask` - Ask a question
  - Body: `{"question": "..."}`
  - Response: `{"answer": "..."}`

## Authentication
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout
