from typing import List
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel
import uuid
import sqlite3
from sqlite3 import Connection
import sys

sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")

from uniflow.flow.client import TransformClient
from uniflow.flow.config import TransformExpandReduceConfig

app = FastAPI()


"""
For simiplicity, we use SQLite as the database for storing the job status and result.
However, SQLite is not suitable for high concurrency requirements. In my first design,
redis is used as the job queue and the job status and result are stored in PostgreSQL.
"""
DATABASE_NAME = "jobs.db"

# Create SQLite database and table
conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        input_data TEXT,
        output_data TEXT,
        status TEXT
    )
''')
conn.commit()
conn.close()


class Job(BaseModel):
    input_data: List[dict]


class JobResult(BaseModel):
    job_id: str
    status: str
    result: list


def get_db() -> Connection:
    return sqlite3.connect(DATABASE_NAME, check_same_thread=False)


async def run_expand_reduce_flow(job_id: str, input_data: List[dict], db: Connection):
    try:
        client = TransformClient(TransformExpandReduceConfig())
        output = client.run(input_data)
        filtered_output = [{k: v for k, v in item.items() if k != 'root'} for item in output]
        result_data = str(filtered_output)  # Convert result to string before storing in SQLite

        # Check if the record with the same job_id already exists
        existing_record = db.execute('SELECT 1 FROM jobs WHERE job_id = ?', (job_id,)).fetchone()

        if existing_record:
            # Update the existing record
            db.execute('''
                UPDATE jobs
                SET input_data = ?, output_data = ?, status = ?
                WHERE job_id = ?
            ''', (str(input_data), result_data, 'completed', job_id))
        else:
            # Insert a new record
            db.execute('''
                INSERT INTO jobs (job_id, input_data, output_data, status)
                VALUES (?, ?, ?, ?)
            ''', (job_id, str(input_data), result_data, 'completed'))

        db.commit()
    except Exception as e:
        db.execute('''
            INSERT INTO jobs (job_id, input_data, output_data, status)
            VALUES (?, ?, ?, ?)
        ''', (job_id, str(input_data), str(e), 'failed'))
        db.commit()


@app.post("/expand_reduce_flow/")
async def expand_reduce_flow(
        job: Job, background_tasks: BackgroundTasks, db: Connection = Depends(get_db)
):
    job_id = str(uuid.uuid4())

    # Insert a new record with 'processing' status
    db.execute('''
        INSERT INTO jobs (job_id, input_data, output_d]]]]]]]]]]]]
    ''', (job_id, str(job.input_data), None, 'processing'))
    db.commit()

    # Start the asynchronous task in the background
    background_tasks.add_task(run_expand_reduce_flow, job_id, job.input_data, db)

    return {"job_id": job_id}


@app.get("/check_status/{job_id}")
async def check_status(job_id: str, db: Connection = Depends(get_db)):
    result = db.execute('''
        SELECT status FROM jobs WHERE job_id = ?
    ''', (job_id,)).fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"job_id": job_id, "status": result[0]}


@app.get("/job_result/{job_id}")
async def read_job_result(job_id: str, db: Connection = Depends(get_db)):
    result = db.execute('''
        SELECT status, output_data FROM jobs WHERE job_id = ?
    ''', (job_id,)).fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")

    status, output_data = result
    return JobResult(job_id=job_id, status=status, result=eval(output_data) if output_data else None)
