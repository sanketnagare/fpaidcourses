import './LandingHero.css'

function LandingHero({
    url,
    setUrl,
    onSubmit,
    error,
    history = [],
    onLoadHistory,
    onRemoveHistory,
    onClearHistory,
    getHistoryProgress
}) {
    const formatDate = (dateString) => {
        const date = new Date(dateString)
        const now = new Date()
        const diffMs = now - date
        const diffMins = Math.floor(diffMs / 60000)
        const diffHours = Math.floor(diffMs / 3600000)
        const diffDays = Math.floor(diffMs / 86400000)

        if (diffMins < 1) return 'Just now'
        if (diffMins < 60) return `${diffMins}m ago`
        if (diffHours < 24) return `${diffHours}h ago`
        if (diffDays < 7) return `${diffDays}d ago`
        return date.toLocaleDateString()
    }

    return (
        <div className="landing">
            <div className="landing-content">
                {/* Logo/Brand */}
                <div className="brand animate-fade-in">
                    <div className="logo-container">
                        <span className="brand-icon">🎓</span>
                        <div className="logo-glow"></div>
                    </div>
                    <h1 className="brand-name">
                        Fuck<span className="gradient-text">Paid</span>Courses
                    </h1>
                </div>

                {/* Tagline */}
                <p className="tagline animate-fade-in" style={{ animationDelay: '0.1s' }}>
                    Transform any paid course into a <span className="gradient-text">free learning roadmap</span>
                    <br />with curated YouTube videos and documentation
                </p>

                {/* URL Input Form */}
                <form onSubmit={onSubmit} className="url-form animate-fade-in" style={{ animationDelay: '0.2s' }}>
                    <div className="input-wrapper">
                        <input
                            type="url"
                            className="url-input"
                            placeholder="Paste Udemy, Coursera, or any course URL..."
                            value={url}
                            onChange={(e) => setUrl(e.target.value)}
                            required
                        />
                        <button type="submit" className="submit-btn">
                            <span>Generate Roadmap</span>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M5 12h14M12 5l7 7-7 7" />
                            </svg>
                        </button>
                    </div>
                </form>

                {/* Error Message */}
                {error && (
                    <div className="error-message animate-fade-in">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="10" />
                            <path d="M12 8v4M12 16h.01" />
                        </svg>
                        <span>{error}</span>
                    </div>
                )}

                {/* Previous Roadmaps */}
                {history.length > 0 && (
                    <div className="history-section animate-fade-in" style={{ animationDelay: '0.25s' }}>
                        <div className="history-header">
                            <h2 className="section-title">📚 Your Roadmaps</h2>
                            <button className="clear-history-btn" onClick={onClearHistory}>
                                Clear All
                            </button>
                        </div>
                        <div className="history-grid">
                            {history.map((item) => {
                                const progress = getHistoryProgress(item)
                                return (
                                    <div key={item.id} className="history-card" onClick={() => onLoadHistory(item)}>
                                        <button
                                            className="history-remove"
                                            onClick={(e) => {
                                                e.stopPropagation()
                                                onRemoveHistory(item.id)
                                            }}
                                        >
                                            ×
                                        </button>
                                        <div className="history-platform">{item.platform}</div>
                                        <h3 className="history-title">{item.title}</h3>
                                        <div className="history-meta">
                                            <span>{item.totalTopics} topics</span>
                                            <span>•</span>
                                            <span>{formatDate(item.generatedAt)}</span>
                                        </div>
                                        <div className="history-progress">
                                            <div className="history-progress-bar">
                                                <div
                                                    className="history-progress-fill"
                                                    style={{ width: `${progress}%` }}
                                                ></div>
                                            </div>
                                            <span className="history-progress-text">{progress}%</span>
                                        </div>
                                    </div>
                                )
                            })}
                        </div>
                    </div>
                )}

                {/* How It Works */}
                <div className="how-it-works animate-fade-in" style={{ animationDelay: '0.3s' }}>
                    <h2 className="section-title">How It Works</h2>
                    <div className="steps-grid">
                        <div className="step-card">
                            <div className="step-number">1</div>
                            <div className="step-icon">🔗</div>
                            <h3>Paste URL</h3>
                            <p>Copy any paid course link from Udemy, Coursera, or other platforms</p>
                        </div>
                        <div className="step-card">
                            <div className="step-number">2</div>
                            <div className="step-icon">🤖</div>
                            <h3>AI Analysis</h3>
                            <p>Our AI extracts the curriculum and identifies key learning topics</p>
                        </div>
                        <div className="step-card">
                            <div className="step-number">3</div>
                            <div className="step-icon">🎯</div>
                            <h3>Get Roadmap</h3>
                            <p>Receive a structured path with free videos and documentation</p>
                        </div>
                    </div>
                </div>

                {/* Why Use This */}
                <div className="why-section animate-fade-in" style={{ animationDelay: '0.4s' }}>
                    <h2 className="section-title">Why Use FuckPaidCourses?</h2>
                    <div className="benefits-grid">
                        <div className="benefit-item">
                            <div className="benefit-icon">💰</div>
                            <div className="benefit-content">
                                <h4>Save Hundreds of Dollars</h4>
                                <p>Stop paying $100-$200 for courses when quality free content exists</p>
                            </div>
                        </div>
                        <div className="benefit-item">
                            <div className="benefit-icon">📺</div>
                            <div className="benefit-content">
                                <h4>Best YouTube Videos</h4>
                                <p>We find the most-viewed, highest-quality tutorials for each topic</p>
                            </div>
                        </div>
                        <div className="benefit-item">
                            <div className="benefit-icon">📚</div>
                            <div className="benefit-content">
                                <h4>Official Documentation</h4>
                                <p>Learn from official docs, MDN, Real Python, and trusted sources</p>
                            </div>
                        </div>
                        <div className="benefit-item">
                            <div className="benefit-icon">🎮</div>
                            <div className="benefit-content">
                                <h4>Track Your Progress</h4>
                                <p>Gamified learning path with milestones - mark topics as you go</p>
                            </div>
                        </div>
                        <div className="benefit-item">
                            <div className="benefit-icon">💾</div>
                            <div className="benefit-content">
                                <h4>Saves Locally</h4>
                                <p>Your progress is saved in browser - come back anytime</p>
                            </div>
                        </div>
                        <div className="benefit-item">
                            <div className="benefit-icon">⚡</div>
                            <div className="benefit-content">
                                <h4>Powered by AI</h4>
                                <p>Google Gemini AI understands course structure intelligently</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Stats */}
                <div className="stats-section animate-fade-in" style={{ animationDelay: '0.5s' }}>
                    <div className="stat-item">
                        <span className="stat-number">100%</span>
                        <span className="stat-label">Free Resources</span>
                    </div>
                    <div className="stat-divider"></div>
                    <div className="stat-item">
                        <span className="stat-number">10+</span>
                        <span className="stat-label">Platforms Supported</span>
                    </div>
                    <div className="stat-divider"></div>
                    <div className="stat-item">
                        <span className="stat-number">∞</span>
                        <span className="stat-label">Learning Potential</span>
                    </div>
                </div>

                {/* Supported Platforms */}
                <div className="platforms animate-fade-in" style={{ animationDelay: '0.6s' }}>
                    <span className="platforms-label">Supported Platforms:</span>
                    <div className="platform-badges">
                        <span className="platform-badge">Udemy</span>
                        <span className="platform-badge">Coursera</span>
                        <span className="platform-badge">Skillshare</span>
                        <span className="platform-badge">Pluralsight</span>
                        <span className="platform-badge">LinkedIn Learning</span>
                        <span className="platform-badge">edX</span>
                        <span className="platform-badge">+ More</span>
                    </div>
                </div>

                {/* Footer */}
                <div className="footer animate-fade-in" style={{ animationDelay: '0.7s' }}>
                    <p>Built with 💜 to democratize education</p>
                </div>
            </div>

            {/* Floating Education Icons */}
            <div className="floating-icons">
                <span className="floating-icon" style={{ left: '5%', animationDelay: '0s' }}>📚</span>
                <span className="floating-icon" style={{ left: '15%', animationDelay: '2s' }}>💡</span>
                <span className="floating-icon" style={{ left: '25%', animationDelay: '4s' }}>🎓</span>
                <span className="floating-icon" style={{ left: '40%', animationDelay: '1s' }}>📖</span>
                <span className="floating-icon" style={{ left: '55%', animationDelay: '3s' }}>✏️</span>
                <span className="floating-icon" style={{ left: '70%', animationDelay: '5s' }}>🔬</span>
                <span className="floating-icon" style={{ left: '85%', animationDelay: '2.5s' }}>💻</span>
                <span className="floating-icon" style={{ left: '95%', animationDelay: '4.5s' }}>🎯</span>
            </div>

            {/* Gradient Orbs */}
            <div className="orb orb-1"></div>
            <div className="orb orb-2"></div>
            <div className="orb orb-3"></div>
        </div>
    )
}

export default LandingHero
