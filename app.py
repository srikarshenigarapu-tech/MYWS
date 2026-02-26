from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Mock "Database" ---
MOCK_DATA = {
    "12345": {"name": "Alex", "bill": "$75.00", "due": "$0.00", "data": "15GB"},
    "67890": {"name": "Jordan", "bill": "$110.00", "due": "$45.00", "data": "2GB"}
}

# --- Tag Handler Functions ---
def handle_billing(user):
    return f"Hi {user['name']}, your latest bill is {user['bill']}. Pending: {user['due']}."

def handle_usage(user):
    return f"Status for {user['name']}: You have {user['data']} of data remaining."

def handle_plans(user):
    return "You are currently on the 'Unlimited Gold' plan. No upgrades available."

# --- Tag Mapping ---
# This maps the "tag" from Dialogflow to the Python function
TAG_MAP = {
    "check_billing": handle_billing,
    "check_usage": handle_usage,
    "check_plan": handle_plans
}

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True)
    
    # Extract Tag and Parameters from Dialogflow fulfillment request
    # Note: 'tag' is usually found in Dialogflow CX, or as a parameter in ES
    tag = req.get('fulfillmentInfo', {}).get('tag') 
    params = req.get('intentInfo', {}).get('parameters', {})
    
    # Fallback for Dialogflow ES structure if CX isn't used
    if not tag:
        tag = req.get('queryResult', {}).get('intent', {}).get('displayName')
        params = req.get('queryResult', {}).get('parameters', {})

    customer_id = params.get('customer_id')
    user = MOCK_DATA.get(str(customer_id))

    if not user:
        response_text = "Access denied. I couldn't find that Customer ID in our records."
    elif tag in TAG_MAP:
        # Dynamically call the function based on the tag
        response_text = TAG_MAP[tag](user)
    else:
        response_text = f"Tag '{tag}' received, but no handler is defined in the webhook."

    return jsonify({"fulfillmentText": response_text})

if __name__ == '__main__':
    app.run(port=5000, debug=True)