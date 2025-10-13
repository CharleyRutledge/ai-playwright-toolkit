# Architecture Documentation

## Project Overview

This is an AI-assisted Playwright automation testing framework built with Python and Pytest. The framework follows best practices from official Playwright documentation and implements a modular, maintainable architecture.

## Architecture Diagram

```
Playwright-example/
│
├── Core Components
│   ├── page_objects/          # Page Object Model (POM)
│   │   ├── base_page.py       # Base class for all pages
│   │   └── *_page.py          # Specific page objects
│   │
│   ├── utils/                 # Utility functions
│   │   ├── helpers.py         # General helper functions
│   │   └── wait_helpers.py    # Wait and sync utilities
│   │
│   ├── fixtures/              # Custom pytest fixtures
│   │   ├── page_fixtures.py   # Page object fixtures
│   │   └── data_fixtures.py   # Test data fixtures
│   │
│   └── data/                  # Test data management
│       ├── test_data.json     # JSON test data
│       ├── test_data.yaml     # YAML test data
│       └── factories.py       # Data factory classes
│
├── Tests
│   └── tests/                 # Test files
│       ├── conftest.py        # Pytest configuration
│       └── test_*.py          # Test modules
│
├── Configuration
│   ├── .cursorules            # AI assistant rules
│   ├── pyproject.toml         # Project configuration
│   ├── pytest.ini             # Pytest configuration
│   ├── requirements.txt       # Python dependencies
│   └── env.template           # Environment template
│
├── AI Assistance
│   ├── rules/                 # Project rules
│   │   ├── Starting Rules.md  # Core project rules
│   │   ├── Testing Rules.md   # Testing standards
│   │   └── Reporting.md       # Reporting rules
│   │
│   ├── prompts/               # Reusable AI prompts
│   │   ├── generate-tests.prompt.md
│   │   ├── explore-website.prompt.md
│   │   └── *.prompt.md
│   │
│   ├── instructions/          # Project instructions
│   │   └── playwright.instructions.md
│   │
│   └── chatmodes/             # Chat mode configurations
│       ├── playwright-tester.chatmode.md
│       ├── test-explorer.chatmode.md
│       └── test-generator.chatmode.md
│
├── CI/CD
│   └── .github/workflows/     # GitHub Actions
│       └── playwright-tests.yml
│
└── Documentation
    ├── README.md              # Main documentation
    ├── CONTRIBUTING.md        # Contribution guide
    └── ARCHITECTURE.md        # This file
```

## Design Patterns

### 1. Page Object Model (POM)

**Purpose**: Separate page structure from test logic for better maintainability.

**Implementation**:
```python
# Base Page Object
class BasePage:
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str):
        self.page.goto(url)

# Specific Page Object
class PlaywrightHomePage(BasePage):
    @property
    def search_button(self) -> Locator:
        return self.page.get_by_role("button", name="Search")
    
    def search(self, query: str):
        self.search_button.click()
        self.search_box.fill(query)
```

**Benefits**:
- Reusable page components
- Easy to maintain locators
- Clear separation of concerns
- Reduces code duplication

### 2. Factory Pattern

**Purpose**: Generate test data dynamically.

**Implementation**:
```python
class UserFactory:
    @staticmethod
    def create_user(username=None, email=None):
        if username is None:
            username = f"user_{random_string(8)}"
        return UserData(username=username, email=email)
```

**Benefits**:
- Generates fresh test data
- Supports data-driven testing
- Easy to customize data
- Reduces test data maintenance

### 3. Fixture Pattern

**Purpose**: Provide reusable test setup and teardown.

**Implementation**:
```python
@pytest.fixture
def playwright_home_page(page: Page) -> PlaywrightHomePage:
    return PlaywrightHomePage(page)

def test_example(playwright_home_page):
    playwright_home_page.search("python")
```

**Benefits**:
- Reusable setup code
- Automatic cleanup
- Dependency injection
- Improved test readability

## Component Details

### Page Objects Layer

**Responsibility**: Encapsulate page structure and interactions.

**Key Features**:
- Base class with common functionality
- Property-based locators (lazy initialization)
- Accessibility-first selectors
- Method-based actions

**Example**:
```python
class PlaywrightHomePage(BasePage):
    @property
    def search_button(self) -> Locator:
        return self.page.get_by_role("button", name="Search")
    
    def search(self, query: str):
        self.search_button.click()
        self.search_box.fill(query)
```

### Utils Layer

**Responsibility**: Provide helper functions for common operations.

**Modules**:
- `helpers.py` - General utilities (timestamps, file operations, JSON handling)
- `wait_helpers.py` - Wait and synchronization utilities

**Example**:
```python
from utils.helpers import get_timestamp, save_json
from utils.wait_helpers import wait_for_element_visible

timestamp = get_timestamp()
wait_for_element_visible(locator, timeout=5000)
```

### Fixtures Layer

**Responsibility**: Provide reusable test fixtures.

**Modules**:
- `page_fixtures.py` - Page object fixtures
- `data_fixtures.py` - Test data fixtures

**Example**:
```python
@pytest.fixture
def playwright_home_page(page: Page):
    return PlaywrightHomePage(page)

def test_search(playwright_home_page):
    playwright_home_page.search("python")
```

### Data Layer

**Responsibility**: Manage test data.

**Components**:
- JSON files for static test data
- YAML files for configuration data
- Factory classes for dynamic data generation

**Example**:
```python
# Static data from JSON
data = load_json("data/test_data.json")

# Dynamic data from factory
user = UserFactory.create_user()
```

## Test Organization

### Test Structure

```python
import pytest
import allure
from playwright.sync_api import Page

class TestFeature:
    """Test class for specific feature."""
    
    @pytest.mark.smoke
    @allure.title("Test Title")
    @allure.description("Test description")
    def test_scenario(self, page: Page, playwright_home_page):
        """Test method with descriptive name."""
        # Arrange
        playwright_home_page.navigate_to_home()
        
        # Act
        playwright_home_page.search("python")
        
        # Assert
        expect(playwright_home_page.search_box).to_have_value("python")
```

### Test Markers

- `@pytest.mark.smoke` - Quick validation tests
- `@pytest.mark.regression` - Comprehensive tests
- `@pytest.mark.slow` - Long-running tests
- `@pytest.mark.integration` - Integration tests

## Configuration Management

### Environment Variables

Use `env.template` for environment-specific configuration:
- Base URLs
- Browser settings
- Test timeouts
- Authentication credentials
- API keys

### Pytest Configuration

`pytest.ini` contains:
- Test discovery patterns
- Default options
- Markers
- Allure configuration

### Project Configuration

`pyproject.toml` contains:
- Project metadata
- Dependencies
- Tool configurations (Black, MyPy, Coverage)

## Reporting and Monitoring

### Allure Reports

- Comprehensive test results
- Screenshots on failure
- Execution traces
- Test categorization
- Historical trends

### Test Artifacts

- Screenshots: `test-results/screenshot_*.png`
- Videos: `test-results/videos/`
- Traces: `test-results/trace_*.zip`
- Page content: `test-results/page_content_*.html`

## CI/CD Integration

### GitHub Actions Workflow

1. **Matrix Testing**: Tests run across multiple Python versions and browsers
2. **Parallel Execution**: Tests run in parallel for faster feedback
3. **Artifact Upload**: Test results and screenshots uploaded
4. **Report Generation**: Allure reports generated and published
5. **Code Quality**: Linting and type checking

### Workflow Stages

```
Checkout Code
    ↓
Setup Python
    ↓
Install Dependencies
    ↓
Install Browsers
    ↓
Run Tests (Matrix)
    ↓
Generate Reports
    ↓
Upload Artifacts
    ↓
Deploy Reports
```

## AI-Assisted Development

### Model Context Protocols (MCPs)

1. **Context7 MCP**: Retrieves latest library documentation
2. **Playwright MCP**: Explores websites and finds locators
3. **Sequential Thinking MCP**: Breaks down complex problems
4. **Fetch MCP**: Accesses and processes web pages

### AI Rules and Prompts

- Rules in `rules/` define project standards
- Prompts in `prompts/` provide reusable templates
- Instructions in `instructions/` guide development
- Chat modes in `chatmodes/` configure AI behavior

## Best Practices

### Locator Strategy

1. **Priority Order**:
   - `getByRole()` - Accessibility first
   - `getByLabel()` - Form elements
   - `getByText()` - Text content
   - `getByTestId()` - Last resort

2. **Avoid**:
   - CSS selectors
   - XPath
   - ID selectors

### Assertion Strategy

1. **Use Web-First Assertions**:
   ```python
   # Good
   expect(page).to_have_title("Title")
   expect(element).to_be_visible()
   
   # Avoid
   assert page.title() == "Title"
   assert element.is_visible()
   ```

2. **Auto-Retrying**: Web-first assertions automatically retry

### Wait Strategy

1. **Use Explicit Waits**:
   ```python
   element.wait_for(state="visible")
   page.wait_for_load_state("networkidle")
   ```

2. **Never Use Sleep**:
   ```python
   # Bad
   time.sleep(5)
   
   # Good
   element.wait_for(state="visible")
   ```

## Scalability Considerations

### Adding New Tests

1. Create page object in `page_objects/`
2. Add fixtures if needed in `fixtures/`
3. Add test data in `data/`
4. Create test file in `tests/`
5. Use appropriate markers

### Adding New Features

1. Update page objects
2. Add new utilities if needed
3. Create new fixtures
4. Update documentation
5. Add tests

### Performance Optimization

1. Use parallel execution: `pytest -n auto`
2. Use test markers to run subsets
3. Optimize page load waits
4. Cache browser installations
5. Use shared browser contexts

## Security Considerations

1. **Never commit secrets** - Use environment variables
2. **Use env.template** - Provide examples, not actual values
3. **Secure CI/CD** - Use GitHub secrets
4. **Validate inputs** - Sanitize test data
5. **Regular updates** - Keep dependencies current

## Maintenance

### Regular Tasks

1. Update dependencies quarterly
2. Review and update documentation
3. Clean up old test artifacts
4. Review and optimize slow tests
5. Update browser versions

### Monitoring

1. CI/CD pipeline health
2. Test execution times
3. Flaky test detection
4. Coverage trends
5. Allure report metrics

## Future Enhancements

1. API testing integration
2. Visual regression testing
3. Performance testing
4. Mobile testing support
5. Database integration
6. Test data management UI
7. Enhanced reporting dashboard

