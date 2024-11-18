import os
import sys
import base64
from datetime import datetime, timedelta
import uuid
from quart import Quart, jsonify, request, abort, make_response
from dotenv import load_dotenv
from functools import wraps
from utils.whip_handler import whip_handler
from storage import stream_keys
from auth import require_auth
from config import APP_ID, CERTIFICATE, CUSTOMER_ID, CUSTOMER_SECRET
from stream_key_manager import create_stream_key_entry, get_stream_keys, delete_stream_key_entry

# Initialize Quart app
app = Quart(__name__)

# Validate required configuration variables
required_config = {
    "APP_ID": APP_ID,
    "CUSTOMER_ID": CUSTOMER_ID,
    "CUSTOMER_SECRET": CUSTOMER_SECRET
}

missing_config_vars = [key for key, value in required_config.items() if not value]

if missing_config_vars:
    print(f"Error: Missing required configuration variables: {', '.join(missing_config_vars)}")
    sys.exit(1)

@app.route('/streamKey', methods=['POST'])
@require_auth
async def create_stream_key():
    # Ensure APP_ID is available
    if not APP_ID:
        return jsonify({"error": "APP_ID must be set"}), 500

    # Get request data
    data = await request.get_json()
    cname = data.get("cname")
    uid = data.get("uid", 0)
    duration = data.get("duration", 31536000) # Default to 1 year in seconds if not provided

    # Validate input
    if not cname:
        return jsonify({"error": "cname is required"}), 400

    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Create stream key entry
    expiration_date = datetime.now() + timedelta(minutes=duration)
    stream_key = create_stream_key_entry(cname, uid, expiration_date)

    return jsonify({"message": "Stream key created", "streamKey": stream_key}), 201


@app.route('/streamKeys', methods=['GET'])
@require_auth
async def get_all_stream_keys():
    # Retrieve and return all stream keys
    stream_keys_list = get_stream_keys()
    return jsonify({"streamKeys": stream_keys_list}), 200

@app.route('/streamKey/<stream_key>', methods=['GET'])
@require_auth
async def get_stream_key(stream_key):
    # Retrieve and return a specific stream key
    if stream_key in stream_keys:
        return jsonify({"streamKey": stream_key, **stream_keys[stream_key]}), 200
    return jsonify({"error": "Stream key not found"}), 404

@app.route('/streamKey/<stream_key>', methods=['DELETE'])
@require_auth
async def delete_stream_key(stream_key):
    if delete_stream_key_entry(stream_key):
        return jsonify({"message": "Stream key deleted"}), 200
    return jsonify({"error": "Stream key not found"}), 404


@app.route('/whip', methods=['POST'])
async def whip():
    return await whip_handler()

if __name__ == '__main__':
    app.run(debug=True)
