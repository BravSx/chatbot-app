#!/usr/bin/env bash
set -euo pipefail

# where we cache the GPT-2 weights
CACHE_DIR=/app/model/gpt2
export TRANSFORMERS_CACHE=/app/model

# download into PVC-backed cache if missing
if [ ! -d "$CACHE_DIR" ]; then
  echo "Downloading GPT-2 small model into $CACHE_DIR…"
  python3 - <<'PYCODE'
import os
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

cache_dir = os.environ["TRANSFORMERS_CACHE"]
model_dir = os.path.join(cache_dir, "gpt2")
os.makedirs(model_dir, exist_ok=True)

print("→ Pulling tokenizer…")
GPT2TokenizerFast.from_pretrained("gpt2", cache_dir=cache_dir)
print("→ Pulling model…")
GPT2LMHeadModel.from_pretrained("gpt2", cache_dir=cache_dir)

print(f"Model cached in {model_dir}")
PYCODE
else
  echo "Using cached model in $CACHE_DIR."
fi

# launch FastAPI via Uvicorn
exec uvicorn app:app --host 0.0.0.0 --port 5000
