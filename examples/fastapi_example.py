# File: examples/fastapi_example.py
from fastapi import FastAPI, Request, HTTPException
from rate_limiter import rate_limit, MemoryCache

app = FastAPI()
cache = MemoryCache()

# Note: In a production environment, you would adjust the identifier function
# to extract the client’s IP from the Request object via dependency injection.
def get_client_ip(request: Request):
    return "ip:" + request.client.host

@app.get("/fastapi-endpoint")
@rate_limit(
    limit=10,
    period=60,
    identifier=lambda: "ip:127.0.0.1",  # Replace with a dynamic identifier in production
    cache=cache,
    auto_ban=True,
    ban_threshold=20,
    ban_duration=120
)
async def my_fastapi_endpoint(request: Request):
    return {"message": "Hello from FastAPI!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

