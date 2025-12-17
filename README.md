# AWS Lambda Playground

A Python-based playground for learning and experimenting with AWS Lambda functions. This repository demonstrates key Lambda features including HTTP API handlers, event-driven processing, and AWS service integrations.

## Features

- **API Gateway Integration** - HTTP request/response handling with path parameters, query strings, and JSON body parsing
- **S3 Event Processing** - Event-driven Lambda handler for S3 PUT events
- **DynamoDB Integration** - Lambda functions with DynamoDB read/write operations
- **Local Testing** - Test Lambda functions locally with mock events
- **Environment Management** - Secure credential handling with `.env` files
- **Python Environment** - Configured with pyenv and venv for consistent development

## Prerequisites

- Python 3.13 (managed via pyenv)
- [just](https://github.com/casey/just) - Command runner (install via `brew install just` or `cargo install just`)
- AWS Account (for deployment)
- AWS CLI configured (for local testing with real AWS services)

## Setup

### 1. Python Environment Setup

This project uses `pyenv` for Python version management and `venv` for virtual environments.

```bash
# Install Python 3.13 via pyenv (if not already installed)
pyenv install 3.13

# The .python-version file will automatically use Python 3.13
# Create and activate virtual environment
just setup
```

The virtual environment (`.venv`) will be automatically detected by VSCode when you open the project.

### 2. Environment Variables

Copy the example environment file and configure your AWS credentials:

```bash
just setup-env
# Then edit .env and add your AWS credentials
```

The `.env` file contains:
- `AWS_ACCESS_KEY_ID` - Your AWS access key (for local testing)
- `AWS_SECRET_ACCESS_KEY` - Your AWS secret key (for local testing)
- `AWS_REGION` - AWS region (default: us-east-1)
- `DYNAMODB_TABLE_NAME` - DynamoDB table name
- `S3_BUCKET_NAME` - S3 bucket name (optional)

**Note:** In AWS Lambda, credentials come from IAM roles. The `.env` file is only for local development.

### 3. Install Dependencies

```bash
just install
```

## Lambda Functions

### 1. API Handler (`lambda_functions/api_handler.py`)

HTTP API Gateway Lambda handler that demonstrates:
- HTTP method handling (GET, POST)
- Path parameter extraction
- Query string parsing
- JSON body parsing
- Proper API Gateway response formatting

**Test locally:**
```bash
just invoke-api        # GET request
just invoke-api-post   # POST request
```

### 2. S3 Event Handler (`lambda_functions/s3_event_handler.py`)

Event-driven Lambda handler for S3 events that demonstrates:
- S3 event notification processing
- Event record parsing
- Object metadata retrieval
- Error handling for event processing

**Test locally:**
```bash
just invoke-s3
```

### 3. DynamoDB Handler (`lambda_functions/dynamodb_handler.py`)

DynamoDB integration Lambda handler that demonstrates:
- DynamoDB read operations (GET)
- DynamoDB write operations (PUT)
- DynamoDB delete operations (DELETE)
- DynamoDB scan operations (LIST)
- Environment variable configuration
- AWS SDK (boto3) usage

**Test locally:**
```bash
just invoke-dynamodb-get   # Retrieve item
just invoke-dynamodb-put   # Create/update item
just invoke-dynamodb-list  # List all items
```

## Testing

Run all Lambda functions with sample events:

```bash
just test-all
```

## AWS Infrastructure Requirements

To deploy these Lambda functions to AWS, you'll need the following resources:

### Required AWS Resources

1. **Lambda Functions** (3 total)
   - `api-handler` - HTTP API handler
   - `s3-event-handler` - S3 event processor
   - `dynamodb-handler` - DynamoDB integration handler

2. **API Gateway**
   - HTTP API or REST API
   - Configured to trigger `api-handler` Lambda function

3. **S3 Bucket**
   - Bucket for storing objects
   - Event notification configured to trigger `s3-event-handler` Lambda on PUT events

4. **DynamoDB Table**
   - Table for `dynamodb-handler` to read/write data
   - Table name configured via `DYNAMODB_TABLE_NAME` environment variable

5. **IAM Roles** (3 Lambda execution roles, one per function)
   - `api-handler-role`:
     - CloudWatch Logs permissions (`logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`)
   - `s3-event-handler-role`:
     - CloudWatch Logs permissions
     - S3 read permissions (`s3:GetObject`) for the bucket
   - `dynamodb-handler-role`:
     - CloudWatch Logs permissions
     - DynamoDB read/write permissions (`dynamodb:GetItem`, `dynamodb:PutItem`, `dynamodb:UpdateItem`, `dynamodb:DeleteItem`) for the table

### Optional Resources

- **CloudWatch Log Groups** - Created automatically when Lambda functions are invoked

## Credential Management

### Local Development

- Credentials are loaded from `.env` file using `python-dotenv`
- The `.env` file is git-ignored and should never be committed
- Use `.env.example` as a template

### AWS Deployment

- **Preferred:** Use IAM roles for Lambda execution (no credentials needed in code)
- **Alternative:** Use environment variables in Lambda configuration (less secure)

## Project Structure

```
lambda-playground/
├── lambda_functions/
│   ├── api_handler.py          # API Gateway handler
│   ├── s3_event_handler.py     # S3 event handler
│   └── dynamodb_handler.py      # DynamoDB handler
├── .venv/                      # Python virtual environment (git-ignored)
├── .vscode/
│   └── settings.json            # VSCode Python interpreter config
├── .python-version              # pyenv Python version
├── .env.example                 # Environment variables template
├── .env                         # Your credentials (git-ignored)
├── requirements.txt             # Python dependencies
├── justfile                     # Command runner recipes
└── README.md                    # This file
```

## Available Commands

- `just setup` - Create virtual environment and install dependencies
- `just install` - Install Python dependencies
- `just setup-env` - Copy `.env.example` to `.env` (if it doesn't exist)
- `just invoke-api` - Test API handler with GET request
- `just invoke-api-post` - Test API handler with POST request
- `just invoke-s3` - Test S3 event handler
- `just invoke-dynamodb-get` - Test DynamoDB GET operation
- `just invoke-dynamodb-put` - Test DynamoDB PUT operation
- `just invoke-dynamodb-list` - Test DynamoDB LIST operation
- `just test-all` - Run all Lambda functions with sample events

## VSCode Integration

The project is configured to automatically use the `.venv` Python interpreter when opened in VSCode. The configuration is in `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true
}
```

When you open the project in VSCode, it will:
- Automatically detect the `.venv` Python interpreter
- Activate the virtual environment in integrated terminals

## License

MIT License - see [LICENSE](LICENSE) file for details.
