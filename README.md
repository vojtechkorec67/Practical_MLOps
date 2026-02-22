# Practical MLOps

A Python project demonstrating best practices in MLOps including testing, linting, and CI/CD with GitHub Actions.

## Project Structure

```
Practical_MLOps/
├── hello.py              # Main application code
├── test_hello.py         # Unit tests
├── requirements.txt      # Python dependencies
├── Makefile              # Build automation
├── .gitignore            # Git ignore rules
└── .github/
    └── workflows/
        └── python-app.yml   # GitHub Actions CI/CD
```

## Setup

### Prerequisites
- Python 3.13+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/vojtechkorec67/Practical_MLOps.git
cd Practical_MLOps
```

2. Create and activate virtual environment:
```bash
python3 -m venv ~/.Practical_MLOps
source ~/.Practical_MLOps/bin/activate
```

3. Install dependencies:
```bash
make install
```

## Usage

### Run all checks (install, lint, test)
```bash
make all
```

### Run individual commands
```bash
make install    # Install dependencies
make lint       # Run pylint checks
make test       # Run pytest with coverage
```

## Testing

Tests are run with pytest and include coverage reporting:
```bash
python -m pytest -vv --cov=hello test_hello.py
```

## Linting

Code quality checks with pylint:
```bash
pylint --disable=R,C hello.py
```

## CI/CD

This project uses GitHub Actions for continuous integration. Every push to `main` or `develop` branches automatically runs:
- Dependency installation
- Code linting
- Unit tests with coverage

See `.github/workflows/python-app.yml` for configuration.

## License

MIT
