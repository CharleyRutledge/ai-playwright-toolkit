# Contributing to Playwright Automation Framework

Thank you for your interest in contributing to this AI-assisted Playwright automation framework!

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Rules](#project-rules)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [AI-Assisted Development](#ai-assisted-development)

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/playwright-automation-framework.git
   cd playwright-automation-framework
   ```

3. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

1. **Install Python dependencies:**
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

3. **Install development dependencies:**
   ```bash
   pip install black flake8 mypy pytest-cov
   ```

4. **Set up environment variables:**
   ```bash
   cp env.template .env
   # Edit .env with your configuration
   ```

## Project Rules

This project follows strict rules defined in the `rules/` directory:

### Core Rules (from `rules/Starting Rules.md`)

1. **Use Playwright** for browser automation
2. **Use Pytest** for test framework
3. **Use Python** as the programming language
4. **Use Context7 MCP** to retrieve latest documentation
5. **Use Playwright MCP** to explore websites and find locators
6. **Use Sequential Thinking MCP** for complex problem-solving
7. **Follow official Playwright documentation** only

### Testing Rules (from `rules/Testing Rules.md`)

1. **Write short, concise comments** for all code
2. **Use accessibility-first locators** (getByRole, getByLabel, getByText)
3. **Use web-first assertions** that auto-retry
4. **No sleep() calls** - use explicit waits only
5. **Iterate over all code** to ensure rule compliance

### Reporting Rules (from `rules/Reporting.md`)

1. **Use Allure for reporting** - https://allurereport.org/docs/playwright/
2. **Save reports after each test**
3. **Remove other reporting functionality** if implemented

## Coding Standards

### Python Style Guide

- Follow PEP 8 guidelines
- Use Black for code formatting (line length: 100)
- Use type hints for function parameters and return values
- Write docstrings for all classes and functions

### Naming Conventions

- **Files**: `snake_case.py` (e.g., `test_homepage.py`)
- **Classes**: `PascalCase` (e.g., `PlaywrightHomePage`)
- **Functions/Methods**: `snake_case` (e.g., `navigate_to_home`)
- **Constants**: `UPPER_CASE` (e.g., `BASE_URL`)

### Code Formatting

Run Black before committing:
```bash
black page_objects/ utils/ fixtures/ tests/
```

Run Flake8 for linting:
```bash
flake8 page_objects/ utils/ fixtures/ tests/ --max-line-length=100
```

Run MyPy for type checking:
```bash
mypy page_objects/ utils/ fixtures/
```

## Testing Guidelines

### Test Structure

1. **File naming**: `test_*.py`
2. **Class naming**: `Test[FeatureName]`
3. **Method naming**: `test_[description]`

Example:
```python
class TestHomepage:
    def test_homepage_loads_successfully(self, page: Page):
        """Test that homepage loads successfully."""
        # Test implementation
        pass
```

### Writing Tests

1. **Use Page Object Model**:
   ```python
   from page_objects.playwright_home_page import PlaywrightHomePage
   
   def test_example(page: Page):
       home_page = PlaywrightHomePage(page)
       home_page.navigate_to_home()
       home_page.search("python")
   ```

2. **Use accessibility-first locators**:
   ```python
   # Good
   page.get_by_role("button", name="Search")
   page.get_by_label("Email")
   page.get_by_text("Submit")
   
   # Avoid
   page.locator("#search-button")
   page.locator(".email-input")
   ```

3. **Use web-first assertions**:
   ```python
   # Good
   expect(page).to_have_title("Expected Title")
   expect(element).to_be_visible()
   
   # Avoid
   assert page.title() == "Expected Title"
   assert element.is_visible()
   ```

4. **Add Allure decorators**:
   ```python
   import allure
   
   @allure.title("Test Homepage Navigation")
   @allure.description("Verify homepage navigation works correctly")
   @allure.severity(allure.severity_level.CRITICAL)
   @pytest.mark.smoke
   def test_homepage_navigation(self, page: Page):
       # Test implementation
       pass
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_example.py

# Run with specific browser
pytest --browser firefox

# Run with markers
pytest -m smoke
pytest -m "not slow"

# Run with coverage
pytest --cov=page_objects --cov=utils --cov=fixtures
```

## Submitting Changes

1. **Ensure all tests pass**:
   ```bash
   pytest tests/ -v
   ```

2. **Format code**:
   ```bash
   black page_objects/ utils/ fixtures/ tests/
   ```

3. **Check linting**:
   ```bash
   flake8 page_objects/ utils/ fixtures/ tests/
   ```

4. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: description of your changes"
   ```

   Use conventional commit messages:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `test:` - Test changes
   - `refactor:` - Code refactoring
   - `style:` - Code style changes
   - `chore:` - Maintenance tasks

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**:
   - Provide a clear description of changes
   - Reference any related issues
   - Ensure CI/CD checks pass

## AI-Assisted Development

This project is designed to work with AI assistants (Cursor, GitHub Copilot, etc.):

### Using Project Rules

The `.cursorules` file defines project-specific rules for AI assistants. Review this file to understand the automated guidance.

### Using Prompts

The `prompts/` directory contains reusable prompts:

- `generate-tests.prompt.md` - Generate comprehensive tests
- `explore-website.prompt.md` - Explore and document websites
- `automate-form.prompt.md` - Automate form testing
- `test-fail-fix.prompt.md` - Fix failing tests

### Using MCPs (Model Context Protocols)

1. **Context7 MCP** - Retrieve latest library documentation
2. **Playwright MCP** - Explore websites and find locators
3. **Sequential Thinking MCP** - Break down complex problems
4. **Fetch MCP** - Access and process web page data

## Questions?

If you have questions:

1. Check the [README.md](README.md) for basic information
2. Review the `rules/` directory for project rules
3. Check existing issues on GitHub
4. Create a new issue with your question

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Thank You!

Thank you for contributing to this project and helping make it better!

