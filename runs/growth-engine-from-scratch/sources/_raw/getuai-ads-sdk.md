# Repo: getuai-ads-sdk

## README.md
```markdown
# GetU AI Ads SDK

A comprehensive Python SDK for user authentication, third-party credentials management, and project configuration in advertising platforms.

## Features

- **User Authentication**: Token-based user authentication with Redis caching
- **Third-party Credentials**: Manage Google Ads, Meta Ads, and TikTok Ads credentials
- **Project Management**: Create, update, and manage project configurations
- **Caching**: Redis-based caching for improved performance
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Async Support**: Full async/await support for all operations

## Installation

### From Source

Add to `requirements.txt`:

```bash
git+https://github.com/Optiminds-Inc/getuai-ads-sdk.git@main
```

Or install locally:

```bash
git clone <repository-url>
cd ads-sdk
pip install -e .
```

## Quick Start

### Basic Usage

```python
import asyncio
from getuai_ads_sdk import GetUAdsSDK, PlatformType

async def main():
    # Initialize SDK
    sdk = GetUAdsSDK()

    try:
        # Get user information
        user = await sdk.get_user_by_token("your_access_token")
        if user:
            print(f"User: {user.name} ({user.email})")

            # Get user projects
            projects = await sdk.projects.get_user_projects(user.id, "your_access_token")
            print(f"User has {len(projects.get('list', []))} projects")

            # Get third-party credentials
            google_creds = await sdk.get_google_credentials(user.id)
            if google_creds:
                print("Google Ads credentials available")

    finally:
        # Close SDK connections
        await sdk.close()

asyncio.run(main())
```

### Using Context Manager

```python
import asyncio
from getuai_ads_sdk import GetUAdsSDK

async def main():
    async with GetUAdsSDK() as sdk:
        # SDK is automatically initialized and will be closed when exiting context
        user = await sdk.get_user_by_token("your_access_token")
        if user:
            print(f"User: {user.name}")

asyncio.run(main())
```

## Configuration

The SDK can be configured using environment variables or a configuration object:

```python
from getuai_ads_sdk import GetUAdsSDK, SDKConfig

# Method 1: Environment variables
# export REDIS_HOST=localhost
# export REDIS_PORT=6379
# export GETUAI_API_BASE_URL=http://localhost:8001

sdk = GetUAdsSDK()  # Loads from environment variables

# Method 2: Configuration object
config = SDKConfig(
    redis_host="localhost",
    redis_port=6379,
    api_base_url="http://localhost:8001"
)

sdk = GetUAdsSDK(config)
```

## API Reference

### Core Classes

#### GetUAdsSDK

Main SDK class providing access to all services.

```python
sdk = GetUAdsSDK(config=None)
await sdk.close()
```

#### SDKConfig

Configuration class for SDK settings.

```python
config = SDKConfig(
    redis_host="localhost",
    redis_port=6379,
    api_base_url="http://localhost:8001",
    cache_ttl=10
)
```

### Authentication Service

#### Get User Information

```python
user = await sdk.get_user_by_token(access_token)
```

### Credentials Service

#### Get Google Ads Credentials

```python
credentials = await sdk.get_google_credentials(user_id)
```

#### Get Meta Ads Credentials

```python
access_token = await sdk.get_meta_credentials(user_id)
```

#### Get TikTok Ads Credentials

```python
access_token = await sdk.get_tiktok_credentials(user_id)
```

### Project Service

#### Get Project Configuration

```python
project = await sdk.get_project(user_id, project_id, access_token)
```

#### Get User Projects

```python
projects = await sdk.projects.get_user_projects(user_id, access_token, page=1, page_size=10)
```

#### Get Project Integrations

```python
integrations = await sdk.get_project_integrations(user_id, project_id, access_token)
```

### Service Properties

You can also access services directly:

```python
# Auth service
user = await sdk.auth.get_user_by_token(access_token)

# Credentials service
google_creds = await sdk.credentials.get_google_credentials(user_id)
meta_creds = await sdk.credentials.get_meta_credentials(user_id)
tiktok_creds = await sdk.credentials.get_tiktok_credentials(user_id)

# Project service
projects = await sdk.projects.get_user_projects(user_id, access_token)
project = await sdk.projects.get_project(user_id, project_id, access_token)
```

## Data Models

### User

```python
from getuai_ads_sdk import User

user = User(
    id="user123",
    email="user@example.com",
    name="John Doe",
    company="Example Corp"
)
```

### ProjectConfig

```python
from getuai_ads_sdk import ProjectConfig

project = ProjectConfig(
    id="project123",
    title="My Project",
    type="copilot",
    description="Project description"
)
```

### PlatformType Enum

```python
from getuai_ads_sdk import PlatformType

platforms = [PlatformType.GOOGLE, PlatformType.META, PlatformType.TIKTOK]
```

## Error Handling

The SDK provides custom exceptions for different error types:

```python
from getuai_ads_sdk.exceptions import (
    SDKError, AuthenticationError, CredentialsError,
    ProjectError, NetworkError, CacheError
)

try:
    user = await sdk.get_user_by_token(access_token)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except NetworkError as e:
    print(f"Network error: {e}")
except SDKError as e:
    print(f"SDK error: {e}")
```

## Configuration

### Environment Variables

| Variable                 | Default                 | Description            |
| ------------------------ | ----------------------- | ---------------------- |
| `REDIS_HOST`             | `localhost`             | Redis server host      |
| `REDIS_PORT`             | `6379`                  | Redis server port      |
| `REDIS_DB`               | `0`                     | Redis database number  |
| `REDIS_PASSWORD`         | `None`                  | Redis password         |
| `REDIS_SSL`              | `false`                 | Enable SSL for Redis   |
| `GETUAI_API_BASE_URL`    | `http://localhost:8001` | API base URL           |
| `GETUAI_API_TIMEOUT`     | `30`                    | API request timeout    |
| `GETUAI_API_MAX_RETRIES` | `3`                     | Maximum retry attempts |
| `GETUAI_LOG_LEVEL`       | `INFO`                  | Logging level          |
| `GETUAI_CACHE_TTL`       | `10`                    | Cache TTL in seconds   |

### Configuration Object

```python
config = SDKConfig(
    # Redis settings
    redis_host="localhost",
    redis_port=6379,
    redis_db=0,
    redis_password=None,
    redis_ssl=False,
    redis_timeout=30,
    redis_max_connections=10,

    # API settings
    api_base_url="http://localhost:8001",
    api_timeout=30,
    api_max_retries=3,
    api_key=None,

    # General settings
    log_level="INFO",
    cache_ttl=10
)
```

## Examples

See the `examples/` directory for complete usage examples:

- `basic_usage.py`: Basic SDK usage
- `advanced_usage.py`: Advanced features and error handling

## Development

### Setup Development Environment

```bash
git clone <repository-url>
cd ads-sdk
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_sdk.py

# Run with coverage
pytest --cov=getuai_ads_sdk
```

### Building and Publishing

```bash
# Build package
python -m build

# Check package
twine check dist/*

# Publish to PyPI
twine upload dist/*
```

## API Endpoints

The SDK connects to the following API endpoints (based on v2-ai project):

### Authentication

- `GET /auth/me` - Get current user information

### Third-party Credentials

- `POST /auth/refresh_third_party_auth` - Refresh third-party credentials

### Projects

- `GET /project/get/{project_id}` - Get project configuration
- `POST /project/paginate` - Get paginated user projects

## License

MIT License - see LICENSE file for details.

## Support

For support and questions, please contact the GetU AI team.

```
