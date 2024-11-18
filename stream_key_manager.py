import uuid
from datetime import datetime
from storage import stream_keys

def create_stream_key_entry(cname, uid, expiration_date):
    stream_key = str(uuid.uuid4())
    stream_keys[stream_key] = {
        "cname": cname,
        "uid": uid,
        "expiration_date": expiration_date.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active"
    }
    return stream_key

def get_stream_keys():
    return [{"streamKey": key, **value} for key, value in stream_keys.items()]

def delete_stream_key_entry(stream_key):
    if stream_key in stream_keys:
        del stream_keys[stream_key]
        return True
    return False
