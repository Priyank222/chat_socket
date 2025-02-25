import websockets
import asyncio
from websockets.asyncio.server import serve
import json
from http import HTTPStatus


async def handle_events(websocket):
    client_address = websocket.remote_address
    print(f"Client connected {client_address}")
    async for message in websocket:
        # Parse the incoming JSON message
        event = json.loads(message)
        event_type = event.get("type")
        event_data = event.get("data")

        print(f"Received event: {event_type} with data: {event_data}")

async def process_request(connection, request):
    """
    Handle HTTP requests that are not WebSocket upgrades.
    """
    if("HealthChecker" in request.headers.get("User-Agent","")):
        return connection.respond(HTTPStatus.OK, "OK\n")
    elif "Upgrade" not in request.headers:
        # Return a 400 Bad Request for non-WebSocket HTTP requests
        return connection.respond(HTTPStatus.BAD_REQUEST, "Websocket request required\n")

async def main():
    """
    Main server entry point.
    """
    async with serve(
        handle_events, 
        host="0.0.0.0", 
        port= 8080, 
        process_request=process_request,
        ping_interval=30,
        ping_timeout=10,
        close_timeout=10,
    )as server:
        print("Server running on port 8765")
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")

