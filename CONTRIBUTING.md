# Contributing to Trading Analysis MVP

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/RamsesAguirre777/trading-analysis-mvp/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/RamsesAguirre777/trading-analysis-mvp/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists or is planned
2. Describe the problem you're trying to solve
3. Describe the solution you'd like
4. Describe alternatives you've considered
5. Add any additional context

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/trading-analysis-mvp.git
cd trading-analysis-mvp

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Test the calculator
python src/trading_calculator.py --input data/nvda_test_data.json --pretty
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where appropriate
- Comment complex logic

## Testing

- Write tests for new features
- Ensure existing tests pass
- Test with real market data when possible
- Include edge cases in tests

## Documentation

- Update README.md if needed
- Add docstrings to new functions
- Update API documentation
- Include examples in documentation

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## Questions?

Feel free to open an issue with your questions or contact the maintainers directly.

Thank you for contributing! 🚀