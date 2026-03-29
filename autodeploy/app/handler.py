import json

def handler(event, context):
    """
    Simple calculator API — demonstrates CI/CD deployment.
    Supports: add, subtract, multiply, divide
    """
    try:
        operation = event.get("operation")
        a = event.get("a")
        b = event.get("b")

        if a is None or b is None or not operation:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "operation, a, and b are required"})
            }

        if operation == "add":
            result = a + b
        elif operation == "subtract":
            result = a - b
        elif operation == "multiply":
            result = a * b
        elif operation == "divide":
            if b == 0:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Cannot divide by zero"})
                }
            result = a / b
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": f"Unknown operation: {operation}"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"operation": operation, "a": a, "b": b, "result": result})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
