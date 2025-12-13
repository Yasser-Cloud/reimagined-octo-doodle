import os

# Lazy Imports for optional dependencies
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
    _AI_AVAILABLE = True
except ImportError:
    _AI_AVAILABLE = False
    print("LLM: 'transformers' or 'torch' not found. AI features will be Mocked.")

MODEL_ID = "LiquidAI/LFM2-1.2B-RAG"

class LLMClient:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.mock_mode = False
        
        # Check availability
        if not _AI_AVAILABLE:
            self.mock_mode = True
            return

        # Check if we should attempt loading (ENV VAR or Default)
        if os.getenv("ENABLE_REAL_LLM", "False").lower() == "true":
            self._load_model()
        else:
            print("LLM: Running in Mock Mode (Default). Set ENABLE_REAL_LLM=True to load LiquidAI model.")
            self.mock_mode = True

    def _load_model(self):
        print(f"LLM: Loading {MODEL_ID}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID, 
                device_map="auto", 
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            print("LLM: Model Loaded Successfully.")
        except Exception as e:
            print(f"LLM: Failed to load model ({e}). Falling back to Mock.")
            self.mock_mode = True

    def generate_response(self, system_context: str, user_query: str) -> str:
        """
        Generates a response using the LLM (Modal, Local, or Mock).
        """
        # 1. Check for Modal (Prioritized)
        modal_url = os.getenv("MODAL_URL")
        if modal_url and modal_url.startswith("http"):
            return self._call_modal(modal_url, system_context, user_query)

        # 2. Mock Mode
        if self.mock_mode:
            return self._mock_response(user_query, system_context)
            
        # 3. Local Model (CPU/GPU)
        prompt = f"<|im_start|>system\n{system_context}<|im_end|>\n<|im_start|>user\n{user_query}<|im_end|>\n<|im_start|>assistant\n"
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(
                **inputs, 
                max_new_tokens=150,
                temperature=0.7,
                do_sample=True
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response.split("assistant")[-1].strip()
        except Exception as e:
            return f"Error generating response: {e}"

    def _call_modal(self, url, context, query):
        """Calls the serverless Modal endpoint."""
        import requests 
        # Note: requests must be installed. It usually is, but let's be safe.
        prompt = f"System: {context}\nUser: {query}\nAssistant:"
        try:
            res = requests.post(url, json={"prompt": prompt}, timeout=30)
            if res.status_code == 200:
                return res.json().get("response", "Error: No response field")
            return f"Modal Error {res.status_code}: {res.text}"
        except Exception as e:
            return f"Modal Connection Failed: {e}"

    def _mock_response(self, query, context):

        """Simple rule-based fallback for demo purposes."""
        query = query.lower()
        if "status" in query or "load" in query:
            if "Critical" in context:
                return "Based on the live twin data, I detected a CRITICAL issue. The Transformer T1 is overloaded. We advise immediate load shedding."
            return "The station is currently operating within normal parameters. Transformer load is steady."
        return "I am the Digital Twin Assistant. I can help you monitor asset health and grid status."

llm_client = LLMClient()
