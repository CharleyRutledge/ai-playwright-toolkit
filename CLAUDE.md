# AI Assistant Rules for Playwright Automation Project

## Project Context
This is a Playwright automation testing project using Python, Pytest, and following AI-assisted testing practices.

## Core Rules
1. **Always use Playwright for browser automation** - Follow official Playwright documentation
2. **Use Pytest as the test framework** - Follow pytest best practices
3. **Python is the programming language** - Use Python 3.8+ features
4. **Use Context7 MCP** - Always retrieve latest library documentation via Context7
5. **Use Playwright MCP** - Use Playwright MCP to explore websites and find locators
6. **Use Sequential Thinking MCP** - Break down complex problems systematically

## Code Quality Standards
1. **Comments** - Write short, concise comments for all code
2. **Documentation** - Provide overview of functionality in docstrings
3. **Naming** - Use descriptive names following Python conventions (snake_case for functions, PascalCase for classes)
4. **Type Hints** - Use type hints for function parameters and return values

## Testing Standards
1. **Locators** - Use accessibility-first locators (getByRole, getByLabel, getByText)
2. **Assertions** - Use web-first assertions that auto-retry (expect)
3. **Page Objects** - Use Page Object Model for maintainability
4. **Test Organization** - Use class-based organization with descriptive names
5. **No Sleep** - Never use sleep(), always use explicit waits

## Reporting Standards
1. **Allure Reports** - Use Allure for test reporting
2. **Screenshots** - Capture screenshots on test failure
3. **Traces** - Save execution traces for debugging
4. **Videos** - Record videos for failed tests

## File Organization
- `tests/` - Test files (test_*.py)
- `page_objects/` - Page Object Model classes
- `fixtures/` - Custom pytest fixtures
- `utils/` - Helper functions and utilities
- `data/` - Test data files (JSON, YAML, factories)
- `rules/` - Project rules and guidelines
- `prompts/` - AI prompts for automation tasks
- `instructions/` - Project instructions

## Workflow
1. **Before coding** - Review rules and ensure compliance
2. **During coding** - Use MCPs (Context7, Playwright, Sequential Thinking)
3. **After coding** - Verify no deviations from rules
4. **If deviation found** - Fix immediately

## MCP Usage
- Use Context7 MCP for retrieving up-to-date documentation
- Use Playwright MCP for exploring websites and finding locators
- Use Sequential Thinking MCP for complex problem-solving
- Use Fetch MCP for accessing URLs and processing web page data

## Maintenance
- Update requirements.txt when adding new dependencies
- Update README.md when adding new functionality
- Keep all documentation in sync with code changes
