# Azure Deployment

## Project

Actuarial AI Economic Review Assistant is a Django application that combines:

- Django
- OpenAI
- LangChain
- Retrieval-Augmented Generation (RAG)
- Chroma vector database
- Docker
- Azure App Service
- Azure Container Registry
- Azure Bicep

The application reviews economic actuarial assumptions for an Iranian pension fund and uses an actuarial valuation report as reference information through RAG.

---

# Azure Architecture

The current Azure architecture is:

```text
Azure Subscription
        |
        v
actuarial-ai-rg
        |
        +----------------------+
        |                      |
        v                      v
Azure Container Registry   App Service Plan
actuarialaiacr             actuarial-ai-plan
        |                      |
        |                      v
        |               App Service
        |               actuarial-ai-app
        |                      |
        +------ Docker -------+
