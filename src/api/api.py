from src.utils.scrapper import get_job_postings
from src.entities import job_posting
from src.utils.cover_letter_gen import get_cover_letter
from fastapi import FastAPI
import numpy as np
import uvicorn


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/jobs")
def scrape_jobs(data: job_posting.ApiJobPosting):
    jobs = get_job_postings(
        job_posting=job_posting.JobPosting(
            search_term=data.search_term,
            location=data.location,
            results_wanted=data.results_wanted,
            hours_old=data.hours_old,
            is_remote=data.is_remote
        ),
        export_to_csv=True
    )

    drop_columns = ["min_amount", "max_amount"]
    jobs = jobs.drop(
        columns=[col for col in drop_columns if col in jobs.columns])
    jobs.replace([np.inf, -np.inf], np.nan, inplace=True)  # Convert inf -> NaN
    jobs.fillna("", inplace=True)  # Convert NaN -> empty string

    return jobs.to_dict(orient="records")


def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)
