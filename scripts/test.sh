#!/bin/bash

BASE_URL="http://127.0.0.1:8000"

echo "Starting API Tests..."

# 1. Check server health
echo "Testing Home Endpoint..."
response=$(curl -s $BASE_URL/)
if [[ $response == *"Job Portal API running"* ]]; then
  echo "✅ Home endpoint working"
else
  echo "❌ Home endpoint failed"
  exit 1
fi

# 2. Register User
echo "Testing User Registration..."
register_response=$(curl -s -X POST $BASE_URL/register \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"123456"}')

echo $register_response

# 3. Login User
echo "Testing Login..."
login_response=$(curl -s -X POST $BASE_URL/login \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"123456"}')

echo $login_response

# Extract token (adjust based on your API response)
TOKEN=$(echo $login_response | jq -r '.access_token')

if [[ "$TOKEN" == "null" ]]; then
  echo "❌ Login failed"
  exit 1
else
  echo "✅ Login successful"
fi

# 4. Create Job
echo "Testing Job Creation..."
job_response=$(curl -s -X POST $BASE_URL/jobs \
-H "Authorization: Bearer $TOKEN" \
-H "Content-Type: application/json" \
-d '{"title":"DevOps Engineer","description":"CI/CD pipeline job"}')

echo $job_response

# 5. Get Jobs
echo "Testing Get Jobs..."
jobs=$(curl -s $BASE_URL/jobs)

if [[ $jobs == *"DevOps Engineer"* ]]; then
  echo "✅ Job fetch successful"
else
  echo "❌ Job fetch failed"
  exit 1
fi

echo "🎉 All tests passed!"