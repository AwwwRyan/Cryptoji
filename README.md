# Cryptoji - Emoji Crypto API

A Django REST Framework API that transforms plain text into encrypted emoji sequences and back again using RSA and AES encryption.

## Overview

Cryptoji is a unique encryption service that converts regular text messages into emoji-based ciphertexts. Built with Django REST Framework, it uses a hybrid encryption approach combining RSA for key exchange and AES for efficient message encryption. The encrypted data is then encoded as a sequence of emojis, making cryptographic messages more visually appealing and fun to share.

**Key Features:**
- Hybrid RSA + AES encryption for security and performance
- Emoji-based ciphertext encoding
- RESTful API endpoints for easy integration
- JSON request/response format
- Stateless encryption/decryption operations

## Tech Stack

- **Python 3.x** - Core programming language
- **Django** - Web framework
- **Django REST Framework** - API framework for building REST endpoints
- **Cryptography** - Python library for RSA and AES encryption

## Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/cryptoji.git
cd cryptoji
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Start Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Endpoints

### Encrypt Text to Emojis

**Endpoint:** `POST /api/encrypt/`

**Request Body:**
```json
{
  "message": "hello"
}
```

**Response:**
```json
{
  "encrypted": "😄🎉🌟💫🚀🎈🌈✨🎊🔥🌺🦋🎭🎪🎨"
}
```

**Postman Example:**
- Method: `POST`
- URL: `http://localhost:8000/api/encrypt/`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
  ```json
  {
    "message": "Hello, World!"
  }
  ```

### Decrypt Emojis to Text

**Endpoint:** `POST /api/decrypt/`

**Request Body:**
```json
{
  "emoji_text": "😄🎉🌟💫🚀🎈🌈✨🎊🔥🌺🦋🎭🎪🎨"
}
```

**Response:**
```json
{
  "message": "hello"
}
```

**Postman Example:**
- Method: `POST`
- URL: `http://localhost:8000/api/decrypt/`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
  ```json
  {
    "emoji_text": "😄🎉🌟💫🚀🎈🌈✨🎊🔥🌺🦋🎭🎪🎨"
  }
  ```

## Frontend Usage

Frontend applications can easily integrate with the Cryptoji API using standard HTTP clients:

### Using Fetch API
```javascript
// Encrypt a message
const encryptMessage = async (message) => {
  const response = await fetch('http://localhost:8000/api/encrypt/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  });
  const data = await response.json();
  return data.encrypted;
};

// Decrypt emoji text
const decryptMessage = async (emojiText) => {
  const response = await fetch('http://localhost:8000/api/decrypt/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ emoji_text: emojiText }),
  });
  const data = await response.json();
  return data.message;
};
```

### Using Axios
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Encrypt a message
const encryptMessage = async (message) => {
  const response = await api.post('/encrypt/', { message });
  return response.data.encrypted;
};

// Decrypt emoji text
const decryptMessage = async (emojiText) => {
  const response = await api.post('/decrypt/', { emoji_text: emojiText });
  return response.data.message;
};
```

**Important:** Always ensure you're sending the `Content-Type: application/json` header with your requests.

## Running Notes

### Key Generation and Persistence

- **Development Mode**: Encryption keys are generated at runtime when the server starts. This means that emoji ciphertexts encrypted in one session will only be valid until the server restarts.

- **Production Considerations**: For production deployments, you should implement key persistence to maintain decryption capabilities across server restarts. Consider:
  - Storing keys in environment variables
  - Using a secure key management service
  - Implementing a database-backed key store
  - Setting up proper key rotation policies

### Security Considerations

- The current implementation is designed for demonstration purposes
- In production, implement proper key management and storage
- Consider adding authentication and rate limiting
- Ensure HTTPS is used for all API communications
- Implement proper error handling without exposing sensitive information

### Development Tips

- Use the Django admin interface to monitor API usage if needed
- Enable Django's debug toolbar for development insights
- Consider adding logging for encryption/decryption operations
- Test with various message lengths and character sets

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
