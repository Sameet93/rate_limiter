# My Rate Limiter

**My Rate Limiter** is a lightweight, flexible library for rate limiting in your FastAPI and Flask applications. It provides easy-to-use decorators that can be applied to endpoints, along with customizable options for per-user, per-IP, or per-endpoint limits. The library supports multiple caching backends—from in-memory storage to Redis or PostgreSQL—and includes an auto-ban feature to block abusive clients.

---

## Features

- **Plug-and-Play Decorators:** Easily add rate limits to any endpoint.
- **Flexible Configuration:** Customize limits based on user, IP, or endpoint.
- **Multiple Caching Backends:** Use the default in-memory cache or integrate with Redis, PostgreSQL, etc.
- **Auto-Ban Abusive Clients:** Automatically ban users who exceed defined abuse thresholds.
- **Framework Compatibility:** Works seamlessly with both FastAPI and Flask.

---

## Project Structure

```plaintext
rate_limiter/
├── rate_limiter/
│   ├── __init__.py         # Exposes the public API for the rate limiter.
│   ├── rate_limiter.py     # Contains the rate_limit decorator implementation.
│   └── caches.py           # Defines MemoryCache and other caching backend implementations.
├── examples/
│   ├── fastapi_example.py  # Example integration with FastAPI.
│   └── flask_example.py    # Example integration with Flask.
├── setup.py                # Packaging and installation configuration.
└── README.md               # Project documentation.

## Quick Start

### FastAPI Example

```python
# File: examples/fastapi_example.py
from fastapi import FastAPI, Request
from rate_limiter import rate_limit, MemoryCache

app = FastAPI()
cache = MemoryCache()

def get_client_ip(request: Request):
    # In production, extract the client IP dynamically from the request.
    return "ip:" + request.client.host

@app.get("/fastapi-endpoint")
@rate_limit(
    limit=10,
    period=60,
    identifier=lambda: "ip:127.0.0.1",  # Replace with a dynamic identifier in production.
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

### Flask Example

```python
# File: examples/flask_example.py
from flask import Flask, request, jsonify
from rate_limiter import rate_limit, MemoryCache

app = Flask(__name__)
cache = MemoryCache()

def get_remote_addr():
    return "ip:" + request.remote_addr

@app.route("/flask-endpoint")
@rate_limit(
    limit=10,
    period=60,
    identifier=get_remote_addr,
    cache=cache,
    auto_ban=True,
    ban_threshold=20,
    ban_duration=120
)
def my_flask_endpoint():
    return jsonify(message="Hello from Flask!")

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Business Model Canvas

| **Component**         | **Details**                                                                                     |
|-----------------------|-------------------------------------------------------------------------------------------------|
| **Problem**           | APIs need robust, easily integrated rate limiting to manage traffic and prevent abuse.          |
| **Solution**          | A lightweight rate limiter offering plug-and-play decorators, configurable limits, and auto-ban functionality.  |
| **Key Features**      | Easy integration, multiple caching backends, and auto-ban abusive clients.                      |
| **Customer Segments** | API-heavy businesses, developers, and platform providers.                                      |
| **Revenue Streams**   | Licensing or subscription fees for performance and enterprise features.                        |
| **Channels**          | GitHub, API marketplaces, developer communities, and direct sales.                              |
| **Cost Structure**    | Development, maintenance, support, and marketing.                                               |
| **Key Partners**      | API platforms, cloud service providers, and developer communities.                              |

---

## Installation

Install the package via pip:

```bash
pip install my_rate_limiter
```

---

## Contributing

Contributions are welcome!  
If you have suggestions, bug reports, or improvements, please open an issue or submit a pull request on [GitHub](https://github.com/Sameet93/rate_limiter).

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/MIT) file for details.

---

## Contact

For questions or feedback, please reach out at [sameetfe@gmail.com](mailto:sameetfe@gmail.com).

