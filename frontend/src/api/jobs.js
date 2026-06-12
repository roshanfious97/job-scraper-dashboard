import axios from "axios";

const API_URL = "http://localhost:8000";

export const getJobs = async ({
  search = "",
  source = "",
  page = 1,
  limit = 10,
}) => {
  const response = await axios.get(`${API_URL}/jobs`, {
    params: {
      search,
      source: source || undefined,
      page,
      limit,
    },
  });

  return response.data;
};