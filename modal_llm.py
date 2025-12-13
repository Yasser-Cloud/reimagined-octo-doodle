import modal
from pydantic import BaseModel

# Defines the Modal App
app = modal.App("digital-twin-llm")

def download_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer
    # Using LiquidAI/LFM2-1.2B-RAG
    model_id = "LiquidAI/LFM2-1.2B-RAG" 
    print(f"Downloading {model_id}...")
    try:
        AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
        AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    except Exception as e:
        print(f"Build Warning: {e}")

# Define the container image with dependencies and build step
image = (
    modal.Image.debian_slim()
    .pip_install("torch", "transformers", "accelerate")
    .run_function(download_model)
)

# Request Model
class QueryRequest(BaseModel):
    prompt: str

# The GPU Class
# Updated container_idle_timeout -> scaledown_window (Modal 1.0)
@app.cls(image=image, gpu="T4", scaledown_window=300)
class Model:
    # 2. Startup: Loads model into GPU memory
    @modal.enter()
    def setup(self):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.model_id = "LiquidAI/LFM2-1.2B-RAG"
        print("Loading LiquidAI Model into GPU...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, 
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )

    # 3. Method: The Generation Logic
    @modal.method()
    def generate(self, prompt: str):
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

# 4. Web Endpoint: The Interface for our Render App
@app.function(image=image)
@modal.web_endpoint(method="POST")
def api_generate(item: QueryRequest):
    """
    HTTP Endpoint reachable from anywhere (e.g. Render).
    """
    # Spin up the GPU class and call generate
    response = Model().generate.remote(item.prompt)
    return {"response": response}
