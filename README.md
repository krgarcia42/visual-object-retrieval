# Visual Object Retrieval System

An event-driven pipeline built to process, analyze, and store image data using **Python**, **Redis**, and **FAISS Vector Search**.

## System Architecture
This project follows a microservices-style architecture where components communicate via an asynchronous message broker.
* **App layer**: Handles image metadata submissions via a Publisher.
* **Orchestrator**: Acts as a Subscriber, coordinating data flow between services in the background.
* **Inference Worker**: Simulates AI object detection and generates **128-dim vectors** (embeddings).
* **Document Store**: Manages JSON-based NoSQL metadata persistence within Redis.
* **Vector DB**: Utilizes **FAISS** to store embeddings with disk-based persistence for similarity searching.

## Tech Stack
* **Language**: Python 3.10
* **Messaging/Storage**: Redis (Pub/Sub & Document Store)
* **Vector Engine**: FAISS (Facebook AI Similarity Search)
* **Testing**: Unittest with Polling Resilience for asynchronous verification.
* **CI/CD**: GitHub Actions with automated service containers and final data audits.

## Data Ingestion
The system is pre-loaded with a hard-coded dataset of 10 images. Each image undergoes:
1.  **Event Trigger**: Publication of image data to a Redis channel.
2.  **Analysis**: Extraction of labels and high-fidelity inference simulation.
3.  **Vectorization**: Generation of persistent 128-dimensional embeddings.
4.  **Polyglot Storage**: JSON metadata is stored in Redis, while vectors are indexed in FAISS for Nearest Neighbor retrieval.

## Setup & Testing
1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Tests**:
    ```bash
    export PYTHONPATH=.
    python3 -m unittest discover tests
    ```
3.  **Run Ingestion**:
    ```bash
    # Start Orchestrator in background, then run ingestion
    python3 -c "from src.orchestrator import Orchestrator; Orchestrator().start()" &
    python3 scripts/ingest_data.py
    ```

## Video
[video1597628826.mov.zip](https://github.com/user-attachments/files/27102604/video1597628826.mov.zip)

## Video 2
[video1874110443.mov.zip](https://github.com/user-attachments/files/27213277/video1874110443.mov.zip)
