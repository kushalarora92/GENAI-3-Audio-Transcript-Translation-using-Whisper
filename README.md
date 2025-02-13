Architecture Design

Audio File MP3 -> Whisper -> Transcript / Text -> GPT 3 / Translate with language -> Response / translated text


# Steps
Steps to setup the project:

1. Create a new virtual environment
```
conda create -n openai python=3.10 -y
```
2. Activate the virtual environment
```
conda activate openai
```
3. Create requirements.txt file

4. Install the required packages
```
pip install -r requirements.txt
```

5. Create a new .env file and add the required variables

6. Run the project



# OPTIONAL - SKIP

HOW TO: freeze requirements
Initial requirements.txt file -- requirements-initial.txt
Frozen requirements.txt file -- requirements-frozen.txt
```
pip freeze > requirements-frozen.txt
```


HOW TO: check version of any package
```
pip freeze | grep <package_name>
```

# AWS Lambda DEPLOYMENT

1. Create a deployment directory
```
mkdir -p deployment/package
```

2. Install dependencies to a package directory
```
pip install -r requirements.txt --target deployment/package
```
<!-- pip freeze > deployment/requirements.txt -->

<!-- NOT NEEDED FOR PRODUCTION -->
<!-- 3. Create and activate virtual environment -->
<!-- python -m venv venv -->
<!-- source venv/bin/activate -->

3. Copy application files
```
cp app.py deployment/package/
cp -r templates deployment/package/
cp -r static deployment/package/
```

4. Create deployment ZIP
```
cd deployment/package
zip -r ../deployment.zip .
```

5. Create AWS Lambda Function
Function Configuration:
  Runtime: Python 3.9
  Handler: app.handler
  Memory: 256 MB (minimum)
  Timeout: 30 seconds
  Environment variables:
    - OPENAI_API_KEY: your_api_key

Execution role permissions:
  - Basic Lambda execution role
  - CloudWatch Logs access

Upload the deployment.zip file

TEST the lambda function with the following test event:
```
{
  "httpMethod": "GET",
  "path": "/",
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.5",
    "host": "your-api-gateway-id.execute-api.region.amazonaws.com",
    "user-agent": "Mozilla/5.0"
  },
  "queryStringParameters": null,
  "requestContext": {
    "identity": {
      "sourceIp": "127.0.0.1"
    }
  },
  "body": null,
  "isBase64Encoded": false
}
```

6. Create API Gateway Console
  - Select your API
  - Go to Resources
  - Create a new resource:
    - Resource Name: proxy
    - Resource Path: {proxy+}  (important: include the plus sign)
    - Enable CORS: ✓
  - Create ANY method under {proxy+}:
    - Integration type: Lambda Function
    - Lambda Function: your-function-name
    - Use Lambda Proxy integration: ✓
   
  - Create root path method:
    - Select the root (/)
    - Create ANY method
    - Same settings as above
  - Deploy the API
    - Click Actions → Deploy API
    - Select deployment stage (or create new)
    - Click Deploy
  - CORS Configuration
    - Select the resource
    - Click Enable CORS
    - Add headers:
      - Access-Control-Allow-Headers: 'Content-Type,X-Amz-Date,Authorization,X-Api-Key'
      - Access-Control-Allow-Methods: '*'
      - Access-Control-Allow-Origin: '*'
     - Click "Enable CORS and replace existing CORS headers"

  - Test the API from the API Gateway Console

7. Create a new ACM Certificate in AWS Certificate Manager
  - In AWS Certificate Manager Console
  - Click "Request a public certificate"
  - Fill in:
    - Domain name: complete prefix.domain.com
    - Validation method: DNS validation - recommended
    - Click "Request certificate"
    - Create CNAME record in Route 53 with an available button

8. Create a Custom Domain Name in API Gateway
  - In API Gateway Console
  - Go to "Custom domain names"
  - Click "Create"
  - Fill in:
    - Domain name: prefix.domain.com [[[THIS NAME NEEDS TO MATCH CNAME RECORD IN ROUTE 53 - ** IN THE NEXT STEP]]]
    - Minimum TLS version: TLS 1.2
    - ACM Certificate: Select the existing certificate (or create new)
  - Click "Create domain name"
  - Add API mapping:
    - API: your audio translation API
    - Stage: <enter stage name>
    - Path: <optional path>

9. Update Route 53 configuration with the new domain name
  - Go to Route53 Console
  - Select your hosted zone
  - Create new record:
    - Routing policy: Simple routing
    - Record name: prefix.domain.com [[[THIS NAME MATCHES ** IN THE PREVIOUS STEP]]]
    - Record type: A
    - Route traffic to: Alias to API Gateway API
    - Choose region
    - Choose the API Gateway domain name created in the previous step
    

10. TADA 🎉 Test the API from the new domain name 
