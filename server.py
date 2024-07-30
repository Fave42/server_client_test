import uuid

from sanic import Sanic
from sanic.response import json
from sanic.worker.manager import WorkerManager

from logzero import logger

from talker import talk

from backend_connector import save_data, is_conv_id_unique

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
        await save_data("user", data["text"], data["conversation_id"])

        await save_data("bot", talker_response, data["conversation_id"])

        return json(response_data, status=200)


@app.post("/login")
async def login_new_user(request):
    data = request.json
    if "initial_data" not in data:
        return json(
            {"error": "Invalid request, key 'initial_data' missing."}, status=400
        )

    while True:
        conv_id = str(uuid.uuid4())
        if await is_conv_id_unique(conv_id):
            break

    await save_data("user", "login", conv_id)
    return json({"conversation_id": conv_id}, status=200)


@app.post("/logout")
async def logout_user(request):
    data = request.json
    if "conversation_id" not in data:
        return json(
            {"error": "Invalid request, key 'conversation_id' missing."}, status=400
        )
    return json(
        {"success": f"User {data['conversation_id']} was logged out!"}, status=200
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, auto_reload=True)
