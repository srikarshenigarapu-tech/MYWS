from flask import Flask, request, jsonify
import logging

# --- Setup ---
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# --- Handler Functions for Each Tag ---
# Each function is responsible for a single troubleshooting task.
# This makes the logic for each tag isolated and easy to test/modify.

def handle_password_reset():
    """Provides steps for resetting a password."""
    logging.info("Handling 'reset_password' tag.")
    return "To reset your password, press Ctrl+Alt+Delete and select 'Change a password'."

def handle_vpn_issue():
    """Provides steps for VPN issues."""
    logging.info("Handling 'vpn_issue' tag.")
    return "Please verify internet connectivity, reconnect your VPN client, and retry."

def handle_outlook_issue():
    """Provides steps for Outlook issues."""
    logging.info("Handling 'outlook_issue' tag.")
    return "Restart Outlook, run Office Quick Repair, and check your mailbox quota."

def handle_slow_laptop():
    """Provides steps for a slow laptop."""
    logging.info("Handling 'laptop_slow' tag.")
    return "Restart the laptop, close unused apps, and ensure at least 15% disk space is free."

def handle_wifi_issue():
    """Provides steps for Wi-Fi issues."""
    logging.info("Handling 'wifi_not_working' tag.")
    return "Turn Wi-Fi off/on, forget and reconnect to the network, then restart the router if needed."

# --- Tag to Function Mapping ---
# This dictionary maps the tag from Dialogflow to the corresponding handler function.
TAG_HANDLERS = {
    "reset_password": handle_password_reset,
    "vpn_issue": handle_vpn_issue,
    "outlook_issue": handle_outlook_issue,
    "laptop_slow": handle_slow_laptop,
    "wifi_not_working": handle_wifi_issue,
}

@app.route("/webhook", methods=["POST"])
def webhook():
    """
    Main webhook endpoint. It finds the correct handler function based on the
    Dialogflow tag and executes it to get the response.
    """
    payload = request.get_json(silent=True) or {}
    logging.info(f"Received request payload: {payload}")

    tag = payload.get("fulfillmentInfo", {}).get("tag")

    # Find the handler function in our map.
    handler = TAG_HANDLERS.get(tag)

    if handler:
        # If a handler is found, call it to get the response message.
        message = handler()
    else:
        # If no handler is found for the tag, create a default message.
        logging.warning(f"No handler found for tag: '{tag}'")
        message = f"I received your request, but no response is configured for tag: '{tag}'."

    # Format the response for Dialogflow CX
    return jsonify({
        "fulfillment_response": {
            "messages": [{"text": {"text": [message]}}]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
