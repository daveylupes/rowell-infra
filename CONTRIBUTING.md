# Contributing to Rowell Infra

Thank you for your interest in contributing to **Rowell Infra** - Alchemy for Africa! We welcome contributions from the community and are excited to work together to build the future of African fintech infrastructure.

## 🚀 Getting Started

### Prerequisites

- Node.js 16+ and npm
- Python 3.11+
- Docker and Docker Compose
- Git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/rowell-infra.git
   cd rowell-infra
   ```

2. **Install dependencies**
   ```bash
   make install
   ```

3. **Start development environment**
   ```bash
   make dev
   ```

4. **Verify setup**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Grafana: http://localhost:3000 (admin/admin)

## 📋 How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fix issues in existing code
- **Features**: Add new functionality
- **Documentation**: Improve docs, examples, and guides
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **Security**: Improve security measures

### Contribution Process

1. **Create an issue** (if one doesn't exist)
   - Describe the problem or feature request
   - Use appropriate labels
   - Provide context and examples

2. **Fork the repository**
   ```bash
   git fork https://github.com/rowell-infra/rowell-infra.git
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

4. **Make your changes**
   - Write clean, readable code
   - Add tests for new functionality
   - Update documentation as needed
   - Follow our coding standards

5. **Test your changes**
   ```bash
   make test
   make lint
   make format
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Provide a clear description
   - Reference related issues
   - Include screenshots for UI changes
   - Request reviews from maintainers

## 📝 Coding Standards

### Python (API)

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Use `black` for formatting
- Use `isort` for import sorting

```python
def create_account(
    network: str,
    environment: str,
    account_type: str
) -> Account:
    """
    Create a new account on the specified network.
    
    Args:
        network: Network type ('stellar' or 'hedera')
        environment: Environment ('testnet' or 'mainnet')
        account_type: Type of account ('user', 'merchant', etc.)
        
    Returns:
        Account object with account details
        
    Raises:
        ValueError: If invalid parameters provided
    """
    # Implementation here
```

### JavaScript/TypeScript (SDKs)

- Use TypeScript for type safety
- Follow ESLint configuration
- Use Prettier for formatting
- Write JSDoc comments

```typescript
/**
 * Create a new account on the specified network
 * @param network - Network type ('stellar' or 'hedera')
 * @param environment - Environment ('testnet' or 'mainnet')
 * @param accountType - Type of account ('user', 'merchant', etc.)
 * @returns Promise resolving to Account object
 */
async createAccount(
  network: Network,
  environment: Environment,
  accountType: AccountType
): Promise<Account> {
  // Implementation here
}
```

### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Build/tooling changes

Examples:
```
feat(api): add support for Hedera token transfers
fix(sdk): resolve account balance calculation issue
docs(quickstart): update installation instructions
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test suites
cd api && python -m pytest tests/ -v
cd sdk/js && npm test
cd sdk/python && python -m pytest tests/ -v
```

### Writing Tests

- Write unit tests for new functionality
- Include integration tests for API endpoints
- Test error cases and edge conditions
- Aim for high test coverage

Example test:

```python
import pytest
from api.services.account_service import AccountService

@pytest.mark.asyncio
async def test_create_account():
    """Test account creation functionality."""
    service = AccountService(db_session)
    
    account = await service.create_account(
        network="stellar",
        environment="testnet",
        account_type="user"
    )
    
    assert account.network == "stellar"
    assert account.environment == "testnet"
    assert account.account_type == "user"
    assert account.is_active is True
```

## 📚 Documentation

### API Documentation

- Update OpenAPI/Swagger specs when adding endpoints
- Include request/response examples
- Document error codes and messages

### SDK Documentation

- Update README files for SDKs
- Include code examples
- Document breaking changes

### Guides and Tutorials

- Write clear, step-by-step guides
- Include code examples
- Test all examples before publishing

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs actual behavior
4. **Environment details** (OS, Node version, etc.)
5. **Error messages** and logs
6. **Screenshots** if applicable

## 💡 Feature Requests

When requesting features, please include:

1. **Clear description** of the feature
2. **Use case** and motivation
3. **Proposed implementation** (if you have ideas)
4. **Alternative solutions** considered
5. **Additional context** and examples

## 🔒 Security

### Reporting Security Issues

For security vulnerabilities, please:

1. **DO NOT** create public issues
2. Email security@rowell-infra.com
3. Include detailed information about the vulnerability
4. Allow time for us to respond and fix the issue

### Security Best Practices

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Validate all inputs
- Follow secure coding practices

## 🌍 Community Guidelines

### Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please:

- Be respectful and inclusive
- Use welcoming and inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discord**: For community discussions
- **Email**: support@rowell-infra.com for support
- **Documentation**: Check docs first

## 🏆 Recognition

Contributors will be recognized in:

- CONTRIBUTORS.md file
- Release notes
- Community highlights
- Special badges and recognition

## 📄 License

By contributing to Rowell Infra, you agree that your contributions will be licensed under the MIT License.

## 🤝 Maintainers

Current maintainers:

- **Lead Maintainer**: [Your Name](https://github.com/your-username)
- **API Maintainer**: [API Maintainer](https://github.com/api-maintainer)
- **SDK Maintainer**: [SDK Maintainer](https://github.com/sdk-maintainer)

## 📞 Contact

- **Email**: contributors@rowell-infra.com
- **Discord**: [Join our community](https://discord.gg/rowell-infra)
- **Twitter**: [@RowellInfra](https://twitter.com/rowellinfra)

---

Thank you for contributing to Rowell Infra! Together, we're building the future of African fintech infrastructure. 🚀

**Built for Africa, by Africa** 🇰🇪🇳🇬🇿🇦🇬🇭🇺🇬
