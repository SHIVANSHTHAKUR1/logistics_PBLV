# Test Suite

This directory contains all test files for the project.

## Test Structure
- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for component interactions
- `e2e/` - End-to-end tests for complete workflows
- `fixtures/` - Test data and mock objects
- `utils/` - Test utilities and helpers

## Running Tests
1. Install test dependencies
2. Run unit tests: `python -m pytest tests/unit/`
3. Run integration tests: `python -m pytest tests/integration/`
4. Run all tests: `python -m pytest tests/`

## Test Guidelines
- Write tests for all critical functionality
- Maintain good test coverage (aim for >80%)
- Use descriptive test names
- Keep tests independent and isolated
