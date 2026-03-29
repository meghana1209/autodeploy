# ADR-001: CI/CD Pipeline Design for Lambda Deployments

## Status
Accepted

## Context
Manual deployments to AWS Lambda were error-prone and inconsistent. There was no automated testing before deployment, no rollback mechanism on failure, and no visibility into system health post-deploy. Every release required manual steps which slowed iteration and introduced risk.

## Decision
Implement a fully automated CI/CD pipeline using:
- **GitHub Actions** — trigger on every push to main; run tests before any deployment
- **pytest** — automated test suite must pass before deployment proceeds
- **AWS Lambda** — target deployment environment
- **AWS CloudWatch** — post-deploy health check, alarms, and dashboard
- **IAM least-privilege roles** — scoped per pipeline stage

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| Manual deploy via AWS Console | Simple | Error-prone, no audit trail, slow |
| AWS CodePipeline only | Native AWS | More setup, no free tier CI |
| GitHub Actions (chosen) | Free, fast, integrates with repo | Requires AWS secrets in GitHub |

## Consequences

**Positive:**
- Every push to main is automatically tested and deployed
- Failed tests block deployment — production is always stable
- CloudWatch alarms notify on errors within 60 seconds
- IAM roles enforce least-privilege access per stage
- Full audit trail via GitHub Actions logs

**Trade-offs:**
- AWS credentials must be stored as GitHub Secrets
- Cold start adds ~200ms on first invocation after idle
- Pipeline adds ~2 min to release cycle (worth the safety guarantee)

## Pipeline Stages

```
Push to main
    → Checkout code
    → Install dependencies
    → Run pytest (FAIL = stop here)
    → Package Lambda (zip)
    → Deploy to AWS Lambda
    → Health check invocation
    → FAIL = rollback, PASS = done
```

## References
- [GitHub Actions AWS Deploy](https://github.com/aws-actions/configure-aws-credentials)
- [AWS Lambda Deployment Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
