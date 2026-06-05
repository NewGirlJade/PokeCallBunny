from fastapi import FastAPI, Response
from fastapi.responses import FileResponse


app = FastAPI()


@app.get("/")
# look up how to make route handlers (look up fastAPI crash course)


def read_root():
    return FileResponse("./website/index.html")
