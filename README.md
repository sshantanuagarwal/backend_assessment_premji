# Stock Market Simulator

## Problem Statement
You are required to create a Stock Market Simulator. You are given 4 stocks with price for last 1 year.
It will allow users to place trade, track prices, and calculate the returns for each portfolio.

## Important Instructions
- Try to implement as many features as possible, as scoring will be proportional to the features implemented.
- You need to implement the all (try as much as you can) methods according to the instructions in description.
- Add all your assumptions/comments, etc in ASSUMPTIONS.md file.
- Some part of code is deliberately broken or left incomplete to test. Feel free to change it.
- Try not to modify the method signatures (input, output, api path, method names, etc.), unless needed. Make sure to give runnable instructions for testing.
- You are expected to finish all the methods as per the descriptions and add appropriate service, databases and other necessary classes/methods.
- You are expected to write test cases for all methods implemented. Coverage report can be generated for all methods to help identify the coverage of methods.
- Test cases must be written in folder `assessment_app/tests/pub_tests/`. A sample test has been provided to get started.
- You can add postman test collection file for api testing of your application backend.
- We will run eval.sh file with our private tests to run and evaluate your submission and score.
- Make sure your assessment is working (on any new system as well, not just your laptop) before submitting.
- You are expected to create unit tests for each method.
- You can create more classes as per the requirement of your implementation.
- Your code should be properly commented and readable and adhering to `PEP-8 guidelines`.
- You should follow the best practices of software development and testing.
- The code should be properly structured and should be modular.
- Edit `Dockerfile`s to install any dependencies and databases you may need.
- You are given `postgres`, however you can use any `relational` database of your choice.
- You are given sample `csv files` which you can use to import the data into your `database`.
- Please note, at any given time, trade can only happen with `trade.execution_ts` of trade to be same or later than `portfolio.current_ts`, i.e., you cannot execute trade in past.

## Scoring params
- Code working as stated in the instructions
- Time taken to complete the task (from the time assessment is received vs it is submitted)
- Code Quality
- Dockerization
- Scalability of the service
- Resiliency of the service
- Unit Tests
- API Documentation
- Concurrency/Race conditions/edge cases handling
- Any additional features

## Run/Debug/Develop Locally
```bash
chmod +x *.sh
./local_run.sh
```

## Evaluate Test cases
```bash
chmod +x *.sh
./eval.sh
```

## Run Driver Script
```bash
python driver.py
```
