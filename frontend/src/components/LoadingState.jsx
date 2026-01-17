import './LoadingState.css'

function LoadingState() {
    const steps = [
        { icon: '🔍', text: 'Scraping course page...' },
        { icon: '🤖', text: 'Analyzing curriculum with AI...' },
        { icon: '📺', text: 'Finding best YouTube videos...' },
        { icon: '📚', text: 'Gathering documentation...' },
        { icon: '🎯', text: 'Building your roadmap...' },
    ]

    return (
        <div className="loading-container">
            <div className="loading-content">
                {/* Animated Loader */}
                <div className="loader-graphic">
                    <div className="loader-ring"></div>
                    <div className="loader-ring"></div>
                    <div className="loader-ring"></div>
                    <span className="loader-emoji">🚀</span>
                </div>

                <h2 className="loading-title">Generating Your Roadmap</h2>
                <p className="loading-subtitle">
                    This may take 30-60 seconds depending on the course size
                </p>

                {/* Progress Steps */}
                <div className="loading-steps">
                    {steps.map((step, index) => (
                        <div
                            key={index}
                            className="loading-step animate-fade-in"
                            style={{ animationDelay: `${index * 0.5}s` }}
                        >
                            <span className="step-icon">{step.icon}</span>
                            <span className="step-text">{step.text}</span>
                        </div>
                    ))}
                </div>

                {/* Fun Fact */}
                <div className="loading-tip">
                    <span className="tip-icon">💡</span>
                    <span>Did you know? We find the most-viewed YouTube videos to ensure quality content!</span>
                </div>
            </div>
        </div>
    )
}

export default LoadingState
