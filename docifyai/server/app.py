from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root_test():
    return "Hello world"
