from app.scrapers.remoteok import scrape_remoteok
from app.scrapers.greenhouse import scrape_greenhouse
from app.scrapers.remotive import scrape_remotive


def scrape_all_jobs():

    total = 0

    total += scrape_remoteok()
    total += scrape_greenhouse()
    total += scrape_remotive()

    return total