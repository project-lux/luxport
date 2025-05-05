# Contributing to LuxPort

Thank you for considering contributing to LuxPort! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in the [Issues](https://github.com/williamjbmattingly/luxport/issues).
2. If not, create a new issue using the bug report template.
3. Provide a clear description of the issue, including steps to reproduce, expected behavior, and any relevant code snippets or screenshots.

### Suggesting Enhancements

1. Check if the enhancement has already been suggested in the [Issues](https://github.com/williamjbmattingly/luxport/issues).
2. If not, create a new issue using the feature request template.
3. Describe the enhancement you'd like to see, why it would be useful, and how it should work.

### Pull Requests

1. Fork the repository.
2. Create a new branch for your feature or bugfix (`git checkout -b feature/amazing-feature`).
3. Make your changes.
4. Add or update tests for your changes.
5. Make sure all tests pass.
6. Update documentation if necessary.
7. Commit your changes with a meaningful commit message.
8. Push to your branch.
9. Open a pull request to the `main` branch.

## Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/yourusername/luxport.git
   cd luxport
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Run tests to ensure everything is working:
   ```bash
   python tests.py
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines.
- Write docstrings following [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).
- Add type hints to function parameters and return values.
- Write tests for new features or bug fixes.

## Commit Messages

- Use clear, descriptive commit messages.
- Start with a short summary (50 chars or less) written in the imperative mood.
- Optionally, follow with a blank line and a more detailed explanation.

## License

By contributing to LuxPort, you agree that your contributions will be licensed under the project's [MIT License](LICENSE). 