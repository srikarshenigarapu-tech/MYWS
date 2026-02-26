from fastapi import FastAPI, Request #Sample usecase
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/webhook")
async def dialogflow_webhook(request: Request):
    body = await request.json()

    tag = body.get("fulfillmentInfo", {}).get("tag", "")
    parameters = body.get("sessionInfo", {}).get("parameters", {})

    print("Received tag:", tag)
    print("Parameters:", parameters)

    # Tag routing
    if tag == "welcome_tag":
        response_text = "Hello! Welcome to the system."

    elif tag == "order_status":
        order_id = parameters.get("order_id", "unknown")
        response_text = f"Checking status for order {order_id}."

    elif tag == "user_info":
        name = parameters.get("name", "friend")
        response_text = f"Nice to meet you {name}!"

    else:
        response_text = "Sorry, I didn't understand the request."

    return JSONResponse({
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [response_text]
                    }
                }
            ]
        }
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)