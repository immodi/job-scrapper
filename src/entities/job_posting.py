from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class JobPosting:
    search_term: str
    location: str
    results_wanted: int
    hours_old: int
    is_remote: bool


class ApiJobPosting(BaseModel):
    search_term: str
    location: str
    results_wanted: int
    hours_old: int
    is_remote: bool
