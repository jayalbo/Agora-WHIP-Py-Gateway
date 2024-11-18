
from .webrtc_handler import setup_peer_connection, finalize_sdp_exchange, cleanup_connection, handle_webrtc_connection
from datetime import datetime
from storage import peer_connections, stream_keys
from quart import jsonify, request, make_response

async def whip_handler():
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header is missing or invalid"}), 400

        stream_key = auth_header.split("Bearer ")[1]
        if stream_key not in stream_keys:
            return jsonify({"error": "Invalid stream key"}), 404

        stream_key_data = stream_keys[stream_key]
        expiration_date = datetime.strptime(stream_key_data["expiration_date"], "%Y-%m-%d %H:%M:%S")
        if stream_key_data["status"] != "active" or datetime.now() > expiration_date:
            return jsonify({"error": "Stream key is expired or inactive"}), 403

        if request.headers.get("Content-Type") != "application/sdp":
            return jsonify({"error": "Unsupported Content-Type. Expected application/sdp"}), 415


        # Debugging log
        raw_data = await request.get_data()
        if raw_data is None:
            print("No data received in the request body")
            return jsonify({"error": "No SDP offer provided"}), 400

        sdp_offer = raw_data.decode("utf-8")
        # print(f"Received SDP Offer: {sdp_offer}")  # Debugging output

        resource_id = stream_key

        sdp_answer = await handle_webrtc_connection(
            sdp_offer, resource_id, stream_key_data["cname"], stream_key_data["uid"]
        )

        response = await make_response(sdp_answer.sdp, 201)
        response.headers["Content-Type"] = "application/sdp"
        response.headers["Location"] = f"/whip/resource/{resource_id}"
        return response

    except Exception as e:
        print(f"Error in WHIP handler: {e}")
        return jsonify({"error": "An error occurred during WHIP processing"}), 500
