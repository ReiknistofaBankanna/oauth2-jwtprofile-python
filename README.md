oauth2-jwtprofile-python
==================================

This sample calls a oAuth2 Authorization Server to get a JWT token using the JWT Profile flow (https://tools.ietf.org/html/rfc7523).

## How To Run This Sample

### To run this sample you will need:
- Python 3

### Python packages:
- request
- jwt
- json

### Usage:
Usage... adfsUrl certificatePath certificatePassword clientId resource

Example:
```
python oauth2_jwtprofile.py https://adfs.test.rb.is/adfs/oauth2/token c:\\cert\\myprivatekey.pem myprivatekeypass 1add817a-4641-4ab0-a881-679f34421af4 urn:rb.api
```
