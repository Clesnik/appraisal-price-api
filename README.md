# Appraisal Price API

A FastAPI-based application that uses Playwright to automate web interactions, specifically designed for the Nadlan valuation website. The API can also execute commands on SSH droplets with variable substitution.

## Features

- **Playwright Automation**: Automate web browser interactions with the Nadlan valuation website
- **FastAPI Backend**: RESTful API endpoints for running scripts
- **SSH Integration**: Execute commands on remote SSH droplets
- **Variable Support**: Pass dynamic variables to scripts via POST requests
- **Screenshot Capture**: Automatic screenshot capture during web automation
- **Form Analysis**: Detailed analysis of web forms and page elements

## Installation

### Prerequisites

- Python 3.8+
- pip
- SSH client (for SSH functionality)

### Setup

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

4. **Run the FastAPI server**:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Root Endpoint
- **GET** `/`
- Returns basic API status

### 2. Run Nadlan Script
- **POST** `/run-nadlan-script`
- Specifically designed for the Nadlan valuation website

**Request Body**:
```json
{
  "url": "https://nadlanvaluation.spurams.com/login.aspx",
  "variables": {
    "wait_time": 3000,
    "screenshot_path": "nadlan_screenshot.png",
    "headless": true
  }
}
```

### 3. Run Generic Playwright Script
- **POST** `/run-playwright`
- Generic endpoint for any website

**Request Body**:
```json
{
  "url": "https://example.com",
  "variables": {
    "custom_wait": 2000,
    "take_screenshot": true
  },
  "script_name": "my_script"
}
```

### 4. Execute SSH Command
- **POST** `/run-ssh`
- Execute commands on SSH droplets

**Request Body**:
```json
{
  "host": "your-droplet-ip",
  "username": "your-username",
  "private_key_path": "/path/to/private/key",
  "command": "python3 /path/to/script.py",
  "variables": {
    "script_path": "/home/user/scripts/",
    "output_file": "result.json"
  }
}
```

## Usage Examples

### Using the Test Client

Run the included test client to see all endpoints in action:

```bash
python test_client.py
```

### Direct API Calls

#### Test the Nadlan website:
```bash
curl -X POST "http://localhost:8000/run-nadlan-script" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://nadlanvaluation.spurams.com/login.aspx",
    "variables": {
      "wait_time": 3000,
      "screenshot_path": "test_screenshot.png"
    }
  }'
```

#### Run a generic Playwright script:
```bash
curl -X POST "http://localhost:8000/run-playwright" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "variables": {
      "custom_wait": 2000
    },
    "script_name": "test_script"
  }'
```

### Standalone Script Usage

You can also run the Nadlan Playwright script directly:

```bash
python nadlan_playwright.py '{"wait_time": 3000, "screenshot_path": "direct_screenshot.png"}'
```

## File Structure

```
appraisal_price_api/
├── main.py                 # FastAPI application
├── nadlan_playwright.py    # Standalone Nadlan script
├── test_client.py         # Test client for API endpoints
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

### Environment Variables

You can set the following environment variables:

- `API_HOST`: Host for the FastAPI server (default: "0.0.0.0")
- `API_PORT`: Port for the FastAPI server (default: 8000)

### SSH Configuration

For SSH functionality, ensure you have:

1. SSH key pair set up
2. Proper permissions on private key file (600)
3. SSH access to your droplet

## Response Format

All API endpoints return JSON responses in the following format:

```json
{
  "status": "success",
  "message": "Operation completed successfully",
  "result": {
    // Detailed result data
  }
}
```

## Error Handling

The API includes comprehensive error handling:

- HTTP 500 for server errors
- Detailed error messages in response body
- Graceful handling of Playwright and SSH failures

## Security Considerations

- SSH private keys should have restricted permissions (600)
- Consider using environment variables for sensitive data
- Validate all input variables before processing
- Use HTTPS in production environments

## Troubleshooting

### Common Issues

1. **Playwright browser not found**:
   ```bash
   playwright install chromium
   ```

2. **SSH connection failed**:
   - Check SSH key permissions
   - Verify droplet IP and credentials
   - Ensure SSH service is running on droplet

3. **Permission denied errors**:
   - Check file permissions
   - Ensure proper user permissions

### Debug Mode

To run with debug output, modify the script to set `headless=False` in the variables.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
