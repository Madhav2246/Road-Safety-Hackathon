// src/api/backend.js
import axios from "axios";

const BASE = "http://127.0.0.1:8000";

const client = axios.create({
  baseURL: BASE,
  timeout: 30000,
});

/**
 * ---------------------------------------------------------
 * Helper: Convert chainage string → meters
 * Examples:
 *   "4+200"
 *   "362+380 to 362+500"
 * ---------------------------------------------------------
 */
function parseChainage(text) {
  if (!text) return { start_m: 0, end_m: 0, length_m: 0 };

  const normalize = (s) => {
    if (!s.includes("+")) return parseInt(s, 10);
    const [km, m] = s.split("+").map((v) => parseInt(v, 10));
    return km * 1000 + m;
  };

  let start, end;

  if (text.includes("to")) {
    const [a, b] = text.split("to").map((v) => v.trim());
    start = normalize(a);
    end = normalize(b);
  } else if (text.includes("-")) {
    const [a, b] = text.split("-").map((v) => v.trim());
    start = normalize(a);
    end = normalize(b);
  } else {
    start = normalize(text.trim());
    end = start;
  }

  return {
    start_m: start,
    end_m: end,
    length_m: Math.abs(end - start),
  };
}

/**
 * ---------------------------------------------------------
 * API METHODS
 * ---------------------------------------------------------
 */
export const api = {
  /**
   * Upload PDF and extract interventions
   */
  uploadPDF: (formData) =>
    client
      .post("/extract/pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((res) => res.data),

  /**
   * 🔥 SINGLE SOURCE OF TRUTH
   * Full pipeline:
   *  - estimation
   *  - cost calculation
   *  - demographics
   */
  processAll: async (interventions) => {
    // Attach chainage_m to each intervention
    const payload = interventions.map((item) => ({
      ...item,
      chainage_m: parseChainage(item.chainage),
    }));

    const response = await client.post("/api/process-all", payload);
    return response.data;
  },

  /**
   * Ask chatbot a question with context
   */
  askChatbot: (question, context) =>
    client.post("/chatbot/ask", { question, context })
      .then(res => res.data),
};
