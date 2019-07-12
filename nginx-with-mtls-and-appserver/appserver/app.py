import re
from flask import Flask, request

app = Flask(__name__)


def generate_whitelist():
    whitelist = []
    with open('/whitelist.txt', 'r') as f:
        for line in f.readlines():
            if line.strip().endswith('d.wott.local'):
                whitelist.append(line.strip())
    return whitelist


def grant_client_access(headers):
    """
    We need to check for:
     * 'Ssl-Client-Verify' = 'SUCCESS'
     * 'Ssl-Client' = 'CN=x.d.wott.local,O=Web of Trusted Things\\, Ltd,ST=London,C=UK')
    """

    if not headers.get('Ssl-Client-Verify') == 'SUCCESS':
        return False

    whitelist = generate_whitelist()
    print('Device whitelist: {}'.format(whitelist))

    # Extract the Common Name from the certificate
    matchObj = re.match(
        r'.*CN=(.*.d.wott.local)',
        headers.get('Ssl-Client'),
        re.M | re.I
    )

    print('Got request from {}'.format(matchObj.group(1)))

    # Match the device against the whitelist
    if matchObj.group(1) in whitelist:
        print('{} found in whitelist'.format(matchObj.group(1)))
        return True

    return False


@app.route('/')
def hello_world():
    if grant_client_access(request.headers):
        return 'Access granted!\n'
    else:
        return 'Access denied!\n'
