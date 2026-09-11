Actuarial AI Economic Review Assistant

An AI-powered actuarial decision-support application for reviewing economic assumptions used in pension fund actuarial valuations.

The application combines Django, LangChain, OpenAI, Retrieval-Augmented Generation (RAG), Chroma, Docker, Azure App Service, Azure Container Registry, and Infrastructure as Code with Bicep.

The goal is to demonstrate how actuarial knowledge and data engineering can be combined with modern AI and cloud technologies to build a practical decision-support application.

⸻

Project Overview

Economic assumptions such as discount rates, wage growth, pension increases, productivity, investment returns, and borrowing costs can have a significant impact on pension fund actuarial liabilities.

This application allows a user to enter a new set of economic assumptions and receive an AI-assisted actuarial review.

The AI evaluates the assumptions using:

* Historical and economic considerations
* Internal consistency between assumptions
* Actuarial credibility
* Pension valuation considerations
* Evidence from an actuarial valuation report
* Sensitivity analysis
* Comparison with the previous assessment

The system is designed as a decision-support tool, not as a replacement for professional actuarial judgement.

⸻

Key Features

1. AI Actuarial Review

The application evaluates six economic assumptions:

* Discount rate
* Wage increase rate
* Annuity/pension increase rate
* Productivity rate
* Interest rate
* Borrowing rate

The AI produces:

* Overall score from 0–10
* Actuarial review
* Practical suggestions
* Comparison with the previous assessment

⸻

2. Retrieval-Augmented Generation (RAG)

The application uses RAG to provide the AI model with relevant evidence from an actuarial valuation report.

The workflow is:

User assumptions
       |
       v
Retrieve relevant evidence
       |
       v
Chroma Vector Database
       |
       v
Relevant actuarial report passages
       |
       v
LangChain
       |
       v
OpenAI model
       |
       v
Structured actuarial review

This approach reduces the need for the language model to rely only on its general knowledge.

The AI is instructed to use report evidence when relevant and avoid inventing information when the retrieved material does not support a particular conclusion.

⸻

Actuarial Evidence

The RAG knowledge base is based on an Iranian pension fund actuarial valuation report.

The report contains historical assumptions, actuarial results, and sensitivity analysis.

For example, the system includes sensitivity evidence showing the impact of changes in assumptions and demographic parameters on actuarial liabilities.

Example sensitivity results:

Scenario	Actuarial Liability (million Rial)
Base scenario	70,108,351
Retirement age +3 years	72,293,056
Retirement service +3 years	74,231,472
Wage rate +20%	74,313,946
Pension rate +20%	89,855,703

These results allow the AI to consider not only whether an assumption appears reasonable, but also the potential actuarial consequences of changing assumptions.

⸻

Technology Stack

Backend

* Python
* Django
* LangChain
* OpenAI API
* Pydantic

AI / RAG

* OpenAI
* LangChain
* OpenAI Embeddings
* Chroma
* Retrieval-Augmented Generation
* Structured model output

Data

* Actuarial valuation reports
* Python data processing
* SQLite for the current development/demo deployment
* Planned Azure SQL Database for persistent cloud storage

Cloud / DevOps

* Microsoft Azure
* Azure App Service
* Azure Container Registry
* Azure App Service Plan
* Azure Managed Identity
* Azure RBAC
* Docker
* Docker Desktop
* Azure CLI
* Bicep Infrastructure as Code

Planned

* Azure SQL Database
* GitHub Actions CI/CD
* Production application server
* Azure Storage
* Application monitoring

⸻

Architecture

Current architecture:

                         Azure
                          |
                    actuarial-ai-rg
                          |
          +---------------+---------------+
          |                               |
          v                               v
 Azure Container Registry          App Service Plan
     actuarialaiacr               actuarial-ai-plan
          |                               |
          |                               v
          |                       Azure App Service
          |                       actuarial-ai-app
          |                               |
          +------ Docker Image -----------+
                                          |
                                          v
                                  Django Application
                                          |
                       +------------------+------------------+
                       |                                     |
                       v                                     v
                  LangChain                              RAG
                       |                                     |
                       v                                     v
                  OpenAI API                         Chroma Vector DB
                       |                                     |
                       +------------------+------------------+
                                          |
                                          v
                                  Actuarial Review

The App Service uses a system-assigned managed identity with the AcrPull role to retrieve the private Docker image from Azure Container Registry.

⸻

Infrastructure as Code

Azure infrastructure is defined using Bicep.

bicep/
├── main.bicep
├── acr.bicep
├── appservice-plan.bicep
├── appservice.bicep
└── acr-pull.bicep

The main Bicep deployment is subscription-scoped and creates the resource group and application infrastructure.

Current Azure resources include:

Resource Group
    actuarial-ai-rg
Container Registry
    actuarialaiacr
App Service Plan
    actuarial-ai-plan
App Service
    actuarial-ai-app

This demonstrates Infrastructure as Code rather than manually creating every Azure resource through the portal.

⸻

Docker

The application is containerized using Docker.

Because development is performed on an Apple Silicon Mac, the image is explicitly built for AMD64 before being deployed to Azure:

docker build --platform linux/amd64 -t actuarial-ai:v3 .

The image is then tagged and pushed to Azure Container Registry:

docker tag actuarial-ai:v3 \
    actuarialaiacr.azurecr.io/actuarial-ai:v3
docker push \
    actuarialaiacr.azurecr.io/actuarial-ai:v3

The current Azure deployment uses:

actuarialaiacr.azurecr.io/actuarial-ai:v3

Versioned image tags are used instead of relying only on latest, making deployments easier to identify and reproduce.

⸻

Azure Deployment

The application is currently deployed to Azure App Service as a Linux container.

Current deployment:

Region:
Australia East
Resource Group:
actuarial-ai-rg
App Service:
actuarial-ai-app
Container Registry:
actuarialaiacr
Image:
actuarialaiacr.azurecr.io/actuarial-ai:v3

Application:

https://actuarial-ai-app.azurewebsites.net

Detailed deployment instructions are available in:

DEPLOYMENT.md

⸻

Security

Secrets are not stored in the repository.

The following values are provided through environment variables / Azure App Service Application Settings:

OPENAI_API_KEY
DJANGO_SUPERUSER_USERNAME
DJANGO_SUPERUSER_EMAIL
DJANGO_SUPERUSER_PASSWORD

The .env file is excluded from Git.

Generated and local files are also excluded:

.env
.venv/
db.sqlite3
rag/chroma_db/
__pycache__/
*.pyc

The application also uses Azure Managed Identity for authentication between App Service and Azure Container Registry, avoiding the need to store ACR credentials.

⸻

Authentication

The application uses Django authentication.

Users must log in before accessing the actuarial review application.

The current Azure demo environment creates the initial administrator account during container startup using environment variables.

This is a temporary approach for the current SQLite-based deployment.

The planned Azure SQL architecture will provide persistent authentication data and remove this temporary initialization approach.

⸻

Current Database Architecture

The current demo deployment uses SQLite.

This keeps the initial application simple and allows the project to demonstrate the complete AI + RAG + Docker + Azure deployment workflow.

However, SQLite is not intended to be the final production database for the cloud deployment.

The planned architecture is:

Django
   |
   v
Azure SQL Database

This will provide persistent database storage independently of the application container.

⸻

Local Development

Clone the repository:

git clone https://github.com/Ehsan-rajabi/ai-economic-review-assistant.git

Enter the project directory:

cd ai-economic-review-assistant

Create a virtual environment:

python -m venv .venv

Activate it on macOS/Linux:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

OPENAI_API_KEY=your_api_key

Run Django migrations:

python manage.py migrate

Create an administrator:

python manage.py createsuperuser

Start the development server:

python manage.py runserver

The application will then be available locally at:

http://127.0.0.1:8000/

⸻

Project Structure

ai-economic-review-assistant/
│
├── bicep/
│   ├── main.bicep
│   ├── acr.bicep
│   ├── appservice-plan.bicep
│   ├── appservice.bicep
│   └── acr-pull.bicep
│
├── mainapp/
│   ├── templates/
│   ├── views.py
│   └── ...
│
├── rag/
│   ├── documents/
│   │   └── 1405_iran-irp.docx
│   ├── chroma_db/
│   └── rag.py
│
├── django_openai/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── ai_review.py
├── create_azure_user.py
├── manage.py
├── Dockerfile
├── DEPLOYMENT.md
├── requirements.txt
└── .gitignore

⸻

Engineering Highlights

This project demonstrates several areas of practical software engineering:

Actuarial Domain Knowledge

The application applies pension actuarial concepts to economic assumptions, liabilities, and sensitivity analysis.

Data Engineering

The project integrates structured actuarial information and unstructured actuarial report content into an AI workflow.

AI Engineering

The application uses:

* LLM integration
* LangChain
* Structured output
* Prompt engineering
* Embeddings
* Vector search
* RAG

Backend Development

The application is implemented using Django with:

* Authentication
* Forms
* Server-side processing
* API integration
* Environment-based configuration

Cloud Engineering

The application is deployed to Azure using:

* App Service
* Container Registry
* Managed Identity
* RBAC
* Azure CLI
* Bicep

DevOps

The project uses:

* Git
* GitHub
* Docker
* Infrastructure as Code
* Versioned container images

The next stage is automated CI/CD using GitHub Actions.

⸻

Why This Project

This project combines several areas of my professional background and current technical development:

Actuarial Science
        +
Data Engineering
        +
Python
        +
AI / LLM
        +
RAG
        +
Cloud
        +
DevOps

Rather than demonstrating these technologies as isolated tutorials, the project applies them to a real actuarial use case.

The objective is to demonstrate the ability to take a domain-specific problem from data and actuarial analysis through AI integration, containerization, Infrastructure as Code, and cloud deployment.

⸻

Roadmap

Completed

* Django application
* User authentication
* AI economic assumption review
* Structured AI output
* LangChain integration
* RAG implementation
* Chroma vector database
* Actuarial report integration
* Docker containerization
* Azure Container Registry
* Azure App Service
* Azure Managed Identity
* ACR Pull RBAC
* Bicep Infrastructure as Code
* Azure deployment
* Azure application testing

Next

* Azure SQL Database
* Persistent cloud database
* Production WSGI/ASGI server
* GitHub Actions CI/CD
* Automated Docker deployment
* Automated Bicep deployment
* Azure Storage
* Application monitoring
* Production security hardening

⸻

Disclaimer

This application is a technical demonstration and decision-support prototype.

AI-generated actuarial assessments should not be treated as professional actuarial advice or as a substitute for review by a qualified actuary.

The economic assumptions and actuarial information used in the demonstration are specific to the underlying actuarial report and should not be interpreted as current economic forecasts.

⸻

Repository

GitHub:

https://github.com/Ehsan-rajabi/ai-economic-review-assistant