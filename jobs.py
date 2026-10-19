from dataclasses import dataclass


@dataclass
class Job:
    company: str
    title: str
    location: str
    salary_lpa: float | None
    skills: list[str]
    url: str = ""


PREFERENCES = {
    "locations": ["Delhi", "Gurugram", "Noida"],
    "roles": [
        "Financial Analyst",
        "Investment Analyst",
        "Equity Research Analyst",
        "Credit Analyst",
        "MIS Analyst",
        "FP&A Analyst",
        "Finance Analyst",
    ],
    "minimum_salary_lpa": 4.0,
    "preferred_salary_lpa": 6.0,
    "skills": [
        "Excel",
        "Financial Analysis",
        "Financial Modeling",
        "Power BI",
        "Accounting",
        "Reporting",
    ],
}


def score_job(job: Job) -> tuple[int, list[str]]:
    score = 0
    reasons = []

    # Location match
    if any(
        location.lower() in job.location.lower()
        for location in PREFERENCES["locations"]
    ):
        score += 10
        reasons.append("Preferred location")

    # Role match
    title = job.title.lower()

    if any(
        role.lower() in title
        for role in PREFERENCES["roles"]
    ):
        score += 30
        reasons.append("Relevant finance role")

    # Salary match
    if job.salary_lpa is None:
        reasons.append("Salary not disclosed; review required")
    elif job.salary_lpa < PREFERENCES["minimum_salary_lpa"]:
        return 0, ["Below minimum salary preference"]
    elif job.salary_lpa >= PREFERENCES["preferred_salary_lpa"]:
        score += 20
        reasons.append("Meets preferred salary")

    # Skills match
    matching_skills = [
        skill for skill in PREFERENCES["skills"]
        if any(
            skill.lower() in job_skill.lower()
            for job_skill in job.skills
        )
    ]

    score += min(40, len(matching_skills) * 10)

    if matching_skills:
        reasons.append(
            "Matching skills: " + ", ".join(matching_skills)
        )

    return score, reasons


if __name__ == "__main__":
    sample_jobs = [
        Job(
            company="Example Financial Services",
            title="Junior Financial Analyst",
            location="Gurugram",
            salary_lpa=7.0,
            skills=["Excel", "Financial Analysis", "Power BI"],
            url="https://example.com/jobs/123",
        ),
        Job(
            company="Example Sales Company",
            title="Sales Executive",
            location="Delhi",
            salary_lpa=8.0,
            skills=["Sales", "Communication"],
            url="https://example.com/jobs/456",
        ),
    ]

    for job in sample_jobs:
        score, reasons = score_job(job)

        print(f"\nCompany: {job.company}")
        print(f"Role: {job.title}")
        print(f"Score: {score}/100")
        print(f"Reasons: {', '.join(reasons)}")
