import './MilestoneNode.css'

function MilestoneNode({ topic, index, total, isCompleted, justCompleted, onClick, onToggleComplete }) {
    const isLeft = index % 2 === 0

    return (
        <div className={`milestone-row ${isLeft ? 'left' : 'right'} ${justCompleted ? 'just-completed' : ''}`}>
            {/* Connection Line */}
            {index > 0 && (
                <div className={`connection-line ${isCompleted ? 'completed' : ''}`}></div>
            )}

            <div
                className={`milestone-node ${isCompleted ? 'completed' : ''}`}
                onClick={onClick}
            >
                {/* Node Circle */}
                <div className="node-circle">
                    {isCompleted ? (
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3">
                            <path d="M5 12l5 5L20 7" />
                        </svg>
                    ) : (
                        <span className="node-number">{index + 1}</span>
                    )}

                    {/* Completion burst */}
                    {justCompleted && (
                        <div className="completion-burst">
                            <span>🎉</span>
                            <span>⭐</span>
                            <span>✨</span>
                            <span>🎊</span>
                        </div>
                    )}
                </div>

                {/* Content Card */}
                <div className="node-content">
                    <div className="node-header">
                        <h3 className="node-title">{topic.topic}</h3>
                        {isCompleted && <span className="completed-badge">✓ Done</span>}
                    </div>

                    <p className="node-description">{topic.description}</p>

                    <div className="node-meta">
                        <span className="meta-item">
                            <span className="meta-icon">⏱️</span>
                            {topic.estimatedHours}h
                        </span>
                        <span className="meta-item">
                            <span className="meta-icon">📺</span>
                            {topic.videos?.length || 0} videos
                        </span>
                        <span className="meta-item">
                            <span className="meta-icon">📚</span>
                            {topic.documentation?.length || 0} docs
                        </span>
                    </div>

                    {/* Action Buttons */}
                    <div className="node-actions">
                        <button className="view-btn" onClick={(e) => { e.stopPropagation(); onClick(); }}>
                            View Resources →
                        </button>
                        <button
                            className={`complete-btn ${isCompleted ? 'completed' : ''}`}
                            onClick={(e) => { e.stopPropagation(); onToggleComplete(); }}
                        >
                            {isCompleted ? '✓ Completed' : 'Mark Complete'}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default MilestoneNode
