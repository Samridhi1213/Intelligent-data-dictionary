import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Database, Search, Activity, MessageSquare, Download, Table as TableIcon, LayoutDashboard } from 'lucide-react';
import { metadataAPI } from './api';
import Dashboard from './components/Dashboard';
import TableExplorer from './components/TableExplorer';
import ChatInterface from './components/ChatInterface';
import './index.css';

function App() {
  const [metadata, setMetadata] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMetadata();
  }, []);

  const fetchMetadata = async () => {
    try {
      const res = await metadataAPI.getAll();
      setMetadata(res.data);
    } catch (err) {
      console.error("Failed to fetch metadata", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Router>
      <div className="sidebar">
        <h1 className="gradient-text" style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>DataAgent AI</h1>

        <nav style={{ display: 'flex', flex_direction: 'column', gap: '0.5rem' }}>
          <Link to="/" className="btn" style={{ color: 'inherit', text_decoration: 'none' }}>
            <LayoutDashboard size={20} /> Dashboard
          </Link>
          <Link to="/explorer" className="btn" style={{ color: 'inherit', text_decoration: 'none' }}>
            <TableIcon size={20} /> Table Explorer
          </Link>
          <Link to="/chat" className="btn" style={{ color: 'inherit', text_decoration: 'none' }}>
            <MessageSquare size={20} /> AI Chat
          </Link>
        </nav>

        <div style={{ marginTop: 'auto' }}>
          <button className="btn btn-primary w-full" onClick={() => metadataAPI.exportJSON()}>
            <Download size={18} /> Export JSON
          </button>
        </div>
      </div>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard metadata={metadata} loading={loading} />} />
          <Route path="/explorer" element={<TableExplorer metadata={metadata} />} />
          <Route path="/chat" element={<ChatInterface metadata={metadata} />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
