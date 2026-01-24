# Contributing to AI Chatbot Backend

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Docker and Docker Compose
- Git
- A code editor (VS Code, PyCharm, etc.)

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/backend-ai-chatbot-project-bnglr.git
   cd backend-ai-chatbot-project-bnglr
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

5. **Start Database with Docker**
   ```bash
   docker-compose up db
   ```

6. **Initialize Database**
   ```bash
   python init_db.py
   ```

7. **Run Application**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

## Code Style Guidelines

### Python Code
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Maximum line length: 100 characters
- Use docstrings for all functions, classes, and modules

### Docstring Format
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

### Import Organization
```python
# Standard library imports
import os
from typing import List

# Third-party imports
from fastapi import FastAPI
from sqlalchemy import Column

# Local imports
from app.config import settings
from app.models import Session
```

## Project Structure

```
app/
├── api/              # API endpoints
├── config/           # Configuration files
├── models/           # Database and Pydantic models
├── services/         # Business logic
└── utils/            # Utility functions
```

## Making Changes

### Branch Naming
- Feature: `feature/your-feature-name`
- Bug fix: `fix/bug-description`
- Documentation: `docs/what-you-updated`

### Commit Messages
Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

Example:
```
feat: add support for DOCX file uploads
fix: resolve vector similarity search issue
docs: update README with new features
```

## Adding New Features

### New API Endpoint
1. Create route in appropriate file in `app/api/`
2. Add Pydantic schemas in `app/models/schemas.py`
3. Implement business logic in `app/services/`
4. Update API documentation
5. Add tests

### New LLM Provider
1. Add provider in `app/services/llm_service.py`
2. Update `.env.example` with required keys
3. Update README.md with setup instructions
4. Test thoroughly

### New Document Type
1. Add parser in `app/services/document_service.py`
2. Update allowed types in upload endpoint
3. Test with sample documents

## Testing

### Manual Testing
```bash
# Start the server
python -m uvicorn app.main:app --reload

# In another terminal
python test_api.py
```

### Testing Checklist
- [ ] All endpoints return expected responses
- [ ] Error handling works correctly
- [ ] Database operations commit properly
- [ ] Vector search returns relevant results
- [ ] Session management isolates data correctly

## Pull Request Process

1. **Before Submitting**
   - Ensure code follows style guidelines
   - Add/update docstrings
   - Test your changes thoroughly
   - Update documentation if needed

2. **Pull Request Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Refactoring
   
   ## Testing
   - [ ] Tested locally
   - [ ] All endpoints work
   - [ ] No breaking changes
   
   ## Screenshots (if applicable)
   ```

3. **Review Process**
   - Address review comments
   - Keep PR scope focused
   - Rebase if needed

## Common Tasks

### Adding a New Database Model
```python
# In app/models/models.py
class NewModel(Base):
    __tablename__ = "new_table"
    
    id = Column(Integer, primary_key=True)
    # Add fields...
```

Then run:
```bash
python init_db.py
```

### Updating Dependencies
```bash
pip install new-package
pip freeze > requirements.txt
# Update docker-compose.yml if needed
```

## Troubleshooting

### Database Issues
```bash
# Reset database
docker-compose down -v
docker-compose up db
python init_db.py
```

### Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Getting Help

- GitHub Issues: For bugs and feature requests
- Discussions: For questions and general discussion

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards other contributors

Thank you for contributing! 🎉
