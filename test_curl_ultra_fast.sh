#!/bin/bash

echo "⚡ Testing Nadlan Appraisal API with ULTRA-FAST mode..."
echo "📡 Sending request to localhost:8000/run-appraisal"
echo "🚀 Maximum speed with minimal delays"
echo ""

curl -X POST http://localhost:8000/run-appraisal \
  -H "Content-Type: application/json" \
  -d '{
    "wait_time": 0,
    "headless": false,
    "username": "AaronK",
    "password": "berlinchildhood$",
    "transaction_type": "Purchase",
    "loan_type": "Other (please specify)",
    "loan_number": "",
    "borrower": "",
    "property_type": "Single Family Residential",
    "property_address": "15 Burr Avenue",
    "property_city": "Marlboro Township",
    "property_state": "New Jersey",
    "property_zip": "07751",
    "occupancy_type": "Investment",
    "contact_person": "",
    "other_access_instructions": "",
    "agent_name": "",
    "product": 59,
    "date_appraisal_needed": ""
  }' | jq '.'

echo ""
echo "✅ Ultra-fast test completed!"
