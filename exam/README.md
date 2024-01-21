# Backend Interview README
uniflow is a unified interface to solve data augmentation problem for LLM training. It enables use of different LLMs, including OpenAI, Huggingface, and LMQG with a single interface. Using uniflow, you can easily run different LLMs to generate questions and answers, chunk text, summarize text, and more.

To use uniflow, we recommend using the Docker and Kubernetes setup. This will ensure that you have all the dependencies installed and configured correctly.

## Docker and Kubernetes Setup
First, install Docker and Kubernetes and minikube


Then, clone the uniflow repository and run the following commands:

```bash
cd uniflow
minikube start
docker build -t uniflow-hanliao .
docker run -it -p 8080:8080 uniflow-hanliao # check if docker runs correctly
```

Applying the Kubernetes configuration:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Using the flowing command to get the service url:

```bash
kubectl get pods
kubectl get services
minikube service expand-reduce-service
```

and then you can access the service by going to http://localhost:8080 in your browser.


This will start a **ExpandReduceFlow** server on port 8080. You can access the server by going to http://localhost:8080 in your browser.

# Documentation for FastAPI Job Processing API

## Introduction

The FastAPI Job Processing API is designed to handle job processing tasks asynchronously using FastAPI, SQLite as a database, and the Uniflow library for job execution. The API allows clients to submit jobs, check job statuses, and retrieve job results.

## Overview

The API provides the following endpoints:

1. **Submit a Job**:
    - **Endpoint:** `POST /expand_reduce_flow/`
    - **Description:** Submits a job for processing.
    - **Request:**
      ```json
      {
        "job": {
          "input_data": [
            {"key1": "value1"},
            {"key2": "value2"},
            ...
          ]
        }
      }
      ```
    - **Response:**
      ```json
      {
        "job_id": "unique_job_id"
      }
      ```

2. **Check Job Status**:
    - **Endpoint:** `GET /check_status/{job_id}`
    - **Description:** Checks the status of a submitted job.
    - **Request:**
        - Path parameter: `job_id` (string)
    - **Response:**
      ```json
      {
        "job_id": "unique_job_id",
        "status": "job_status"
      }
      ```

3. **Retrieve Job Result**:
    - **Endpoint:** `GET /job_result/{job_id}`
    - **Description:** Retrieves the result of a completed job.
    - **Request:**
        - Path parameter: `job_id` (string)
    - **Response:**
      ```json
      {
        "job_id": "unique_job_id",
        "status": "completed",
        "result": [
          {"key1": "value1"},
          {"key2": "value2"},
          ...
        ]
      }
      ```

## Database

The API uses SQLite as the database for storing job status and results. The database has a single table named `jobs` with the following columns:

- `job_id` (TEXT, PRIMARY KEY): Unique identifier for each job.
- `input_data` (TEXT): Input data provided when submitting the job.
- `output_data` (TEXT): Resultant output data of the job.
- `status` (TEXT): Status of the job (e.g., "processing," "completed," "failed").

## Job Processing Workflow

1. **Job Submission:**
    - A new job is submitted by making a `POST` request to `/expand_reduce_flow/`.
    - The API generates a unique `job_id` for the job.
    - The job is inserted into the database with a status of "processing."

2. **Asynchronous Processing:**
    - An asynchronous task is started in the background using FastAPI's `BackgroundTasks`.
    - The task executes the `run_expand_reduce_flow` function, which uses the Uniflow library for job execution.
    - Upon completion, the job status is updated in the database.

3. **Checking Job Status:**
    - The status of a job can be checked by making a `GET` request to `/check_status/{job_id}`.
    - The response includes the job status.

4. **Retrieving Job Result:**
    - The result of a completed job can be retrieved by making a `GET` request to `/job_result/{job_id}`.
    - The response includes the job status and result data.

## Error Handling

- If a job is not found (e.g., non-existent `job_id`), the API returns a `404 Not Found` error with a relevant error message.

## Example Usage

### Submit a Job

```bash
curl -X POST -H "Content-Type: application/json" -d '{"job": {"input_data": [{"key1": "value1"}, {"key2": "value2"}]}}' http://localhost:8000/expand_reduce_flow/

### Check Job Status

```bash
curl http://localhost:8000/check_status/{job_id}
```

### Retrieve Job Result

```bash
curl http://localhost:8000/job_result/{job_id}
```

## Note
The API uses SQLite for simplicity but is not suitable for high-concurrency requirements. The initial design considered using Redis as the job queue and PostgreSQL for storing job status and results.
Feel free to use this documentation as a reference for interacting with the FastAPI Job Processing API.