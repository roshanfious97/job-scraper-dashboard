from fastapi import FastAPI
from sqlalchemy import text
from fastapi import Query
from app.database import engine
from app.models import Base
from app.scraper import scrape_jobs


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Job Scraper API Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


from fastapi import Query


@app.get("/jobs")
def get_jobs(
    search: str = Query(default=None),
    page: int = Query(default=1),
    limit: int = Query(default=20)
):

    offset = (page - 1) * limit

    with engine.connect() as conn:

        if search:

            result = conn.execute(
                text(
                    """
                    SELECT *
                    FROM jobs
                    WHERE
                        title ILIKE :search
                        OR company ILIKE :search
                        OR location ILIKE :search
                    LIMIT :limit
                    OFFSET :offset
                    """
                ),
                {
                    "search": f"%{search}%",
                    "limit": limit,
                    "offset": offset
                }
            )

        else:

            result = conn.execute(
                text(
                    """
                    SELECT *
                    FROM jobs
                    LIMIT :limit
                    OFFSET :offset
                    """
                ),
                {
                    "limit": limit,
                    "offset": offset
                }
            )

        jobs = []

        for row in result:

            jobs.append(
                {
                    "id": row.id,
                    "title": row.title,
                    "company": row.company,
                    "location": row.location,
                    "url": row.url
                }
            )

        return jobs


@app.post("/scrape")
def scrape():

    count = scrape_jobs()

    return {
        "message": f"{count} jobs scraped"
    }