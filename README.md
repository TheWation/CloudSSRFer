# CloudSSRFer

[![made-with-python](http://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![built-with-love](http://forthebadge.com/images/badges/built-with-love.svg)](https://gitHub.com/TheWation/)

CloudSSRFer aims to develop a tool that detects SSRF (Server-Side Request Forgery) vulnerabilities in URLs and determines if the target host is hosted on AWS cloud services. The tool will further attempt to extract sensitive data from metadata internal endpoints and display the results in a formatted output.

## Features

### 1. SSRF Vulnerability Detection
The tool will analyze URLs provided by the user and check for SSRF vulnerability. SSRF vulnerabilities occur when an attacker can manipulate a server's request to access internal resources or services.

### 2. AWS Cloud Services Detection
The tool will identify if the target host is hosted on AWS cloud services. This detection can help in understanding the potential attack surface and the associated risks.

### 3. Sensitive Data Extraction
If the target host is hosted on AWS cloud services and an SSRF vulnerability is present, the tool will attempt to extract sensitive data from metadata internal endpoints. AWS metadata contains valuable information about the instance, such as access keys, security group configurations, and more.

### 4. Formatted Output
The tool will provide a formatted output that clearly presents the results. This output can include detailed information about the detected vulnerabilities, AWS services identification, and any extracted sensitive data.

## Note

This tool is designed to work exclusively with IMDSv1 (Instance Metadata Service version 1), ensuring compatibility and accurate extraction of sensitive data from metadata internal endpoints.

## Usage

### Prerequisites
Make sure you have Python 3 installed on your system. You can download Python from the official website: [Python.org](https://www.python.org/downloads/)

1. Clone the project repository:
```bash
git clone https://github.com/TheWation/CloudSSRFer
```

2. Navigate to the project directory:
```bash
cd CloudSSRFer
```

3. Install the required dependencies using pip: 

```bash
pip install -r requirements.txt
```

4. Run the CloudSSRFer script:

```bash
python CloudSSRFer.py https://vulnerable.com/?url=
```

## Disclaimer
For educational purposes only. Do not use for illegal activities. Use at your own risk. By using this tool, you agree to comply with all applicable laws and regulations. Unauthorized use is strictly prohibited. Always obtain permission before using this tool. No warranties.

## License

`CloudSSRFer` is made with ♥  by [Wation](https://github.com/TheWation) and it's released under the MIT license.