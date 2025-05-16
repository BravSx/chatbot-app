from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from transformers import pipeline, set_seed

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# load GPT-2 from our cache at startup
generator = pipeline("text-generation", model="/app/model/gpt2")
set_seed(42)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(message: str = Form(...)):
    out = generator(
        message,
        max_length=50,
        num_return_sequences=1,
        pad_token_id=50256
    )
    text = out[0]["generated_text"]
    reply = text[len(message):].strip()
    return JSONResponse(content={"response": reply})
