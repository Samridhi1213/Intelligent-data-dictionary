import React, { useState } from 'react';
import { chatAPI } from '../api';
import { MessageSquare, Send, Bot, User, Code } from 'lucide-react';

const ChatInterface = ({ metadata }) => {
    const [messages, setMessages] = useState([
        { role: 'assistant', text: 'Hello! I am your Intelligent Data Assistant. Ask me anything about your data schema or for business insights.' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMsg = { role: 'user', text: input };
        setMessages([...messages, userMsg]);
        setInput('');
        setLoading(true);

        try {
            const res = await chatAPI.sendMessage(input);
            if (res.data.error) {
                setMessages(prev => [...prev, {
                    role: 'assistant',
                    text: res.data.explanation || res.data.error,
                    interpretation: res.data.business_interpretation
                }]);
            } else {
                const aiMsg = {
                    role: 'assistant',
                    text: res.data.explanation,
                    sql: res.data.sql,
                    interpretation: res.data.business_interpretation
                };
                setMessages(prev => [...prev, aiMsg]);
            }
        } catch (err) {
            setMessages(prev => [...prev, { role: 'assistant', text: "Sorry, I couldn't process that. Make sure the backend and AI service are configured correctly." }]);
        } finally {
            setLoading(false);
        }

    };

    return (
        <div style={{ height: 'calc(100vh - 100px)', display: 'flex', flexDirection: 'column' }}>
            <div className="glass-card" style={{ flex: 1, overflowY: 'auto', marginBottom: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem', padding: '2rem' }}>
                {messages.map((msg, i) => (
                    <div key={i} style={{
                        display: 'flex',
                        gap: '1rem',
                        maxWidth: '80%',
                        alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                        flexDirection: msg.role === 'user' ? 'row-reverse' : 'row'
                    }}>
                        <div style={{
                            width: '40px',
                            height: '40px',
                            borderRadius: '50%',
                            background: msg.role === 'user' ? 'var(--primary-color)' : 'var(--secondary-color)',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            flexShrink: 0
                        }}>
                            {msg.role === 'user' ? <User size={20} /> : <Bot size={20} />}
                        </div>
                        <div className="glass-card" style={{
                            background: msg.role === 'user' ? 'rgba(99, 102, 241, 0.1)' : 'rgba(255,255,255,0.05)',
                            padding: '1rem'
                        }}>
                            <p>{msg.text}</p>
                            {msg.sql && (
                                <div style={{ marginTop: '1rem', background: '#000', padding: '1rem', borderRadius: '8px' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem', color: 'var(--text-secondary)' }}>
                                        <Code size={14} /> Generated SQL
                                    </div>
                                    <code style={{ fontSize: '0.85rem', color: '#10b981' }}>{msg.sql}</code>
                                </div>
                            )}
                            {msg.interpretation && (
                                <p style={{ marginTop: '1rem', fontStyle: 'italic', opacity: 0.8 }}>
                                    💡 {msg.interpretation}
                                </p>
                            )}
                        </div>
                    </div>
                ))}
                {loading && <p style={{ color: 'var(--text-secondary)' }}>AI is thinking...</p>}
            </div>

            <div style={{ display: 'flex', gap: '1rem' }}>
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    placeholder="Ask a question (e.g., 'What is the average order value?')"
                    style={{ flex: 1 }}
                />
                <button className="btn btn-primary" onClick={handleSend} disabled={loading}>
                    <Send size={20} />
                </button>
            </div>
        </div>
    );
};

export default ChatInterface;
