import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../app"))
from handler import handler

def test_add():
    response = handler({"operation": "add", "a": 5, "b": 3}, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["result"] == 8

def test_subtract():
    response = handler({"operation": "subtract", "a": 10, "b": 4}, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["result"] == 6

def test_multiply():
    response = handler({"operation": "multiply", "a": 6, "b": 7}, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["result"] == 42

def test_divide():
    response = handler({"operation": "divide", "a": 20, "b": 4}, None)
    assert response["statusCode"] == 200
    assert json.loads(response["body"])["result"] == 5.0

def test_divide_by_zero():
    response = handler({"operation": "divide", "a": 10, "b": 0}, None)
    assert response["statusCode"] == 400

def test_unknown_operation():
    response = handler({"operation": "power", "a": 2, "b": 3}, None)
    assert response["statusCode"] == 400

def test_missing_fields():
    response = handler({"operation": "add", "a": 5}, None)
    assert response["statusCode"] == 400

def test_missing_operation():
    response = handler({"a": 5, "b": 3}, None)
    assert response["statusCode"] == 400
