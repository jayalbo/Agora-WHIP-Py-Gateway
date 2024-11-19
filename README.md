# Agora WHIP Python Server Gateway Gateway

**Agora WHIP Python Server Gateway** allows users to publish WebRTC streams to Agora’s streaming platform using the WHIP (WebRTC-HTTP Ingestion Protocol), enabling seamless integration for live video and audio workflows.

## Prerequisites

- Python 3.x installed
- (Optional) Virtual environment for dependency management

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jayalbo/Agora-WHIP-Py-Gateway
   cd Agora-WHIP-Py-Gateway
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate # On macOS/Linux
   venv\Scripts\activate # On Windows
   ```
3. Install the dependencies:
   ```bash
    pip install -r requirements.txt
   ```
4. Copy the `.env.example` file to `.env` and update the values:

   ```bash
   cp .env.example .env
   ```

   - .env values
     - APP_ID - Agora App ID
     - CERTIFICATE - Agora App Certificate (\*Optional)
     - CUSTOMER_ID - Agora Customer ID
     - CUSTOMER_SECRET - Agora Customer Secret

5. Run the application:
   ```bash
    python whip.py
   ```
6. Access the application:
   The server will run at http://127.0.0.1:5000.

# API Endpoints

## Authentication

All endpoints (except `/whip` and `/whip/resource/<stream_key>`) are protected by **Basic Authentication**.

Use your Agora **Customer ID** as the username and **Customer Secret** as the password.

---

## Endpoints

### **POST** `/streamKey`

Creates a new stream key.

- **Parameters**:
  - **cname** (string): Channel name (required)
  - **uid** (integer, optional): User ID
  - **duration** (integer, optional): Duration in minutes (defaults to 1 year)

---

### **GET** `/streamKeys`

Retrieves all created stream keys.

---

### **GET** `/streamKey/<stream_key>`

Retrieves a specific stream key.

---

### **DELETE** `/streamKey/<stream_key>`

Deletes a specified stream key.

---

### **POST** `/whip`

Endpoint for WebRTC WHIP logic.

---

### **DELETE** `/whip/resource/<stream_key>`

Endpoint for WebRTC / Agora WHIP termination logic.

---

# To do

- [x] ~~Add Agora token support~~
- [ ] Enable encoded video frames processing
- [ ] Enable video transcoding
