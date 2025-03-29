from src.utils.scrapper import get_job_postings, export_to_csv
from src.entities import job_posting
from src.utils.google_search import google_search
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
        )
    )

    drop_columns = ["min_amount", "max_amount"]
    jobs = jobs.drop(
        columns=[col for col in drop_columns if col in jobs.columns])
    jobs.replace([np.inf, -np.inf], np.nan, inplace=True)  # Convert inf -> NaN
    jobs.fillna("", inplace=True)  # Convert NaN -> empty string

    jobs.loc[jobs["job_url_direct"].isna() | (jobs["job_url_direct"] == ""), "job_url_direct"] = jobs["company"].apply(
        lambda company_name: google_search(f"{company_name} jobs")
    )

    export_to_csv(jobs, data.search_term)

    return jobs.to_dict(orient="records")


def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)
