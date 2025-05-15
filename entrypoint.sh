#!/usr/bin/env bash
set -euo pipefail

CACHE_DIR=/app/model/gpt2

# If we haven’t already pulled GPT-2 weights into our PVC-backed cache, do it now:
if [ ! -d "$CACHE_DIR" ]; then
  echo "Downloading GPT-2 small model into $CACHE_DIR…"
  python3 - <<'PYCODE'
import os
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

cache_dir = os.environ.get("TRANSFORMERS_CACHE", "/app/model")
model_dir = os.path.join(cache_dir, "gpt2")
os.makedirs(model_dir, exist_ok=True)

print("→ Pulling tokenizer…")
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2", cache_dir=cache_dir)
print("→ Pulling model…")
model = GPT2LMHeadModel.from_pretrained("gpt2", cache_dir=cache_dir)

print(f"Saving to {model_dir}…")
tokenizer.save_pretrained(model_dir)
model.save_pretrained(model_dir)
PYCODE
  echo "Model downloaded."
else
  echo "Using cached model in $CACHE_DIR."
fi

# Finally start the Flask app
exec python3 app.py
