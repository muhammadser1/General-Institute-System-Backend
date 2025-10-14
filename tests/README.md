# Test Suite Documentation

## 📁 Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── requirements-test.txt    # Testing dependencies
├── user/                    # User module tests
│   ├── __init__.py
│   ├── test_user_model.py   # User model unit tests (70+ tests)
│   ├── test_deps.py         # Authentication & authorization tests (20+ tests)
│   └── test_user_routes.py  # User endpoint integration tests (30+ tests)
└── README.md               # This file
```

## 🚀 Setup

### Install All Dependencies (including tests)

```bash
pip install -r requirements.txt
```

All dependencies (production + testing) are now in one file!

## ▶️ Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/user/test_user_model.py
pytest tests/user/test_deps.py
pytest tests/user/test_user_routes.py
```

### Run Specific Test Class
```bash
pytest tests/user/test_user_model.py::TestUserBusinessLogic
```

### Run Specific Test Function
```bash
pytest tests/user/test_user_model.py::TestUserBusinessLogic::test_is_active_returns_true_for_active_user
```

### Run with Markers
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only user tests
pytest -m user
```

### Run with Coverage Report
```bash
pytest --cov=app --cov-report=html
```

Then open `htmlcov/index.html` in your browser to see detailed coverage.

### Run with Verbose Output
```bash
pytest -v
```

### Run and Stop on First Failure
```bash
pytest -x
```

### Run Last Failed Tests Only
```bash
pytest --lf
```

## 📊 Test Coverage

### User Module Test Coverage

#### **test_user_model.py** - 70+ Unit Tests
- ✅ User creation with required/optional fields
- ✅ User ID auto-generation
- ✅ Business logic methods (is_active, is_admin, is_teacher, get_full_name)
- ✅ Data conversion (to_dict, from_dict)
- ✅ Database operations (find, save, update, exists checks)
- ✅ Roundtrip conversions
- ✅ String representation

#### **test_deps.py** - 20+ Integration Tests
- ✅ Token validation
- ✅ User authentication
- ✅ User authorization (admin/teacher)
- ✅ Invalid token handling
- ✅ Expired token handling
- ✅ Inactive/suspended user handling
- ✅ Dependency chaining
- ✅ Security headers

#### **test_user_routes.py** - 30+ Integration Tests
- ✅ Login endpoint (success, failures, validation)
- ✅ Logout endpoint (authenticated, unauthenticated)
- ✅ Get profile endpoint (/me)
- ✅ Teacher signup endpoint (success, duplicates, validation)
- ✅ Full user flow integration (signup → login → profile)
- ✅ Password hashing
- ✅ Role enforcement

## 🎯 Test Categories

### Unit Tests (Fast)
- Test individual functions/methods in isolation
- No database or network calls
- Mock all dependencies
- **Location**: `test_user_model.py`

### Integration Tests (Medium)
- Test multiple components together
- Use mock database (mongomock)
- Test API endpoints
- **Location**: `test_deps.py`, `test_user_routes.py`

### E2E Tests (Slow)
- Test complete user flows
- Use real-like environment
- **Location**: Integration test classes with `TestEndpointIntegration`

## 🔧 Writing New Tests

### 1. Model Tests Example
```python
def test_my_new_feature():
    """Test description"""
    user = User(username="test", hashed_password="hash")
    
    result = user.my_new_method()
    
    assert result == expected_value
```

### 2. Endpoint Tests Example
```python
def test_my_endpoint(client, mock_db):
    """Test description"""
    # Setup
    with patch('app.api.v1.endpoints.user.mongo_db') as mock_mongo:
        mock_mongo.users_collection = mock_db["users"]
        
        # Execute
        response = client.post("/api/v1/user/endpoint", json={...})
        
        # Assert
        assert response.status_code == 200
        assert response.json()["key"] == "value"
```

## 🏆 Best Practices

1. ✅ **One assertion per test** (when possible)
2. ✅ **Descriptive test names** (`test_what_when_expected`)
3. ✅ **AAA Pattern**: Arrange, Act, Assert
4. ✅ **Use fixtures** for common setup
5. ✅ **Mock external dependencies**
6. ✅ **Test edge cases** and error conditions
7. ✅ **Keep tests independent**
8. ✅ **Clean up after tests**

## 📈 Continuous Integration

### GitHub Actions Example
```yaml
- name: Run tests
  run: |
    pip install -r tests/requirements-test.txt
    pytest --cov=app --cov-report=xml
```

## 🐛 Debugging Tests

### Run with Print Statements
```bash
pytest -s
```

### Run with Debugger
```bash
pytest --pdb
```

### See Full Error Traceback
```bash
pytest --tb=long
```

## 📝 Current Test Statistics

- **Total Tests**: 120+
- **User Model Tests**: 70+
- **Dependencies Tests**: 20+
- **Routes Tests**: 30+
- **Coverage Target**: >90%

## 🎨 Test Report

After running tests with coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

You'll see:
- Lines covered/missed
- Percentage coverage per file
- Missing line numbers

## ⚡ Performance

- **Unit tests**: ~0.001s each
- **Integration tests**: ~0.1-0.5s each
- **Full suite**: ~5-10s

## 🔒 Security Testing

Tests include:
- ✅ Password hashing verification
- ✅ Token validation
- ✅ Authorization checks
- ✅ Input validation
- ✅ SQL injection prevention (via MongoDB)
- ✅ XSS prevention (via Pydantic)

