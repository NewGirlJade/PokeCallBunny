from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import core

app = FastAPI()

# look up how to make route handlers (look up fastAPI crash course)


@app.get("/")
def read_root():
    return FileResponse("./website/index.html")


@app.get("/api/random")
def get_random_pokemon_route():
    context = core.Context()

    random = core.gen_random_pokenumber(context)
    return core.get_pokemon_by_id(context, random)
