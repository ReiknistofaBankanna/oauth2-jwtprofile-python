import sys
import urllib.request
import urllib.parse
import json
import jwt
import uuid
import datetime
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import serialization, hashes

def load_cert(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    cert = cryptography.x509.load_pem_x509_certificate(pemlines, default_backend())
    return cert

def load_key(filename, password):
    passString = password
    passw = passString.encode('utf-8')
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, passw, default_backend())    
    return private_key


if (len(sys.argv) != 7):
    print('Usage... url certificatePath certificatePassword clientId resource audience')
    sys.exit(2)

url = sys.argv[1]
pem_path = sys.argv[2]
password = sys.argv[3]
client_id = sys.argv[4]
resource = sys.argv[5]
audience = sys.argv[6]

nbf = datetime.datetime.utcnow()
exp = datetime.datetime.utcnow() + datetime.timedelta(0,0,5) 

jti = str(uuid.uuid4())

payload =  {
                "aud": audience,
                "iss": client_id,
                "sub": client_id, 
                "nbf": nbf,
                "exp": exp,
                "jti": jti
           }

pk1 = load_key(pem_path, password)

cert = load_cert(pem_path)
thumbprint = cert.fingerprint(hashes.SHA1())
t = str(''.join('{:02x}'.format(x) for x in thumbprint)).upper()

encoded_token = jwt.encode(payload, pk1, algorithm='RS256', headers={'kid': t})
token = encoded_token.decode("utf-8")

postdata = { 'client_id': client_id, 'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer', 'grant_type' : 'client_credentials', 'resource': resource, 'client_assertion': token }
data = bytes( urllib.parse.urlencode( postdata ).encode() )
f = urllib.request.urlopen(url, data)
response = f.read().decode('utf-8')
print(response)