import csv
import html
import requests
from datetime import datetime, timezone

# CAREERPILOT AI — LIVE JOB FINDER

LOCATIONS = ["Delhi", "Gurugram", "Gurgaon", "Noida"]

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
]

MIN_SALARY_LPA = 4.0

# Add verified Greenhouse board identifiers here.
# These are identifiers, not company names.
GREENHOUSE_BOARDS = []

OUTPUT_FILE = "jobs_found.csv"


def fetch_greenhouse_jobs(board_token):
    """Retrieve publicly listed jobs from one Greenhouse board."""

    endpoint = (
        "https://boards-api.greenhouse.io/v1/boards/"
        f"{board_token}/jobs"
    )

    try:
        response = requests.get(
            endpoint,
            params={"content": "true"},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError) as error:
        print(f"Could not retrieve board {board_token}: {error}")
        return []

    jobs = []

    for item in data.get("jobs", []):
        location = item.get("location") or {}
        description = html.unescape(
            item.get("content") or ""
        )

        jobs.append({
            "company": board_token,
            "title": item.get("title", ""),
            "location": location.get("name", ""),
            "description": description,
            "url": item.get("absolute_url", ""),
            "updated_at": item.get("updated_at", ""),
            "salary_lpa": None,
        })

    return jobs


def matches_preferences(job):
    """Keep jobs matching the preferred finance roles and locations."""

    title = job["title"].lower()
    location = job["location"].lower()

    relevant_role = any(
        keyword in title for keyword in KEYWORDS
    )

    relevant_location = any(
        city.lower() in location for city in LOCATIONS
    )

    if not relevant_role or not relevant_location:
        return False

    # Do not invent salary figures when the posting omits them.
    salary = job["salary_lpa"]

    if salary is not None and salary < MIN_SALARY_LPA:
        return False

    return True


def save_jobs(jobs):
    """Save matching vacancies to a CSV file."""

    fields = [
        "company",
        "title",
        "location",
        "salary_lpa",
        "url",
        "updated_at",
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
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(jobs)


def find_jobs():
    all_jobs = []

    for board in GREENHOUSE_BOARDS:
        all_jobs.extend(fetch_greenhouse_jobs(board))

    # Remove duplicate listings by application URL.
    unique_jobs = {}
    for job in all_jobs:
        if job["url"]:
            unique_jobs[job["url"]] = job

    matching_jobs = [
        job for job in unique_jobs.values()
        if matches_preferences(job)
    ]

    matching_jobs.sort(
        key=lambda job: (
            job["salary_lpa"] is not None,
            job["updated_at"],
        ),
        reverse=True,
    )

    save_jobs(matching_jobs)

    return matching_jobs


if __name__ == "__main__":
    print("CareerPilot AI — Live Job Search")
    print("Started:", datetime.now(timezone.utc).isoformat())

    if not GREENHOUSE_BOARDS:
        print(
            "\nNo verified job boards configured yet."
            "\nAdd employer board identifiers to "
            "GREENHOUSE_BOARDS before searching."
        )
    else:
        jobs = find_jobs()

        print(f"\nMatching vacancies: {len(jobs)}\n")

        for job in jobs:
            print(f"Company/board: {job['company']}")
            print(f"Role: {job['title']}")
            print(f"Location: {job['location']}")
            print(f"Salary: Not disclosed")
            print(f"Application: {job['url']}")
            print("-" * 45)

        print(f"\nResults saved to {OUTPUT_FILE}")
