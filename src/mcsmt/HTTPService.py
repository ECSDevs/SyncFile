from fastapi import FastAPI
import uvicorn

app = FastAPI()

def read_and_clear_log():
    try:
        with open("mcsmt.log", "r") as file:
            content = file.read()
    except FileNotFoundError:
        return ""
    with open("mcsmt.log", "w") as file:
        file.write("")
    return content

@app.get("/client/getlog")
def get_log():
    return read_and_clear_log()

def do_job():
    uvicorn.run(app, host="127.0.0.1", port=36685)
