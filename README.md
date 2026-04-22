# Visual Object Retrieval System

An event-driven pipeline built to process, analyze, and store image data using **Python**, **Redis**, and **AI-driven embeddings**.

## System Architecture
This project follows a microservices-style architecture where components communicate via an asynchronous message broker.
* **App layer**: Handles image submissions.
* **Orchestrator**: Coordinates data flow between services.
* **Inference Worker**: Simulates AI object detection and generates 128-dim vectors.
* **Labeler**: Cleans and standardizes object tags.
* **Vector DB**: Stores embeddings and metadata in a searchable format.

## Tech Stack
* **Language**: Python
* **Messaging/Storage**: Redis Cloud
* **Testing**: Unittest & GitHub Actions (CI/CD)
* **Environment**: Environment variables for secure credential management.

## Data Ingestion
The system is pre-loaded with a hard-coded dataset of 10 images. Each image undergoes:
1.  **Validation**: Format checking via `FileUploader`.
2.  **Analysis**: Extraction of bounding boxes and labels (e.g., Tree, Car, Cat).
3.  **Vectorization**: Generation of random 128-dimensional embeddings.
4.  **Storage**: Final records are pushed to the Cloud Redis instance.

## Setup & Testing
1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Tests**:
    ```bash
    python -m unittest discover tests
    ```
3.  **Run Ingestion**:
    ```bash
    python scripts/ingest_data.py
    ```
