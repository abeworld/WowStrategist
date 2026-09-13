import { Link, Navigate, Route, Routes } from "react-router-dom";
import CoveragePage from "./pages/CoveragePage";
import HomePage from "./pages/HomePage";
import MatchPage from "./pages/MatchPage";
import MatchupPage from "./pages/MatchupPage";

export default function App() {
  return (
    <div className="shell">
      <header className="app">
        <h1>WoW Arena Strategist</h1>
        <nav>
          <Link to="/">Lookup</Link>
          <Link to="/coverage">Coverage</Link>
        </nav>
      </header>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/coverage" element={<CoveragePage />} />
        <Route path="/matchup/:strategyKey" element={<MatchupPage />} />
        <Route path="/match/:matchId" element={<MatchPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
