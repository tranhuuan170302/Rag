# Building an API Chatbot Using RAG Technology
## Description
This project leverages Retrieval-Augmented Generation (RAG) based on large language models (LLMs) to build a chatbot for book consultation. Users can inquire about book recommendations and reading preferences, and the chatbot will respond with tailored advice.

## Features
* Provide personalized book recommendations.
* Offer clickable links for users to purchase recommended books.
* Display ratings and reviews based on previous users' feedback.
## Technologies Used
* FastAPI
* LangChain
* RAG (Retrieval-Augmented Generation)
* Python
* MongoDB
## How to Use
Users can input questions or book-related inquiries, and the chatbot will provide relevant responses based on the trained data and embedded knowledge.

## Folder Structure
This template follows a structured format. The typical flow includes directories for API code, database interactions, and model training:
``` .
├── api                 # Contains the API logic (FastAPI routes, endpoints)
├── data                # Raw data and preprocessing scripts
├── models              # Trained models, embeddings, etc.
├── services            # Service layer for integrating different components
├── database            # MongoDB connection and operations
├── utils               # Helper functions and utility scripts
├── tests               # Unit and integration tests
└── README.md           # Project documentation
```
## Features Under Development
* Interactive Interface: Building a full-fledged interactive user interface.
* Redis Integration: Utilizing Redis to optimize costs and improve response time.
* Handling New Scenarios: Developing logic to handle scenarios not covered by the existing system.
## Demo:
