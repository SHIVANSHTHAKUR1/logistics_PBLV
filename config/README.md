# Configuration Files

This directory contains configuration files for the project.

## Contents
- `config.json` - Main configuration file
- `database.conf` - Database configuration
- `env/` - Environment-specific configurations
  - `development.conf`
  - `testing.conf`
  - `production.conf`
- `logging.conf` - Logging configuration
- `security.conf` - Security settings

## Configuration Guidelines
- Use JSON or YAML format for configuration files
- Separate configurations by environment
- Never commit sensitive information (passwords, API keys)
- Use environment variables for sensitive data
- Document all configuration options
