import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { metadataAPI } from '../api';
import { Search, ChevronRight, Activity, FileText, AlertCircle } from 'lucide-react';

const TableExplorer = ({ metadata }) => {
    const [searchParams] = useSearchParams();
    const [selectedTable, setSelectedTable] = useState(null);
    const [quality, setQuality] = useState(null);
    const [docs, setDocs] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const tableParam = searchParams.get('table');
        if (tableParam && metadata[tableParam]) {
            handleTableSelect(tableParam);
        }
    }, [searchParams, metadata]);

    const handleTableSelect = async (name) => {
        setSelectedTable(name);
        setQuality(null);
        setDocs(null);
        setError(null);
        setLoading(true);
        try {
            const [qRes, dRes] = await Promise.all([
                metadataAPI.getQuality(name),
                metadataAPI.getDocumentation(name)
            ]);
            setQuality(qRes.data);

            if (dRes.data.error) {
                setError(dRes.data.error);
            } else {
                setDocs(dRes.data.documentation);
            }
        } catch (err) {
            console.error(err);
            setError("Failed to fetch documentation. Make sure the backend is running.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '2rem' }}>
            <div className="glass-card">
                <h3 style={{ marginBottom: '1rem' }}>Tables</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {Object.keys(metadata).map(name => (
                        <button
                            key={name}
                            onClick={() => handleTableSelect(name)}
                            className={`btn ${selectedTable === name ? 'btn-primary' : ''}`}
                            style={{ justifyContent: 'space-between', width: '100%', background: selectedTable === name ? '' : 'rgba(255,255,255,0.05)' }}
                        >
                            {name} <ChevronRight size={16} />
                        </button>
                    ))}
                </div>
            </div>

            <div className="fade-in">
                {selectedTable ? (
                    <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                            <h2 style={{ textTransform: 'capitalize' }}>{selectedTable}</h2>
                            <div style={{ display: 'flex', gap: '1rem' }}>
                                <span className="glass-card" style={{ padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                    Health: <span style={{ color: 'var(--success)', fontWeight: 'bold' }}>{quality?.health_score || '...'}%</span>
                                </span>
                            </div>
                        </div>

                        <div className="grid-dashboard" style={{ marginBottom: '2rem' }}>
                            <div className="glass-card">
                                <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                                    <Activity size={18} /> Quality Metrics
                                </h4>
                                {loading ? <p>Analyzing...</p> : quality && (
                                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                        <p>Total Rows: <strong>{quality.row_count}</strong></p>
                                        <p>Avg Completeness: <strong>{quality.health_score}%</strong></p>
                                    </div>
                                )}
                            </div>
                            <div className="glass-card">
                                <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                                    <FileText size={18} /> AI Summary
                                </h4>
                                {loading ? <p>Generating...</p> : error ? (
                                    <div style={{ background: 'rgba(239, 68, 68, 0.1)', padding: '1rem', borderRadius: '8px', borderLeft: '3px solid var(--danger)' }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--danger)', marginBottom: '0.5rem' }}>
                                            <AlertCircle size={16} /> Error
                                        </div>
                                        <p style={{ fontSize: '0.85rem' }}>{error}</p>
                                    </div>
                                ) : docs ? (
                                    <div style={{ maxHeight: '200px', overflowY: 'auto', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                        {docs}
                                    </div>
                                ) : <p>No documentation found.</p>}
                            </div>
                        </div>

                        <div className="glass-card">
                            <h3>Columns Schema</h3>
                            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
                                <thead>
                                    <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border-color)' }}>
                                        <th style={{ padding: '0.75rem' }}>Name</th>
                                        <th style={{ padding: '0.75rem' }}>Type</th>
                                        <th style={{ padding: '0.75rem' }}>Null %</th>
                                        <th style={{ padding: '0.75rem' }}>Distinct Ratio</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {metadata[selectedTable]?.columns.map(col => (
                                        <tr key={col.name} style={{ borderBottom: '1px solid var(--border-color)' }}>
                                            <td style={{ padding: '0.75rem' }}>{col.name}</td>
                                            <td style={{ padding: '0.75rem', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{col.type}</td>
                                            <td style={{ padding: '0.75rem' }}>
                                                {quality?.columns?.[col.name] ? (
                                                    <span style={{ color: quality.columns[col.name].null_percentage > 10 ? 'var(--danger)' : 'var(--success)' }}>
                                                        {quality.columns[col.name].null_percentage}%
                                                    </span>
                                                ) : '...'}
                                            </td>
                                            <td style={{ padding: '0.75rem' }}>
                                                {quality?.columns?.[col.name]?.distinct_ratio || '...'}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                ) : (
                    <div className="glass-card" style={{ textAlign: 'center', padding: '5rem' }}>
                        <Search size={48} style={{ marginBottom: '1rem', opacity: 0.5 }} />
                        <h3>Select a table to explore metadata and quality metrics</h3>
                    </div>
                )}
            </div>
        </div>
    );
};

export default TableExplorer;
