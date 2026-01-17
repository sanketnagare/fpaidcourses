import { useState, useEffect } from 'react'
import MilestoneNode from './MilestoneNode'
import TopicModal from './TopicModal'
import './RoadmapView.css'

function RoadmapView({ data, progress, toggleComplete, onReset, progressPercent, completedCount }) {
    const [selectedTopic, setSelectedTopic] = useState(null)
    const [showCelebration, setShowCelebration] = useState(false)
    const [lastCompletedId, setLastCompletedId] = useState(null)

    const { course, roadmap } = data

    // Check for course completion
    useEffect(() => {
        if (progressPercent === 100 && completedCount > 0) {
            setShowCelebration(true)
            setTimeout(() => setShowCelebration(false), 5000)
        }
    }, [progressPercent, completedCount])

    const handleToggleComplete = (topicId) => {
        const wasCompleted = progress[topicId]?.completed
        if (!wasCompleted) {
            setLastCompletedId(topicId)
            setTimeout(() => setLastCompletedId(null), 1500)
        }
        toggleComplete(topicId)
    }

    return (
        <div className="roadmap-container">
            {/* Celebration Confetti */}
            {showCelebration && (
                <div className="celebration-overlay">
                    <div className="confetti-container">
                        {[...Array(50)].map((_, i) => (
                            <div
                                key={i}
                                className="confetti"
                                style={{
                                    left: `${Math.random() * 100}%`,
                                    animationDelay: `${Math.random() * 2}s`,
                                    backgroundColor: ['#f59e0b', '#d97706', '#10b981', '#3b82f6', '#8b5cf6'][Math.floor(Math.random() * 5)]
                                }}
                            />
                        ))}
                    </div>
                    <div className="celebration-message">
                        <span className="celebration-emoji">🎓</span>
                        <h2>Course Completed!</h2>
                        <p>You've mastered all {course.totalTopics} topics!</p>
                    </div>
                </div>
            )}

            {/* Clean Minimal Header */}
            <header className="roadmap-header">
                <button className="back-btn" onClick={onReset}>
                    ← New Roadmap
                </button>

                <div className="header-info">
                    <h1 className="course-title">{course.title}</h1>
                    <span className="platform-badge">{course.platform}</span>
                </div>
            </header>

            {/* Simple Progress Bar */}
            <div className="progress-section">
                <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${progressPercent}%` }}></div>
                </div>
                <span className="progress-text">{completedCount} of {course.totalTopics} completed</span>
            </div>

            {/* Gameboard Path */}
            <div className="gameboard">
                <div className="path-container">
                    {roadmap.map((topic, index) => {
                        const isCompleted = progress[topic.id]?.completed
                        const justCompleted = lastCompletedId === topic.id

                        return (
                            <MilestoneNode
                                key={topic.id}
                                topic={topic}
                                index={index}
                                total={roadmap.length}
                                isCompleted={isCompleted}
                                justCompleted={justCompleted}
                                onClick={() => setSelectedTopic(topic)}
                                onToggleComplete={() => handleToggleComplete(topic.id)}
                            />
                        )
                    })}
                </div>
            </div>

            {/* Topic Modal */}
            {selectedTopic && (
                <TopicModal
                    topic={selectedTopic}
                    isCompleted={progress[selectedTopic.id]?.completed}
                    onClose={() => setSelectedTopic(null)}
                    onToggleComplete={() => handleToggleComplete(selectedTopic.id)}
                />
            )}
        </div>
    )
}

export default RoadmapView
