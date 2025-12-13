# Hybrid Deployment (Render + Modal)

This project uses a Hybrid Architecture for cost-efficiency:
1.  **Frontend/API**: Hosted on **Render** (Free Tier).
2.  **AI Engine**: Hosted on **Modal** (Serverless GPU, ~$0.0001/sec).

## 1. Deploy AI to Modal
Prerequisite: `uv` installed.

1.  **Install & Login**:
    ```bash
    make install       # Installs modal via uv
    uv run modal setup # Authenticate with Modal
    ```

2.  **Deploy**:
    ```bash
    make deploy-ai
    ```
    *   This will deploy the **LiquidAI** model to a T4 GPU.
    *   Copy the URL it gives you: `https://<your-username>--digital-twin-llm-api-generate.modal.run`


## 2. Link to Render
1.  Go to your Render Dashboard -> Environment Variables.
2.  Add a new Variable:
    *   **Key**: `MODAL_URL`
    *   **Value**: (The URL you got from step 1)

**That's it!** Your app on Render will now send prompts to the GPU on Modal, getting you high-performance AI responses for pennies.
