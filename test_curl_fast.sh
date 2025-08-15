#!/bin/bash

echo "🚀 Testing Nadlan Appraisal API with FAST mode and visible browser..."
echo "📡 Sending request to localhost:8000/run-appraisal"
echo "⚡ Reduced delays for faster execution"
echo ""

curl -X POST http://localhost:8000/run-appraisal \
  -H "Content-Type: application/json" \
  -d '{
    "wait_time": 500,
    "screenshot_path": "appraisal_fee_test.png",
    "headless": false,
    "username": "AaronK",
    "password": "berlinchildhood$",
    "transaction_type": "Purchase",
    "loan_type": "Other (please specify)",
    "loan_number": "123456",
    "borrower": "Example LLC",
    "property_type": "Single Family Residential",
    "property_address": "15 Burr Avenue",
    "property_city": "Marlboro Township",
    "property_state": "New Jersey",
    "property_zip": "07751",
    "occupancy_type": "Investment",
    "contact_person": "Agent",
    "other_access_instructions": "NA",
    "agent_name": "Chris Lesnik",
    "product": 59,
    "date_appraisal_needed": "2025-08-27"
  }' | jq '.'

echo ""
echo "✅ Fast request completed!"
