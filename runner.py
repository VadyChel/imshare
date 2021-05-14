import uvicorn

if __name__ == "__main__":
    uvicorn.run("imshare.api.main:app", port=2222, reload=True)