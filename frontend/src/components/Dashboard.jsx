import { useNavigate } from 'react-router-dom';
import { Database, Table as TableIcon, Activity, CheckCircle, ChevronRight } from 'lucide-react';

const Dashboard = ({ metadata, loading }) => {
    const navigate = useNavigate();
    if (loading) return <div>Loading...</div>;

    const tableCount = Object.keys(metadata).length;
    const columnCount = Object.values(metadata).reduce((acc, curr) => acc + curr.columns.length, 0);

    return (
        <div className="fade-in">
            <h2 style={{ marginBottom: '2rem' }}>System Overview</h2>

            <div className="grid-dashboard">
                <div className="glass-card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                        <Database className="primary" size={32} color="#6366f1" />
                        <div>
                            <p style={{ color: 'var(--text-secondary)' }}>Connected Database</p>
                            <h3 style={{ fontSize: '1.5rem' }}>PostgreSQL</h3>
                        </div>
                    </div>
                </div>

                <div className="glass-card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                        <TableIcon size={32} color="#a855f7" />
                        <div>
                            <p style={{ color: 'var(--text-secondary)' }}>Total Tables</p>
                            <h3 style={{ fontSize: '1.5rem' }}>{tableCount}</h3>
                        </div>
                    </div>
                </div>

                <div className="glass-card">
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem' }}>
                        <Activity size={32} color="#ec4899" />
                        <div>
                            <p style={{ color: 'var(--text-secondary)' }}>Total Columns</p>
                            <h3 style={{ fontSize: '1.5rem' }}>{columnCount}</h3>
                        </div>
                    </div>
                </div>
            </div>

            <div className="glass-card" style={{ marginTop: '2rem' }}>
                <h3 style={{ marginBottom: '1rem' }}>Recent Metadata Snapshots</h3>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.9rem' }}>Click a table row to explore its schema and documentation.</p>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border-color)' }}>
                            <th style={{ padding: '1rem' }}>Table Name</th>
                            <th style={{ padding: '1rem' }}>Columns</th>
                            <th style={{ padding: '1rem' }}>Primary Key</th>
                            <th style={{ padding: '1rem' }}>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(metadata).map(([name, info]) => (
                            <tr
                                key={name}
                                className="table-row-hover"
                                onClick={() => navigate(`/explorer?table=${name}`)}
                                style={{ borderBottom: '1px solid var(--border-color)', cursor: 'pointer' }}
                            >
                                <td style={{ padding: '1rem', fontWeight: '500' }}>{name}</td>
                                <td style={{ padding: '1rem' }}>{info.columns.length}</td>
                                <td style={{ padding: '1rem' }}>{info.primary_keys.join(', ')}</td>
                                <td style={{ padding: '1rem', color: 'var(--success)' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', justifyContent: 'space-between' }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <CheckCircle size={16} /> Ready
                                        </div>
                                        <ChevronRight size={14} style={{ opacity: 0.5 }} />
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default Dashboard;
