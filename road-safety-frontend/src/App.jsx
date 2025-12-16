
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";

import HomePage from "./pages/HomePage";
import UploadPage from "./pages/UploadPage";
import ResultsPage from "./pages/ResultsPage";
import SummaryPage from "./pages/SummaryPage";
import AnalyticsPage from "./pages/AnalyticsPage";
import ChatBot from "./components/ChatBot";

function AppRoutes() {
  const location = useLocation();
  const context = location.state?.result || location.state?.demographics;

  return (
    <>
      <Routes>
        {/* Home / Landing */}
        <Route path="/" element={<HomePage />} />

        {/* Upload PDF */}
        <Route path="/upload" element={<UploadPage />} />

        {/* Flow pages */}
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/summary" element={<SummaryPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
      </Routes>

      {context && <ChatBot context={context} />}
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}
