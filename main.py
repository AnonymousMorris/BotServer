import asyncio
import threading
from queue import Queue
from flask import Flask, request
import uuid
from multiprocessing import Process

app = Flask(__name__)
import Openai_calls

result = {}
result_completion = {}
task_que = Queue(10)


def queue_openai_response(message, request_id):
    print("request id is: " + request_id)
    result_completion[request_id] = False
    print(message)
    print(request_id)
    task_que.put([message, request_id])
    # response = await Openai_calls.get_roast(message)


async def get_open_ai_response():
    while True:
        if not task_que.empty():
            task = task_que.get()
            result[task[1]] = Openai_calls.get_roast(task[0])
            print("process complete")
            print(task[0])
            print(task[1])
            result_completion[task[1]] = True
        else:
            await asyncio.sleep(1)


@app.route('/', methods=['POST'])
def receiving_request():
    data = request.data.decode()
    request_id = str(uuid.uuid4())
    queue_openai_response(data, request_id)
    return request_id, 200


@app.route('/retrieve', methods=['POST'])
def responding_to_request():
    request_id = request.data.decode()
    print("request_id is " + request_id)
    print(result)
    if request_id in result_completion:
        if request_id in result:
            print("returning result")
            print(result)
            return result[request_id], 200
        else:
            return "processing", 202
    print("returning 404")
    return "request id not found", 404


def run_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_open_ai_response())


if __name__ == "__main__":
    flask_thread = threading.Thread(target=app.run)
    processing_thread = threading.Thread(target=run_async_loop)

    flask_thread.start()
    processing_thread.start()
