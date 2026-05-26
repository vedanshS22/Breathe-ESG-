import { Navigate, Route, Routes } from "react-router-dom";
import AppLayout from "./layouts/AppLayout.jsx";
import AuditPage from "./pages/AuditPage.jsx";
import DashboardPage from "./pages/DashboardPage.jsx";
import ReviewQueuePage from "./pages/ReviewQueuePage.jsx";
import UploadPage from "./pages/UploadPage.jsx";

export default function App() {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/review" element={<ReviewQueuePage />} />
        <Route path="/audit" element={<AuditPage />} />
      </Routes>
    </AppLayout>
  );
}

