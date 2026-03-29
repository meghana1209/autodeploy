# AutoDeploy — CI/CD Pipeline on AWS

## Overview
AutoDeploy is an end-to-end CI/CD pipeline that automatically tests and deploys a Python Lambda function to AWS on every push to main. It includes automated rollback on failed health checks and CloudWatch monitoring.

## Architecture
```
GitHub Push
    ↓
GitHub Actions (CI)
    ↓ Run pytest
    ↓ PASS → Package + Deploy to Lambda
    ↓ FAIL → Block deploy, notify
    ↓
AWS Lambda (Production)
    ↓
CloudWatch (Monitor + Alert)
```

## Tech Stack
| Layer      | Technology                        |
|------------|-----------------------------------|
| CI/CD      | GitHub Actions + AWS CodePipeline |
| Compute    | AWS Lambda (Python 3.12)          |
| Monitoring | AWS CloudWatch Alarms + Dashboard |
| Security   | AWS IAM least-privilege roles     |
| Testing    | pytest                            |

## Key Design Decisions
- See [ADR-001](architecture/decisions/ADR-001-cicd-design.md)

## How to Set Up
```bash
# 1. Clone the repo
git clone https://github.com/meghana1209/autodeploy

# 2. Add GitHub Secrets:
#    AWS_ACCESS_KEY_ID
#    AWS_SECRET_ACCESS_KEY
#    AWS_ACCOUNT_ID

# 3. Push to main — pipeline runs automatically
git push origin main
```

## Running Tests Locally
```bash
pip install pytest
pytest tests/ -v
```

## Monitoring
CloudWatch dashboard tracks:
- Lambda invocation count
- Error rate
- Duration (p50, p99)
- Throttles
