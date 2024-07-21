from sanic import Sanic
from sanic.response import json
from sanic.worker.manager import WorkerManager

from logzero import logger

from talker import talk

app = Sanic("SimpleService")

talker = talk()

WorkerManager.THRESHOLD = 100  # Value is in 0.1s


# Initialize a simple message
message = {"content": "Hello, World!"}


# Route to handle GET requests
@app.get("/message")
async def get_message(request):
    return json(message)


# Route to handle POST requests
@app.post("/message")
async def update_message(request):
    global message
    data = request.json
    logger.debug(request.json)
    logger.debug(type(request.json))
    if "text" in data:
        logger.debug(request.json)
        logger.debug(type(request.json))

        response = talker.parse(data["text"])

        return json({"response": response}, status=200)
    return json({"error": "Invalid request, key 'text' missing."}, status=400)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True, auto_reload=True)
