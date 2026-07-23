import API from "./api";

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
        `/student/download/${id}`,
        {
            responseType: "blob"
        }
    );

    return response.data;
};

export default API;
