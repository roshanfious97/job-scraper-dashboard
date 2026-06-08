import { useCallback, useEffect, useState } from "react";
import { getJobs } from "../api/jobs";
import "./JobsPage.css";

function JobsPage() {
  const [jobs, setJobs] = useState([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);


  const loadJobs = useCallback(async () => {
    const data = await getJobs({
      search,
      page,
      limit: 10,
    });

    setJobs(data.jobs);
  }, [search, page]);

  useEffect(() => {
    const fetchJobs = async () => {
      await loadJobs();
    };

    void fetchJobs();
  }, [loadJobs]);

  const handleSearch = async () => {
    const data = await getJobs({
      search,
      page: 1,
      limit: 10,
    });

    setJobs(data.jobs);
    setPage(1);
  };

return (
  <div className="page-container">
    <h1 className="page-title">
      Job Scraper Dashboard
    </h1>

    <div className="search-container">
      <input
        className="search-input"
        type="text"
        placeholder="Search jobs..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      <button
        className="search-button"
        onClick={handleSearch}
      >
        Search
      </button>
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