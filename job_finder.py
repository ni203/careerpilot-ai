import csv
import html
import re
import requests
from datetime import datetime, timezone

# CAREERPILOT AI — JOB FINDER

KEYWORDS = [
    "financial analyst",
    "finance analyst",
    "investment analyst",
    "equity research",
    "credit analyst",
    "fp&a",
    "mis analyst",
    "financial planning",
    "business finance",
    "finance associate",
    "accountant",
    "financial reporting",
]

MIN_SALARY_LPA = 4.0
PREFERRED_SALARY_LPA = 6.0

REMOTIVE_API = "https://remotive.com/api/remote-jobs"
OUTPUT_FILE = "jobs_found.csv"


def fetch_remote_jobs():
    """Retrieve published remote jobs from Remotive."""

    try:
        response = requests.get(
            REMOTIVE_API,
            params={"limit": 500},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        return data.get("jobs", [])

    except (requests.RequestException, ValueError) as error:
        print(f"Could not retrieve Remotive jobs: {error}")
        return []


def matches_finance_role(job):
    """Match finance-related job titles and descriptions."""

    title = job.get("title", "").lower()

    # Avoid matching unrelated jobs just because finance is
    # mentioned somewhere in a long description.
    return any(keyword in title for keyword in KEYWORDS)


def accepts_candidate_location(job):
    """Keep remote roles that accept candidates in India or worldwide."""

    location = job.get(
        "candidate_required_location", ""
    ).lower()

    return (
        "india" in location
        or "worldwide" in location
        or "anywhere" in location
        or "all countries" in location
    )


def save_jobs(jobs):
    """Save vacancies to a CSV file."""

    fields = [
        "company",
        "title",
        "location",
        "salary",
        "job_type",
        "published",
        "source",
        "url",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )
        writer.writeheader()
        writer.writerows(jobs)


def find_jobs():
    """Fetch, filter and save matching remote finance vacancies."""

    raw_jobs = fetch_remote_jobs()
    results = {}
    today = datetime.now(timezone.utc)

    print(f"Retrieved {len(raw_jobs)} remote listings.")

    for job in raw_jobs:
        if not matches_finance_role(job):
            continue

        if not accepts_candidate_location(job):
            continue

        url = job.get("url", "")

        if not url:
            continue

        results[url] = {
            "company": job.get("company_name", "Unknown"),
            "title": job.get("title", ""),
            "location": job.get(
                "candidate_required_location", "Not specified"
            ),
            "salary": job.get("salary", "") or "Not disclosed",
            "job_type": job.get("job_type", "Not specified"),
            "published": job.get("publication_date", ""),
            "source": "Remotive",
            "url": url,
        }

    jobs = list(results.values())

    save_jobs(jobs)

    print(f"Matching remote finance jobs: {len(jobs)}")
    print(f"Results saved to {OUTPUT_FILE}")
    print("Source: Remotive")

    for job in jobs[:15]:
        print("-" * 45)
        print(f"Company: {job['company']}")
        print(f"Role: {job['title']}")
        print(f"Eligible location: {job['location']}")
        print(f"Salary: {job['salary']}")
        print(f"Apply: {job['url']}")
        print("Source: Remotive")


if __name__ == "__main__":
    print("CareerPilot AI — Live Job Search")
    find_jobs()
