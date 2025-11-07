from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
import uvicorn
import json

app = FastAPI()

# Set the forwarding URL (e.g., your internal model server or OpenAI API)
LMSTUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"  # Replace if you want
FORWARD_API_KEY = "lm-studio"  # API key if required

@app.post("/v1/chat/completions")
async def proxy_openai(request: Request):
    payload = await request.json()
    
    # Process messages
    for message in payload["messages"]:
        if message["role"] == "developer":
            message["role"] = "user"
        message["content"] = str(message["content"])
    
    # Print incoming request
    print("Received payload:", payload)
    
    # Forward to actual OpenAI-compatible endpoint
    headers = {
        "Authorization": f"Bearer {FORWARD_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Check if the request is for streaming
    is_stream = payload.get("stream", False)
    
    if is_stream:
        # For streaming, we need to create a generator that keeps the client alive
        async def generate_stream():
            # Create a new client for this stream
            async with httpx.AsyncClient(timeout=None) as client:
                try:
                    async with client.stream("POST", LMSTUDIO_API_URL, headers=headers, json=payload) as response:
                        if response.status_code != 200:
                            error_content = await response.aread()
                            yield f"data: {json.dumps({'error': {'message': f'Error from LMStudio: {error_content.decode()}'}})}".encode()
                            yield b"data: [DONE]\n\n"
                            return
                        
                        async for chunk in response.aiter_bytes():
                            yield chunk
                except Exception as e:
                    error_json = json.dumps({"error": {"message": f"Error: {str(e)}"}})
                    yield f"data: {error_json}\n\n".encode()
                    yield b"data: [DONE]\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/event-stream"
        )
    else:
        # Non-streaming response
        async with httpx.AsyncClient(timeout=None) as client:
            try:
                response = await client.post(LMSTUDIO_API_URL, headers=headers, json=payload)
                return JSONResponse(content=response.json(), status_code=response.status_code)
            except Exception as e:
                return JSONResponse(
                    content={"error": {"message": f"Error processing request: {str(e)}"}},
                    status_code=500
                )

if __name__ == "__main__":
    uvicorn.run("router:app", host="0.0.0.0", port=8000, reload=True)
