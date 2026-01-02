# 🏗️  system Architecture

## System Overview

Legal Summarizer is built using a modern microservices architecture with clear separation between frontend, backend, and database layers.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────┐
│          Frontend (React/Next.js)               │
│  - Document Upload UI                          │
│  - Summary Display                             │
│  - User Dashboard                              │
│  - Admin Panel                                 │
└──────────────┬──────────────────────────────────┘
               │ HTTPS
               ▼
┌─────────────────────────────────────────────────┐
│       API Gateway / Load Balancer               │
│  - Request routing                             │
│  - Rate limiting                               │
│  - CORS handling                               │
└──────────────┬──────────────────────────────────┘
               │
         ┌─────┴──────┐
         ▼            ▼
    ┌─────────┐   ┌─────────┐
    │FastAPI  │   │ Django  │
    │Backend  │   │Backend  │
    └────┬────┘   └────┬────┘
         │             │
         └──────┬──────┘
                ▼
    ┌─────────────────────┐
    │  PostgreSQL/MySQL   │
    │   (Primary DB)      │
    └─────────────────────┘
```

---

## Technology Stack

### Frontend
- **Framework**: React 18+ / Next.js 13+
- **State Management**: Redux / Context API
- **Styling**: Tailwind CSS
- **UI Components**: Material-UI / Custom
- **Build Tool**: Webpack / Vite
- **Testing**: Jest + React Testing Library

### Backend
- **Framework**: FastAPI / Django
- **Language**: Python 3.8+
- **API**: RESTful with OpenAPI docs
- **Authentication**: JWT + OAuth2
- **Task Queue**: Celery + Redis
- **Testing**: Pytest + Unittest

### Database
- **Primary**: PostgreSQL / MySQL
- **Cache**: Redis
- **Search**: Elasticsearch (optional)

### NLP & AI
- **Models**: Hugging Face Transformers
- **Summarization**: BART / T5
- **Entity Extraction**: spaCy
- **Language Detection**: TextBlob

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack

---

## Project Structure

```
Legal-Summarizer/
├── front/                      # React Frontend
│   ├── public/                # Static files
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   ├── hooks/            # Custom hooks
│   │   ├── styles/           # CSS/Tailwind
│   │   └── App.jsx           # Main component
│   ├── package.json
│   └── tailwind.config.js
│
├── fastapi_agents/             # FastAPI Backend
│   ├── main.py               # Entry point
│   ├── requirements.txt       # Dependencies
│   ├── api/
│   │   ├── routes/          # API endpoints
│   │   ├── schemas/         # Request/Response schemas
│   │   └── middleware/      # Custom middleware
│   ├── services/            # Business logic
│   │   ├── summarizer.py   # Summarization service
│   │   ├── auth.py         # Authentication
│   │   └── document.py     # Document handling
│   ├── models/             # Database models
│   ├── database/           # DB configuration
│   ├── utils/              # Utility functions
│   └── config.py           # Configuration
│
├── django_back/            # Django Backend (Alternative)
│   ├── manage.py
│   ├── requirements.txt
│   ├── apps/
│   │   ├── users/         # User management
│   │   ├── documents/     # Document handling
│   │   └── summaries/     # Summarization logic
│   └── config/
│
├── docker-compose.yml      # Container orchestration
├── nginx.conf             # Web server config
└── README.md
```

---

## API Architecture

### Authentication Flow
```
User Login
   ↓
JWT Token Generation
   ↓
Token Stored (LocalStorage/Cookie)
   ↓
Token Sent in Headers
   ↓
Token Validation
   ↓
Access Granted/Denied
```

### Document Processing Flow
```
Document Upload
   ↓
File Validation (Type, Size)
   ↓
Store in Database
   ↓
Extract Text (PDF/DOC/TXT)
   ↓
Preprocessing (Cleaning, Tokenization)
   ↓
NLP Model Processing
   ↓
Generate Summary
   ↓
Store Summary in DB
   ↓
Return to User
```

---

## Data Models

### User Model
```python
User {
  id: UUID
  email: String (unique)
  username: String
  password_hash: String
  created_at: DateTime
  updated_at: DateTime
  is_active: Boolean
  role: Enum(ADMIN, USER)
}
```

### Document Model
```python
Document {
  id: UUID
  user_id: UUID (FK)
  filename: String
  file_path: String
  file_type: String (pdf, docx, txt)
  file_size: Integer
  content: Text
  created_at: DateTime
  updated_at: DateTime
  status: Enum(PROCESSING, COMPLETED, FAILED)
}
```

### Summary Model
```python
Summary {
  id: UUID
  document_id: UUID (FK)
  user_id: UUID (FK)
  title: String
  content: Text
  key_points: JSON Array
  risks: JSON Array
  recommendations: JSON Array
  created_at: DateTime
  updated_at: DateTime
  is_shared: Boolean
}
```

---

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh token

### Documents
- `GET /api/documents` - List documents
- `POST /api/documents` - Upload document
- `GET /api/documents/{id}` - Get document details
- `DELETE /api/documents/{id}` - Delete document

### Summaries
- `GET /api/summaries` - List summaries
- `POST /api/summaries` - Create summary
- `GET /api/summaries/{id}` - Get summary
- `PUT /api/summaries/{id}` - Update summary
- `DELETE /api/summaries/{id}` - Delete summary

---

## Security Architecture

### Layers
1. **Network Layer**: HTTPS, Firewall, WAF
2. **Application Layer**: Input validation, Authentication
3. **Database Layer**: Encryption, Access control
4. **Data Layer**: Encryption at rest

### Encryption
- **In Transit**: TLS 1.3
- **At Rest**: AES-256
- **Passwords**: Bcrypt (salt rounds: 12)

---

## Deployment Architecture

### Development
```
Local Machine
├── Frontend (npm run dev)
├── Backend (python main.py)
└── Database (Docker container)
```

### Production
```
Docker Swarm / Kubernetes
├── Frontend Container
├── Backend Containers (replicated)
├── Database Container (persistent volume)
└── Redis Container (cache)
```

---

## Performance Considerations

### Caching Strategy
- Redis for session storage
- Client-side caching for static assets
- API response caching (5-10 minutes)

### Optimization
- Lazy loading for documents
- Pagination (50 items per page)
- Database indexing on frequently queried fields
- CDN for static files

### Scalability
- Horizontal scaling for backend
- Load balancing with Nginx
- Database read replicas
- Message queue for async processing

---

## Integration Points

### External Services
- **Authentication**: OAuth2 (Google, GitHub)
- **Email**: SendGrid / SMTP
- **Storage**: AWS S3 / Google Cloud Storage
- **NLP**: Hugging Face Models
- **Analytics**: Google Analytics / Mixpanel

---

## Error Handling

### Response Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Server Error

### Error Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

---

## Monitoring & Logging

### Metrics Tracked
- API response times
- Error rates
- Document processing duration
- User engagement
- System resource usage

### Logs Stored
- Request/Response logs
- Error logs
- Security events
- Performance metrics

---

<div align="center">

### Architecture Decisions

Built for **scalability**, **security**, and **maintainability**.

</div>