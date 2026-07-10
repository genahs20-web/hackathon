import { Navigate, Route, BrowserRouter as Router, Routes } from "react-router-dom";

import { Navbar } from "./components/Layout/Navbar";
import { Sidebar } from "./components/Layout/Sidebar";
import { useAuth } from "./hooks/useAuth";
import { AdminPage } from "./pages/AdminPage";
import { ChatPage } from "./pages/ChatPage";
import { ConflictsPage } from "./pages/ConflictsPage";
import { DashboardPage } from "./pages/DashboardPage";
import { DocumentsPage } from "./pages/DocumentsPage";
import { LoginPage } from "./pages/LoginPage";
import { NotFoundPage } from "./pages/NotFoundPage";
import { RecommendationsPage } from "./pages/RecommendationsPage";

function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <div className="p-6 text-secondary">Loading...</div>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="flex">
        <Sidebar />
        <main className="flex-1">{children}</main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/"
          element={
            <ProtectedLayout>
              <DashboardPage />
            </ProtectedLayout>
          }
        />
        <Route
          path="/documents"
          element={
            <ProtectedLayout>
              <DocumentsPage />
            </ProtectedLayout>
          }
        />
        <Route
          path="/chat"
          element={
            <ProtectedLayout>
              <ChatPage />
            </ProtectedLayout>
          }
        />
        <Route
          path="/conflicts"
          element={
            <ProtectedLayout>
              <ConflictsPage />
            </ProtectedLayout>
          }
        />
        <Route
          path="/recommendations"
          element={
            <ProtectedLayout>
              <RecommendationsPage />
            </ProtectedLayout>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedLayout>
              <AdminPage />
            </ProtectedLayout>
          }
        />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
}
