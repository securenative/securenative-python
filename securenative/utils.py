import base64
import json
import hmac
import hashlib


def _parse_cookie(cookie_value=None):
    fp = u''
    cid = u''

    if cookie_value is None:
        return cid, fp

    base64_decoded = base64.b64decode(cookie_value)
    if base64_decoded is None:
        base64_decoded = u'{}'

    json_obj = json.loads(base64_decoded)

    if hasattr(json_obj, 'fp'):
        fp = json_obj['fp']

    if hasattr(json_obj, 'cid'):
        cid = json_obj['cid']

    return cid, fp


def verify_signature(secret, text_body, header_signature):
    comparison_signature = hmac.new(secret, text_body, hashlib.sha3_512).hexdigest()
    return comparison_signature == header_signature
