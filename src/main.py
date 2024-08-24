from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from src.api.board_api import board_router
from src.api.chatting_api import chat_router
from src.api.product_api import product_router
from src.api.gpt_api import gpt_router
from src.api.member_api import member_router
app = FastAPI(
    docs_url="/api/docs", 
    openapi_url="/api/openapi.json",
    redoc_url=None
)

app.include_router(board_router, prefix = "/api")
app.include_router(chat_router, prefix = "/api")
app.include_router(product_router, prefix = "/api")
app.include_router(gpt_router, prefix = "/api")
app.include_router(member_router, prefix = "/api")

# @app.websocket("/ws")
# async def connect_websocket(websocket: WebSocket):
#     print(f"client connected : {websocket.client}")
#     await websocket.accept() # client의 websocket접속 허용
#     await websocket.send_text(f"Welcome client : {websocket.client}")
#     while True:
#         data = await websocket.receive_text()  # client 메시지 수신대기
#         print(f"message received : {data} from : {websocket.client}")
#         await websocket.send_text(f"Message text was: {data}") # client에 메시지 전달


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var ws = new WebSocket("ws://localhost:8000/ws");
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """

# @app.get(path = "/api")
# async def get():
#     return HTMLResponse(html)