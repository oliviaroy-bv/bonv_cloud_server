from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

clients = set()


@app.get("/")
async def root():
    return {"status": "BonV Cloud Server Running"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            # Broadcast received telemetry to every connected client
            disconnected = []

            for client in clients:
                try:
                    await client.send_text(data)
                except Exception:
                    disconnected.append(client)

            for client in disconnected:
                clients.discard(client)

    except WebSocketDisconnect:
        clients.discard(websocket)