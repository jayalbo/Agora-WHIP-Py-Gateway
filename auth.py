from functools import wraps
from quart import request, abort
import base64
from config import CUSTOMER_ID, CUSTOMER_SECRET

def require_auth(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Basic "):
            abort(401, description="Authorization required")

        try:
            auth_decoded = base64.b64decode(auth.split(" ")[1]).decode("utf-8")
            username, password = auth_decoded.split(":", 1)
        except Exception:
            abort(401, description="Invalid Authorization header")

        if username != CUSTOMER_ID or password != CUSTOMER_SECRET:
            abort(401, description="Invalid credentials")

        return await f(*args, **kwargs)
    return decorated
