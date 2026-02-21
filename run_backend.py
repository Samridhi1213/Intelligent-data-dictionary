import os
import uvicorn

if __name__ == "__main__":
    # Ensure the script can locate the 'backend' package regardless of where it's called from
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8001, reload=True)
