import hmac
import hashlib

def create_signature(secret_key, msg, digestmod=None):
	if digestmod is None:
		digestmod = hashlib.sha1
	mac = hmac.new(secret_key, msg=msg, digestmod=digestmod)
	return mac.digest()

