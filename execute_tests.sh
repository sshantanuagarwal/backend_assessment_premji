#!/bin/bash

# Run the tests with coverage
coverage run --source=assessment_app -m pytest /app/assessment_app/tests/pub_tests/ --html=/app/output/pub-test-report.html --self-contained-html
#coverage run --source=assessment_app -m pytest /app/assessment_app/tests/private_tests/ --html=/app/output/private-test-report.html --self-contained-html

# Run additional tests to improve coverage
coverage run -a --source=assessment_app -m pytest /app/assessment_app/tests/pub_tests/test_portfolio_repository.py
coverage run -a --source=assessment_app -m pytest /app/assessment_app/tests/pub_tests/test_trade_repository.py

# Display the report in the terminal with branch coverage
coverage report --show-missing --include="*/assessment_app/*" --omit="*/__init__.py" -m

# Generate HTML report with branch coverage
coverage html --include="*/assessment_app/*" --omit="*/__init__.py" -d output/coverage_report --show-contexts