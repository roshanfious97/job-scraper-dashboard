from app.database import engine
from sqlalchemy import text
import requests


def scrape_jobs():

    print("Fetching jobs from RemoteOK...")

    try:
        response = requests.get(
            "https://remoteok.com/api",
            timeout=10
        )

        response.raise_for_status()

        jobs = response.json()

        print(f"Found {len(jobs) - 1} jobs")

    except Exception as e:
        print(f"Error fetching jobs: {e}")
        return 0

    inserted_count = 0

    with engine.connect() as conn:

        for job in jobs[1:]:

            title = job.get("position", "N/A")
            company = job.get("company", "N/A")
            location = job.get("location", "Remote")
            source = "RemoteOK"
            url = job.get("url")

            if not url:
                continue

            try:

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
                        "source": source,
                        "url": url
                    }
                )

                if result.rowcount > 0:
                    inserted_count += 1

            except Exception as e:
                print(f"Failed to insert {title}: {e}")

        conn.commit()

    print(f"Inserted {inserted_count} new jobs")

    return inserted_count


if __name__ == "__main__":

    count = scrape_jobs()

    print(f"{count} jobs scraped successfully!")