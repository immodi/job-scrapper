from src.entities import job_posting
from jobspy import scrape_jobs
from datetime import datetime
from pandas import DataFrame as DataFrame
import csv


def get_job_postings(job_posting: job_posting.JobPosting, export_to_csv: bool = False) -> DataFrame:
    SOURCES = ["indeed", "linkedin", "zip_recruiter"]

    if not check_if_valid_country(job_posting.location):
        raise Exception("Country is not valid")

    jobs = scrape_jobs(
        site_name=SOURCES,
        search_term=job_posting.search_term,
        google_search_term=job_posting.search_term,
        location=job_posting.location,
        results_wanted=job_posting.results_wanted,
        hours_old=job_posting.hours_old,
        country_indeed=job_posting.location,
        is_remote=job_posting.is_remote
    )

    if export_to_csv:
        timestamp = datetime.now().strftime("%y%m%d%H%M")
        filename = f"{timestamp}_{job_posting.search_term.replace(' ', '_')}.csv"

        jobs.to_csv(filename, quoting=csv.QUOTE_NONNUMERIC,
                    escapechar="\\", index=False)

    return jobs


def check_if_valid_country(country: str):
    valid_countries = [
        "argentina", "australia", "austria", "bahrain", "belgium", "brazil", "canada", "chile",
        "china", "colombia", "costa rica", "czech republic", "denmark", "ecuador", "egypt", "finland",
        "france", "germany", "greece", "hong kong", "hungary", "india", "indonesia", "ireland",
        "israel", "italy", "japan", "kuwait", "luxembourg", "malaysia", "mexico", "morocco",
        "netherlands", "new zealand", "nigeria", "norway", "oman", "pakistan", "panama", "peru",
        "philippines", "poland", "portugal", "qatar", "romania", "saudi arabia", "singapore", "south africa",
        "south korea", "spain", "sweden", "switzerland", "taiwan", "thailand", "turkey", "ukraine",
        "united arab emirates", "united kingdom", "united states", "uruguay", "venezuela", "vietnam",
    ]

    if country.lower() in valid_countries:
        return country.title()  # Capitalize first letter of each word
    return None  # Return None if the country is not valid
