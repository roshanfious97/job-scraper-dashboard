import requests
from sqlalchemy import text

from app.database import engine


def scrape_remotive():

    print("Fetching jobs from Remotive...")

    inserted_count = 0

    try:

        response = requests.get(
            "https://remotive.com/api/remote-jobs",
            timeout=10
        )

        jobs = response.json()["jobs"]

    except Exception as e:

        print(f"Remotive Error: {e}")
        return 0

    with engine.connect() as conn:

        for job in jobs:

            title = job.get("title", "N/A")
            company = job.get("company_name", "N/A")
            location = job.get("candidate_required_location", "Remote")
            url = job.get("url")

            if not url:
                continue

            result = conn.execute(
                text(
                    """
                    INSERT INTO jobs
                    (
                        title,
                        company,
                        location,
                        source,
                        url
                    )
                    VALUES
                    (
                        :title,
                        :company,
                        :location,
                        :source,
                        :url
                    )
                    ON CONFLICT (url)
                    DO NOTHING
                    """
                ),
                {
                    "title": title,
                    "company": company,
                    "location": location,
                    "source": "Remotive",
                    "url": url
                }
            )

            if result.rowcount > 0:
                inserted_count += 1

        conn.commit()

    print(
        f"Inserted {inserted_count} Remotive jobs"
    )

    return inserted_count