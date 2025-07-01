# https://modal.com/docs/examples/vllm_inference
import modal

vllm_image = modal.Image.debian_slim(python_version="3.12").pip_install(
    "vllm==0.8.2",
    "transformers==4.50.3",
    "huggingface_hub[hf_transfer]==0.26.2",
    "flashinfer-python==0.2.0.post2",  # pinning, very unstable
    extra_index_url="https://flashinfer.ai/whl/cu124/torch2.5",
)

# VLLM V1 doesn't support quantized VLMs yet
"""
File "/usr/local/lib/python3.12/site-packages/vllm/v1/attention/backends/flash_attn.py", line 134, in __init__
  raise NotImplementedError("Encoder self-attention and "
NotImplementedError: Encoder self-attention and encoder/decoder cross-attention
                                                                              are not implemented for FlashAttentionImpl
"""
# HF_HUB for faster model transfers
vllm_image = vllm_image.env({"VLLM_USE_V1": "0", "HF_HUB_ENABLE_HF_TRANSFER": "1"})


MODELS_DIR = "/llamas"
MODEL_NAME = "RedHatAI/gemma-3-4b-it-FP8-dynamic"
MODEL_REVISION = "e8535f618f3ff62cd745395b05eb8cbde0851b71"

hf_cache_vol = modal.Volume.from_name("huggingface-cache", create_if_missing=True)
vllm_cache_vol = modal.Volume.from_name("vllm-cache", create_if_missing=True)

app = modal.App("gemma-3-4b")

N_GPU = 1
# api key, for auth. for production use, replace with a modal.Secret
API_KEY = "super-secret-key"

MINUTES = 60  # seconds
VLLM_PORT = 8000


@app.function(
    image=vllm_image,
    gpu=f"A100:{N_GPU}",
    # how many requests can one replica handle? tune carefully!
    allow_concurrent_inputs=100,
    # how long should we stay up with no requests?
    scaledown_window=15 * MINUTES,
    volumes={
        "/root/.cache/huggingface": hf_cache_vol,
        "/root/.cache/vllm": vllm_cache_vol,
    },
)
@modal.web_server(port=VLLM_PORT, startup_timeout=5 * MINUTES)
def serve():
    import subprocess

    cmd = [
        "vllm",
        "serve",
        "--uvicorn-log-level=info",
        MODEL_NAME,
        "--revision",
        MODEL_REVISION,
        "--host",
        "0.0.0.0",
        "--port",
        str(VLLM_PORT),
        "--enforce-eager",
        "--max-num-seqs",
        "16",
        "--max-model-len",
        "40000",
        "--api-key",
        API_KEY,
    ]

    subprocess.Popen(" ".join(cmd), shell=True)
