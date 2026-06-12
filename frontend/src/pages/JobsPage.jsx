import { useEffect, useState } from "react";
import { getJobs } from "../api/jobs";
import "./JobsPage.css";
import axios from "axios";

function JobsPage() {
    const [jobs, setJobs] = useState([]);
    const [total, setTotal] = useState(0);
    const [search, setSearch] = useState("");
    const [page, setPage] = useState(1);
    const [source, setSource] = useState("");
    const [sources, setSources] = useState([]);

    const fetchJobsData = async () => {
        const data = await getJobs({
            search,
            source,
            page,
            limit: 10,
        });

        setJobs(data.jobs);
        setTotal(data.total);
    };

    useEffect(() => {
        let ignore = false;

        const loadJobs = async () => {
            try {
                const data = await getJobs({
                    search,
                    source,
                    page,
                    limit: 10,
                });

                if (!ignore) {
                    setJobs(data.jobs);
                    setTotal(data.total);
                }
            } catch (error) {
                console.error("Failed to load jobs", error);
            }
        };

        void loadJobs();

        return () => {
            ignore = true;
        };
    }, [search, source, page]);

    useEffect(() => {
        let ignore = false;

        const loadSources = async () => {
            try {
                const response = await axios.get(
                    "http://localhost:8000/sources"
                );

                if (!ignore) {
                    setSources(response.data);
                }
            } catch (error) {
                console.error("Failed to load sources", error);
            }
        };

        void loadSources();

        return () => {
            ignore = true;
        };
    }, []);

    useEffect(() => {
        setPage(1);
    }, [search, source]);

    const handleScrape = async () => {
        try {

            const response = await axios.post(
                "http://localhost:8000/scrape-all"
            );

            alert(response.data.message);

            await fetchJobsData();

            try {
                const response = await axios.get(
                    "http://localhost:8000/sources"
                );

                setSources(response.data);
            } catch (error) {
                console.error("Failed to reload sources", error);
            }

        } catch (error) {

            console.error(error);

            alert("Failed to scrape jobs");
        }
    };

    return (
        <div className="page-container">
            <h1 className="page-title">
                Job Scraper Dashboard
            </h1>

            <p className="job-count">
                Showing {jobs.length} of {total} Jobs
            </p>

            <div
                style={{
                    display: "flex",
                    justifyContent: "center",
                    marginBottom: "20px"
                }}
            >
                <button
                    className="scrape-btn"
                    onClick={handleScrape}
                >
                    Scrape All Sources
                </button>
            </div>

            <div className="search-container">
                <input
                    className="search-input"
                    type="text"
                    placeholder="Search jobs..."
                    value={search}
                    onChange={(e) =>
                        setSearch(e.target.value)
                    }
                />

                <select
                    className="source-select"
                    value={source}
                    onChange={(e) =>
                        setSource(e.target.value)
                    }
                >
                    <option value="">
                        All Sources
                    </option>

                    {sources.map((sourceName) => (
                        <option
                            key={sourceName}
                            value={sourceName}
                        >
                            {sourceName}
                        </option>
                    ))}
                </select>
            </div>

            <div className="jobs-grid">
                {jobs.map((job) => (
                    <div
                        key={job.id}
                        className="job-card"
                    >
                        <h3 className="job-title">
                            {job.title}
                        </h3>

                        <p className="job-company">
                            {job.company}
                        </p>

                        <p className="job-location">
                            {job.location}
                        </p>

                        <div className="job-source">
                            {job.source}
                        </div>

                        <br />

                        <a
                            className="apply-btn"
                            href={job.url}
                            target="_blank"
                            rel="noreferrer"
                        >
                            Apply Now
                        </a>
                    </div>
                ))}
            </div>

            <div className="pagination">
                <button
                    disabled={page === 1}
                    onClick={() =>
                        setPage((prev) => prev - 1)
                    }
                >
                    Previous
                </button>

                <span>Page {page}</span>

                <button
                    onClick={() =>
                        setPage((prev) => prev + 1)
                    }
                >
                    Next
                </button>
            </div>
        </div>
    );
}

export default JobsPage;