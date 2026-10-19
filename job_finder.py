import requests

# Your job-search preferences
LOCATIONS = ["Delhi", "Gurugram", "Noida"]

KEYWORDS = [
    "Financial Analyst",
    "Finance Analyst",
    "Investment Analyst",
    "Credit Analyst",
    "FP&A Analyst",
    "MIS Analyst",
]

MIN_SALARY_LPA = 4.0
PREFERRED_SALARY_LPA = 6.0


def find_jobs():
    """
    Retrieve publicly available jobs from a supported job source.
    This initial version uses sample data until a live source is connected.
    """

    jobs = [
        {
            "company": "Example Finance Company",
            "title": "Junior Financial Analyst",
            "location": "Gurugram",
            "salary_lpa": 7.0,
            "url": "https://example.com/jobs/123",
        },
        {
            "company": "Example Consulting Company",
            "title": "Finance Analyst",
            "location": "Delhi",
            "salary_lpa": 5.0,
            "url": "https://example.com/jobs/456",
        },
    ]

    suitable_jobs = []

    for job in jobs:
        title_matches = any(
            keyword.lower() in job["title"].lower()
            for keyword in KEYWORDS
        )

        location_matches = any(
            location.lower() in job["location"].lower()
            for location in LOCATIONS
        )

        salary = job["salary_lpa"]

        if (
            title_matches
            and location_matches
            and salary >= MIN_SALARY_LPA
        ):
            suitable_jobs.append(job)

    suitable_jobs.sort(
        key=lambda job: job["salary_lpa"],
        reverse=True,
    )

    return suitable_jobs


if __name__ == "__main__":
    jobs = find_jobs()

    print("\nCAREERPILOT AI — JOB RESULTS\n")

    if not jobs:
        print("No matching jobs found.")

    for job in jobs:
        print(f"Company: {job['company']}")
        print(f"Role: {job['title']}")
        print(f"Location: {job['location']}")
        print(f"Salary: ₹{job['salary_lpa']} LPA")
        print(f"Apply: {job['url']}")
        print("-" * 40)
