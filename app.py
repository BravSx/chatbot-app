# FILE: app.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from transformers import pipeline, set_seed

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# load our cached GPT-2 at startup
generator = pipeline(
    "text-generation",
    model="/app/model/gpt2",
    tokenizer="/app/model/gpt2",
    device_map="auto",            # CUDA if available, fallback to CPU
)
set_seed(42)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(message: str = Form(...)):
    # sample  max_new_tokens tokens, with nucleus sampling
    out = generator(
        message,
        max_new_tokens=50,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.8,
        pad_token_id=50256,
    )
    generated = out[0]["generated_text"]
    # strip off the prompt, leave only new text
    reply = generated[len(message):].strip()
    return JSONResponse(content={"response": reply})
