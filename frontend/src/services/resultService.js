import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:5000/api",
    headers: {
        "Content-Type": "application/json"
    }
});

export const getLatestEvaluation = async () => {
    const response = await API.get("/results/latest");
    return response.data;
};

export const getEvaluationById = async (id) => {
    const response = await API.get(`/results/${id}`);
    return response.data;
};

export const downloadReport = async (id) => {
    const response = await API.get(
        `/results/${id}/report`,
        {
            responseType: "blob"
        }
    );

    return response.data;
};

export default API;