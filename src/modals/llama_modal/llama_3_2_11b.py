# https://modal.com/docs/examples/vllm_inference
import modal

vllm_image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install(
        "vllm==0.7.2",
        "huggingface_hub[hf_transfer]==0.26.2",
        "flashinfer-python==0.2.0.post2",  # pinning, very unstable
        extra_index_url="https://flashinfer.ai/whl/cu124/torch2.5",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})  # faster model transfers
)

# VLLM V1 doesn't support quantized VLMs yet
"""
File "/usr/local/lib/python3.12/site-packages/vllm/v1/attention/backends/flash_attn.py", line 134, in __init__
  raise NotImplementedError("Encoder self-attention and "
NotImplementedError: Encoder self-attention and encoder/decoder cross-attention
                                                                              are not implemented for FlashAttentionImpl
"""
vllm_image = vllm_image.env({"VLLM_USE_V1": "0"})


MODELS_DIR = "/llamas"
MODEL_NAME = "neuralmagic/Llama-3.2-11B-Vision-Instruct-FP8-dynamic"
MODEL_REVISION = "95d23e17186bdadbbd97dd8e7271caa610636b5a"

hf_cache_vol = modal.Volume.from_name("huggingface-cache", create_if_missing=True)
vllm_cache_vol = modal.Volume.from_name("vllm-cache", create_if_missing=True)

app = modal.App("llama-3.2-11b-vision")

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
        # limit-mm-per-prompt to allow more than 1 image per prompt
    ]

    subprocess.Popen(" ".join(cmd), shell=True)
