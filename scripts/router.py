from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
import uvicorn
import json
import re
from time import sleep

app = FastAPI()

LMSTUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
FORWARD_API_KEY = "lm-studio"


@app.post("/v1/chat/completions")
async def proxy_openai(request: Request):
    payload = await request.json()

    # Normalize message roles
    for message in payload["messages"]:
        if message["role"] == "developer":
            message["role"] = "user"
        message["content"] = str(message["content"])

    print("Received payload:", json.dumps(payload, indent=2))

    headers = {
        "Authorization": f"Bearer {FORWARD_API_KEY}",
        "Content-Type": "application/json"
    }

    is_stream = payload.get("stream", False)

    if is_stream:
        async def generate_stream():
            async with httpx.AsyncClient(timeout=None) as client:
                try:
                    async with client.stream("POST", LMSTUDIO_API_URL, headers=headers, json=payload) as response:
                        if response.status_code != 200:
                            error_content = await response.aread()
                            yield f"data: {json.dumps({'error': {'message': f'Error from LMStudio: {error_content.decode()}'}})}\n\n".encode()
                            yield b"data: [DONE]\n\n"
                            return

                        async for chunk in response.aiter_bytes():
                            if not chunk:
                                continue

                            decoded = chunk.decode("utf-8", errors="ignore").strip()

                            # Match only actual "data:" lines
                            for line in decoded.splitlines():
                                if not line.startswith("data: "):
                                    continue
                                data_str = line[len("data: "):].strip()
                                if data_str == "[DONE]":
                                    continue
                                try:
                                    data = json.loads(data_str)
                                    delta = data.get("choices", [{}])[0].get("delta", {})
                                    if delta:  # Only print meaningful deltas
                                        print("🔹 Delta:", json.dumps(delta, ensure_ascii=False))
                                        sleep(0.1)
                                except json.JSONDecodeError:
                                    # Not a JSON object — skip it
                                    pass

                            yield chunk

                except Exception as e:
                    error_json = json.dumps({"error": {"message": f"Error: {str(e)}"}})
                    yield f"data: {error_json}\n\n".encode()
                    yield b"data: [DONE]\n\n"

        return StreamingResponse(generate_stream(), media_type="text/event-stream")

    else:
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
