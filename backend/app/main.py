from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.scrapers import scrape_all_jobs
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/jobs")
def get_jobs(
    search: str = Query(default=None),
    source: str = Query(default=None),
    page: int = Query(default=1),
    limit: int = Query(default=20)
):

    offset = (page - 1) * limit

    with engine.connect() as conn:

        if search:

            count_result = conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM jobs
                    WHERE
                    (
                        title ILIKE :search
                        OR company ILIKE :search
                        OR location ILIKE :search
                    )
                    AND
                    (
                        :source IS NULL
                        OR source = :source
                    )
                    """
                ),
                {
                    "search": f"%{search}%",
                    "source": source
                }
            )

            total = count_result.scalar()

            result = conn.execute(
                text(
                    """
                    SELECT *
                    FROM jobs
                    WHERE
                    (
                        title ILIKE :search
                        OR company ILIKE :search
                        OR location ILIKE :search
                    )
                    AND
                    (
                        :source IS NULL
                        OR source = :source
                    )
                    ORDER BY id DESC
                    LIMIT :limit
                    OFFSET :offset
                    """
                ),
                {
                    "search": f"%{search}%",
                    "source": source,
                    "limit": limit,
                    "offset": offset
                }
            )

        else:

            count_result = conn.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM jobs
                    WHERE
                    (
                        :source IS NULL
                        OR source = :source
                    )
                    """
                ),
                {
                    "source": source
                }
            )

            total = count_result.scalar()

            result = conn.execute(
                text(
                    """
                    SELECT *
                    FROM jobs
                    WHERE
                    (
                        :source IS NULL
                        OR source = :source
                    )
                    ORDER BY id DESC
                    LIMIT :limit
                    OFFSET :offset
                    """
                ),
                {
                    "source": source,
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
                    "source": row.source,
                    "url": row.url
                }
            )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "jobs": jobs
        }
    

@app.get("/sources")
def get_sources():

    with engine.connect() as conn:

        result = conn.execute(
            text(
                """
                SELECT DISTINCT source
                FROM jobs
                ORDER BY source
                """
            )
        )

        sources = []

        for row in result:
            sources.append(row.source)

        return sources


@app.post("/scrape-all")
def scrape_all():

    count = scrape_all_jobs()

    return {
        "message": f"{count} jobs scraped"
    }