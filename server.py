import uuid

from sanic import Sanic
from sanic.response import json
from sanic.worker.manager import WorkerManager

from logzero import logger

from talker import talk

app = Sanic("SimpleService")

talker = talk()

WorkerManager.THRESHOLD = 100  # Value is in 0.1s


# Route to handle GET requests
@app.get("/message")
async def get_heartbeat(request):
    return json({"hartbeat": "1"})


# Route to handle POST requests
@app.post("/message")
async def parse_message(request):
    data = request.json
    if "conversation_id" not in data:
        return json(
            {"error": "Invalid request, key 'conversation_id' missing."}, status=400
        )
    elif "text" not in data:
        return json({"error": "Invalid request, key 'text' missing."}, status=400)
    else:
        talker_response = await talker.parse(data["text"])
        response_data = {
            "response": talker_response,
            "conversation_id": data["conversation_id"],
        }
        return json(response_data, status=200)


@app.post("/login")
async def login_new_user(request):
    data = request.json
    if "initial_data" in data:
        # response = await talker.parse(data["text"])

        return json({"conversation_id": str(uuid.uuid4())}, status=200)
    return json({"error": "Invalid request, key 'initial_data' missing."}, status=400)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, auto_reload=True)
