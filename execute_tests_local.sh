#!/bin/bash
rm -rf output/*
source .venv/bin/activate
pip install -r requirements.txt

# Set environment variables for testing
export TESTING=true
export SECRET_KEY=test-secret-key
export SKIP_AUTH=true

# Run the tests
pytest assessment_app/tests/ -v --html=output/test-report.html --self-contained-html

# Run the coverage analysis
coverage run --source=assessment_app -m pytest

# Display the report in the terminal
coverage report --show-missing --include="*/assessment_app/*" --omit="*/__init__.py"

# Generate HTML report in the specified directory
coverage html --include="*/assessment_app/*" --omit="*/__init__.py" -d output/coverage_report