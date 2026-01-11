import uvicorn
from . import config

if __name__ == "__main__":
    uvicorn.run("sentinel.proxy:app", host="0.0.0.0", port=config.API_PORT, reload=True)