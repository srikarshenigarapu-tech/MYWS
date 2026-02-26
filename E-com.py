from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock Data: In-memory dictionary representing our "database"
orders = {
    "ORD123": {"status": "Shipped", "item": "Wireless Headphones", "delivery_date": "2026-03-01"},
    "ORD456": {"status": "Delivered", "item": "Smart Watch", "delivery_date": "2026-02-20"},
    "ORD789": {"status": "Processing", "item": "Gaming Mouse", "delivery_date": "TBD"}
}

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the request from Dialogflow CX
    req = request.get_json(silent=True, force=True)
    
    # Extract the intent display name
    intent = req.get('intentInfo', {}).get('displayName')
    parameters = req.get('intentInfo', {}).get('parameters', {})
    
    # Logic for Order Tracking
    if intent == "track.order":
        order_id = parameters.get('order_id', {}).get('resolvedValue')
        if order_id in orders:
            details = orders[order_id]
            response_text = f"Your order for {details['item']} is currently {details['status']}. Estimated arrival: {details['delivery_date']}."
        else:
            response_text = "I couldn't find an order with that ID. Please double-check the number."

    # Logic for Returns
    elif intent == "process.return":
        order_id = parameters.get('order_id', {}).get('resolvedValue')
        if order_id in orders:
            if orders[order_id]['status'] == "Delivered":
                response_text = f"I've initiated a return for your {orders[order_id]['item']}. You will receive a shipping label via email shortly."
            else:
                response_text = "Return failed. Items can only be returned after they have been marked as 'Delivered'."
        else:
            response_text = "Invalid Order ID. I can't process a return for an order that doesn't exist."

    else:
        response_text = "I'm not sure how to help with that yet."

    # Return the response in Dialogflow CX format
    return jsonify({
        "fulfillment_response": {
            "messages": [{"text": {"text": [response_text]}}]
        }
    })

if __name__ == '__main__':
    # host='0.0.0.0' tells Flask to listen on all available IPs
    app.run(host='0.0.0.0', port=5000, debug=True)