from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    tag = req.get('fulfillmentInfo', {}).get('tag')
    
    # Logic for a specific tag
    if tag == 'greet_user':
        response = "Hello from your VS Code Webhook!"
    else:
        response = "API received the request, but tag was not recognized."

    return jsonify({
        "fulfillment_response": {
            "messages": [{"text": {"text": [response]}}]
        }
    })

if __name__ == '__main__':
    app.run(port=5000)