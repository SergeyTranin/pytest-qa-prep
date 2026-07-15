# pytest-qa-prep: Professional QA Automation Framework

[![CI](https://github.com/SergeyTranin/pytest-qa-prep/actions/workflows/ci.yml/badge.svg)](https://github.com/SergeyTranin/pytest-qa-prep/actions)

A **production-grade QA automation framework** built with Python, pytest, and Playwright. Demonstrates professional software engineering practices through API automation, UI automation, and enterprise-ready architecture.

**Perfect for QA engineer job interviews** - showcases design patterns, testing strategies, and architectural decisions.

---

## 🎯 What This Framework Demonstrates

### Design Patterns
- ✅ **Page Object Model** - Maintainable UI tests that survive UI changes
- ✅ **Wrapper Pattern** - Centralized HTTP communication layer
- ✅ **Fixture Pattern** - Automatic setup/teardown with proper resource management
- ✅ **Factory Pattern** - Realistic test data generation

### Testing Architecture
- ✅ **Separation of Concerns** - API and UI layers are independent
- ✅ **DRY Principle** - No code duplication through inheritance
- ✅ **Test Isolation** - Each test gets a fresh environment
- ✅ **Configuration Management** - Environment-driven, not hardcoded

### Professional Practices
- ✅ **66 comprehensive tests** - Well-organized by functionality
- ✅ **~6,000 lines of code** - Production-quality implementation
- ✅ **Complete documentation** - Architecture, patterns, interview tips
- ✅ **CI/CD ready** - Automated testing pipeline included

---

## 📂 Project Structure

```
pytest-qa-prep/
│
├── 📂 api/                         # REST API Testing Layer
│   ├── 📂 clients/                 # HTTP communication
│   │   ├── base_client.py         # Base HTTP wrapper
│   │   ├── auth_client.py         # Authentication API
│   │   └── booking_client.py      # Booking CRUD API
│   ├── 📂 models/                  # Data structures
│   │   ├── auth.py
│   │   └── booking.py
│   └── 📂 tests/                   # API test suite (28 tests)
│       ├── test_create_booking.py
│       ├── test_get_booking.py
│       ├── test_update_booking.py
│       └── test_delete_booking.py
│
├── 📂 ui/                          # Web UI Testing Layer
│   ├── 📂 pages/                   # Page Object Model
│   │   ├── base_page.py           # Base page with common methods
│   │   ├── login_page.py          # Login page object
│   │   └── booking_page.py        # Booking page object
│   ├── 📂 tests/                   # UI test suite (38 tests)
│   │   ├── test_login.py
│   │   └── test_booking.py
│   ├── conftest.py                # UI-specific fixtures
│   └── README.md                  # UI framework guide
│
├── 📂 utils/                       # Shared Utilities
│   ├── constants.py               # Centralized configuration
│   ├── data_generator.py          # Test data generation
│   ├── assertions.py              # Custom assertions
│   └── __init__.py
│
├── 📂 config/                      # Application Configuration
│   ├── settings.py                # Environment settings
│   └── __init__.py
│
├── 📂 docs/                        # Documentation
│   ├── ARCHITECTURE.md            # Complete architecture guide
│   ├── TEST_STRATEGY.md           # What and why we test
│   └── BEST_PRACTICES.md          # Team guidelines
│
├── conftest.py                    # Root pytest configuration
├── pyproject.toml                 # Pytest & project config
├── pytest.ini                     # Additional pytest options
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── .gitignore
```

---

## 📊 Framework Statistics

| Component | Count | Lines |
|-----------|-------|-------|
| **API Tests** | 28 | 1,475 |
| **UI Tests** | 38 | 1,514 |
| **Utilities** | 4 files | 2,100 |
| **Documentation** | 1 file | 812 |
| **TOTAL** | **66 tests** | **~5,900 lines** |

---

## 🚀 Quick Start

### Prerequisites
```bash
# Python 3.9+
python3 --version

# Install pip packages
pip3 install pytest playwright requests python-dotenv

# Install Playwright browsers
python3 -m playwright install
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SergeyTranin/pytest-qa-prep.git
cd pytest-qa-prep
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
# or
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables (optional):
```bash
export ENVIRONMENT=local
export HEADLESS=true
```

---

## ▶️ Running Tests

### Run All Tests
```bash
pytest -v
```

### Run by Layer
```bash
# API tests only
pytest api/tests/ -v

# UI tests only
pytest ui/tests/ -v
```

### Run Specific Test
```bash
# Single test
pytest api/tests/test_create_booking.py::TestCreateBooking::test_create_booking_success -v

# Single test class
pytest ui/tests/test_login.py::TestLoginPageElements -v

# Show browser (UI only)
pytest ui/tests/ -v --headed

# Different browser
pytest ui/tests/ -v --browser firefox
```

### Filter by Marker
```bash
# Run only API tests
pytest -m api -v

# Run only UI tests
pytest -m ui -v

# Run smoke tests (critical path)
pytest -m smoke -v

# Exclude slow tests
pytest -m "not slow" -v

# Combine markers
pytest -m "api and not slow" -v
```

### Custom Options
```bash
# Change environment
pytest --environment staging

# Enable verbose logging
pytest --verbose-logging

# Parallel execution (requires pytest-xdist)
pip install pytest-xdist
pytest -n auto
```

---

## 📚 Documentation

### Architecture Guide
Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for:
- Complete architecture overview
- Design pattern explanations
- Component interaction diagrams
- **Interview talking points**

### API Framework
Framework uses 3-layer architecture:
```
Tests (what to validate)
  ↓
Clients (how to interact with API)
  ↓
HTTP Library (low-level communication)
```

Key files:
- `api/clients/base_client.py` - HTTP wrapper with error handling
- `api/clients/booking_client.py` - High-level API methods
- `api/models/booking.py` - Data structures with type hints

### UI Framework
Framework uses Page Object Model pattern:
```
Tests (business logic)
  ↓
Page Objects (UI interactions)
  ↓
Playwright (browser automation)
```

Key files:
- `ui/pages/base_page.py` - Common methods for all pages
- `ui/pages/login_page.py` - Login interactions
- `ui/pages/booking_page.py` - Booking CRUD operations
- [ui/README.md](ui/README.md) - Detailed UI guide

### Utilities

**Constants** (`utils/constants.py`):
- Centralized test credentials
- API/UI URLs
- Timeouts and status codes
- Error messages
- Test data ranges

**Data Generators** (`utils/data_generator.py`):
- `DataGenerator` - Random test data
- `BookingDataGenerator` - Realistic booking data
- `AuthDataGenerator` - Login credentials
- `FormDataGenerator` - Form data with validation

**Assertions** (`utils/assertions.py`):
- `assert_close()` - Float comparison
- `assert_in_range()` - Range validation
- `assert_valid_email()` - Email format
- `assert_has_keys()` - Required fields
- `assert_response_success()` - HTTP responses

---

## 💡 Interview Preparation

This framework demonstrates:

### Architecture Knowledge
- ✅ Why separate API and UI tests
- ✅ Why use Page Object Model
- ✅ How to organize tests by functionality
- ✅ How to manage configuration

### Design Patterns
- ✅ Inheritance to reduce duplication (DRY)
- ✅ Fixtures for test isolation
- ✅ Parametrization for scalable tests
- ✅ Markers for test categorization

### Best Practices
- ✅ Type hints for clarity
- ✅ Comprehensive error handling
- ✅ Centralized constants
- ✅ Professional documentation

### Talking Points
Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for:
1. "Tell me about your testing architecture"
2. "Why did you make these design choices?"
3. "How would you extend this framework?"
4. "What if a test fails in CI?"
5. "How many tests do you have?"

---

## 🔄 CI/CD Integration

Tests run automatically on push via GitHub Actions:

```yaml
# .github/workflows/ci.yml
- Run linting
- Run API tests
- Run UI tests
- Generate report
```

To run locally:
```bash
# Lint with ruff
ruff check .

# Format with ruff
ruff format .

# Run tests
pytest -v --junitxml=report.xml
```

---

## 🎓 Learning Path

### Beginners
1. Read the structure overview
2. Run a single test: `pytest api/tests/test_create_booking.py::TestCreateBooking::test_create_booking_success -v`
3. Look at test code to understand patterns
4. Modify a test and run it

### Intermediate
1. Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. Update tests to use `utils.constants` instead of hardcoded values
3. Use `DataGenerator` for parametrized tests
4. Add a new test following existing patterns

### Advanced
1. Understand why each design pattern is used
2. Add a new page object and tests
3. Create a new client for additional API
4. Practice explaining architecture to others

---

## 🛠️ Extending the Framework

### Add New Test
1. Identify which file to modify
2. Create test class following existing patterns
3. Use existing page objects or clients
4. Use `DataGenerator` for test data

Example:
```python
# ui/tests/test_booking.py
class TestBookingValidation:
   def test_booking_price_required(self, authenticated_page):
       booking_page = BookingPage(authenticated_page)
       booking_page.create_booking_without_price()
       assert booking_page.has_error_message("Price is required")
```

### Add New Page Object
1. Create class extending `BasePage`
2. Define element locators
3. Create methods for user interactions
4. Create corresponding test file

```python
# ui/pages/profile_page.py
class ProfilePage(BasePage):
   USERNAME_FIELD = "#username"
   SAVE_BUTTON = "button.save"
    
   def update_username(self, username: str):
       self.fill(self.USERNAME_FIELD, username)
       self.click(self.SAVE_BUTTON)
```

### Add New API Client
1. Create class extending `BaseClient`
2. Define API endpoints
3. Create methods for CRUD operations
4. Create corresponding test file

```python
# api/clients/profile_client.py
class ProfileClient(BaseClient):
   def get_profile(self, user_id: str):
       return self.get(f'/users/{user_id}/profile')
```

---

## 🐛 Troubleshooting

### Tests fail with "ModuleNotFoundError"
```bash
# Install missing package
pip install pytest playwright requests python-dotenv

# Ensure you're in venv
source venv/bin/activate
```

### Playwright tests hang or timeout
```bash
# Increase timeout
pytest ui/tests/ --timeout=120

# Check if test site is accessible
curl https://automationintesting.online
```

### Element not found in UI tests
```bash
# Run with visible browser
pytest ui/tests/test_login.py --headed

# Add debugging
login_page.wait_for_element('button', timeout=15)
login_page.take_screenshot()
```

### Flaky tests
```bash
# Run test multiple times
pytest api/tests/test_create_booking.py -v --count=5

# Increase timeouts
# Adjust in utils/constants.py: TIMEOUTS['element_wait'] = 15
```

---

## 📈 Next Steps

1. **Run tests**: `pytest -v`
2. **Read architecture**: Open [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
3. **Explore code**: Review API and UI implementations
4. **Practice explaining**: Tell someone about the design patterns
5. **Interview ready**: You can now explain professional QA automation!

---

## 📝 Project History

This project evolved from basic pytest exercises to a professional framework:
- Started with simple calculator unit tests
- Added API testing layer with proper architecture
- Added UI testing with Page Object Model
- Added comprehensive documentation and utilities
- Now: Enterprise-ready framework with ~6,000 lines of code

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

This is a portfolio/interview-focused project. Feel free to:
- Fork and experiment
- Modify patterns to learn
- Add new tests and pages
- Extend with your own ideas

---

## ✨ Key Files to Review

For **architecture understanding**:
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - Complete guide

For **API patterns**:
- [api/clients/base_client.py](api/clients/base_client.py) - HTTP wrapper
- [api/clients/booking_client.py](api/clients/booking_client.py) - API methods

For **UI patterns**:
- [ui/pages/base_page.py](ui/pages/base_page.py) - Common methods
- [ui/pages/login_page.py](ui/pages/login_page.py) - Page object example
- [ui/README.md](ui/README.md) - UI framework details

For **utilities**:
- [utils/constants.py](utils/constants.py) - Centralized config
- [utils/data_generator.py](utils/data_generator.py) - Test data

---

## 🎉 Ready for Your QA Engineer Interview!

This framework demonstrates:
- ✅ Professional software engineering skills
- ✅ Understanding of testing best practices
- ✅ Ability to design scalable frameworks
- ✅ Knowledge of Python, pytest, and Playwright
- ✅ Clear architectural thinking

**Good luck!** 🚀

---

*Last updated: July 2025*
*Built by: Kristina Tranina*
*Repository: [SergeyTranin/pytest-qa-prep](https://github.com/SergeyTranin/pytest-qa-prep)*