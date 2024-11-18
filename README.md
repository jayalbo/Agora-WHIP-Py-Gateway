# Agora WHIP Python Server Gateway Relay

## Prerequisites

- Python 3.x installed
- (Optional) Virtual environment for dependency management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```
2. Create and activate a virtual environment (recommended):
   python3 -m venv venv
   source venv/bin/activate # On macOS/Linux
   venv\Scripts\activate # On Windows

3. Install the dependencies:
   ```bash
    pip install -r requirements.txt
   ```
4. Copy the `.env.example` file to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```
5. Run the application:
   ```bash
    python whip.py
   ```
6. Access the application:
   The server will run at http://127.0.0.1:5000.

## API Endpoints

Authentication
All endpoints are protected by Basic Authentication. Use your Agora Customer ID and Customer Secret as the username and password, respectively.

Endpoints

    •	POST /streamKey: Creates a new stream key.
       - Parameters: cname (string), uid (optional integer), duration (optional, in minutes; defaults to 1 year)
       - Response: JSON with streamKey, expiration_date, and optional token if CERTIFICATE is provided.
    •	GET /streamKeys: Retrieves all stream keys.
    •	Response: JSON array of all created stream keys.
    •	DELETE /streamKey/<stream_key>: Deletes a specified stream key.
    •	Response: Success message or error if not found.
    •	POST /whip: Placeholder for WebRTC WHIP logic.
    •	Response: JSON message indicating the placeholder.
