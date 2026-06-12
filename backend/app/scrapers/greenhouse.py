import requests
from sqlalchemy import text
from app.database import engine


GREENHOUSE_COMPANIES = [
    "notion",
    "airbnb",
    "duolingo",
    "stripe",
]


def scrape_greenhouse():

    inserted_count = 0

    with engine.connect() as conn:

        for company in GREENHOUSE_COMPANIES:

            url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs"

            try:

                response = requests.get(
                    url,
                    timeout=10
                )

                jobs = response.json()["jobs"]

                for job in jobs:

                    conn.execute(
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
                            "title": job["title"],
                            "company": company.capitalize(),
                            "location": job["location"]["name"],
                            "source": "Greenhouse",
                            "url": job["absolute_url"]
                        }
                    )

                    inserted_count += 1

            except Exception as e:

                print(
                    f"Greenhouse error ({company}): {e}"
                )

        conn.commit()

    return inserted_count