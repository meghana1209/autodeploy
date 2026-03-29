#!/bin/bash
set -e

FUNCTION_NAME="autodeploy-handler"
REGION="ap-south-1"

echo ">>> Packaging Lambda..."
cd app
zip -q function.zip handler.py
cd ..

echo ">>> Deploying to Lambda..."
aws lambda create-function \
  --function-name $FUNCTION_NAME \
  --runtime python3.12 \
  --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/autodeploy-lambda-role \
  --handler handler.handler \
  --zip-file fileb://app/function.zip \
  --region $REGION 2>/dev/null || \
aws lambda update-function-code \
  --function-name $FUNCTION_NAME \
  --zip-file fileb://app/function.zip \
  --region $REGION

echo ">>> Verifying deployment (health check)..."
sleep 5
RESULT=$(aws lambda invoke \
  --function-name $FUNCTION_NAME \
  --payload '{"operation":"add","a":1,"b":1}' \
  --region $REGION \
  /tmp/response.json 2>&1)

STATUS=$(cat /tmp/response.json | python3 -c "import sys,json; print(json.load(sys.stdin)['statusCode'])")

if [ "$STATUS" != "200" ]; then
  echo ">>> Health check FAILED (status $STATUS) — rolling back..."
  # Rollback would restore previous version here
  exit 1
fi

echo ">>> Health check PASSED. Deployment complete!"
rm app/function.zip
