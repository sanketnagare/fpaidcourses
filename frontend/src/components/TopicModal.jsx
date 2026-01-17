import './TopicModal.css'

function TopicModal({ topic, isCompleted, onClose, onToggleComplete }) {
    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                {/* Header */}
                <div className="modal-header">
                    <div className="modal-title-section">
                        <span className="modal-number">{topic.order}</span>
                        <div>
                            <h2 className="modal-title">{topic.topic}</h2>
                            <p className="modal-description">{topic.description}</p>
                        </div>
                    </div>
                    <button className="modal-close" onClick={onClose}>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <path d="M18 6L6 18M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                {/* Meta Info */}
                <div className="modal-meta">
                    <span className="meta-badge">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="10" />
                            <path d="M12 6v6l4 2" />
                        </svg>
                        ~{topic.estimatedHours} hours
                    </span>
                    <span className="meta-badge">
                        📺 {topic.videos?.length || 0} videos
                    </span>
                    <span className="meta-badge">
                        📚 {topic.documentation?.length || 0} docs
                    </span>
                </div>

                {/* Videos Section */}
                {topic.videos && topic.videos.length > 0 && (
                    <div className="modal-section">
                        <h3 className="section-title">
                            <span className="section-icon">📺</span>
                            YouTube Videos
                        </h3>
                        <div className="videos-grid">
                            {topic.videos.map((video, idx) => (
                                <a
                                    key={idx}
                                    href={video.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="video-card"
                                >
                                    <div className="video-thumbnail">
                                        <img src={video.thumbnail} alt={video.title} />
                                        <span className="video-duration">{video.duration}</span>
                                    </div>
                                    <div className="video-info">
                                        <h4 className="video-title">{video.title}</h4>
                                        <div className="video-meta">
                                            <span className="video-channel">{video.channel}</span>
                                            <span className="video-views">{video.views} views</span>
                                        </div>
                                    </div>
                                </a>
                            ))}
                        </div>
                    </div>
                )}

                {/* Documentation Section */}
                {topic.documentation && topic.documentation.length > 0 && (
                    <div className="modal-section">
                        <h3 className="section-title">
                            <span className="section-icon">📚</span>
                            Documentation & Tutorials
                        </h3>
                        <div className="docs-list">
                            {topic.documentation.map((doc, idx) => (
                                <a
                                    key={idx}
                                    href={doc.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="doc-card"
                                >
                                    <div className="doc-icon">
                                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                            <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                                            <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" />
                                        </svg>
                                    </div>
                                    <div className="doc-info">
                                        <h4 className="doc-title">{doc.title}</h4>
                                        {doc.snippet && <p className="doc-snippet">{doc.snippet}</p>}
                                        <span className="doc-url">{new URL(doc.url).hostname}</span>
                                    </div>
                                    <svg className="doc-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                        <path d="M7 17L17 7M7 7h10v10" />
                                    </svg>
                                </a>
                            ))}
                        </div>
                    </div>
                )}

                {/* Footer Actions */}
                <div className="modal-footer">
                    <button
                        className={`complete-btn-large ${isCompleted ? 'completed' : ''}`}
                        onClick={onToggleComplete}
                    >
                        {isCompleted ? (
                            <>
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <path d="M5 12l5 5L20 7" />
                                </svg>
                                Completed
                            </>
                        ) : (
                            <>
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                    <circle cx="12" cy="12" r="10" />
                                </svg>
                                Mark as Complete
                            </>
                        )}
                    </button>
                </div>
            </div>
        </div>
    )
}

export default TopicModal
