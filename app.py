@@
- generator = pipeline("text-generation", model="/app/model/gpt2")
+ generator = pipeline(
+     "text-generation",
+     model="/app/model/gpt2",
+     do_sample=True,           # enable sampling
+     top_k=50,                 # sample from top 50 tokens
+     top_p=0.95,               # nucleus sampling
+ )
 set_seed(42)
@@
- @app.post("/chat")
- async def chat(message: str = Form(...)):
-     out = generator(
-         message,
-         max_length=50,
-         num_return_sequences=1,
-         pad_token_id=50256
-     )
+@app.post("/chat")
+async def chat(message: str = Form(...)):
+    out = generator(
+        message,
+        max_length=50,
+        num_return_sequences=1,
+        pad_token_id=50256,
+    )
     text = out[0]["generated_text"]
     reply = text[len(message):].strip()
     return JSONResponse(content={"response": reply})
