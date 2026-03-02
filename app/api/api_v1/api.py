from fastapi import APIRouter, WebSocket
from app.api.api_v1.endpoints import graph, query, annotation_sharing

api_router = APIRouter()

# Mount descriptors without prefix to match Flask routes
api_router.include_router(graph.router, tags=["graph"])
api_router.include_router(query.router, tags=["query"])
api_router.include_router(annotation_sharing.router, tags=["annotation_sharing"])

@api_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except Exception as e:
        print(f"WebSocket error: {e}")