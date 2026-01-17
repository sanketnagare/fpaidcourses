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

    const handleExport = () => {
        import('jspdf').then(({ jsPDF }) => {
            const doc = new jsPDF()

            // Title
            doc.setFontSize(22)
            doc.setTextColor(217, 119, 6) // Amber-600
            doc.text(course.title, 20, 20)

            doc.setFontSize(12)
            doc.setTextColor(100)
            doc.text(`Platform: ${course.platform}`, 20, 30)
            doc.line(20, 35, 190, 35)

            let y = 45

            roadmap.forEach((topic, i) => {
                // Add new page if logic requires (simple check)
                if (y > 250) {
                    doc.addPage()
                    y = 20
                }

                // Topic Header
                doc.setFontSize(16)
                doc.setTextColor(0)
                doc.text(`${i + 1}. ${topic.topic}`, 20, y)
                y += 10

                // Status
                const isCompleted = progress[topic.id]?.completed
                doc.setFontSize(10)
                doc.setTextColor(isCompleted ? 16 : 100, isCompleted ? 185 : 100, isCompleted ? 129 : 100)
                doc.text(`Status: ${isCompleted ? 'Completed' : 'Pending'}`, 25, y)
                y += 8

                // Video
                if (topic.videos && topic.videos[0]) {
                    const vid = topic.videos[0]
                    doc.setTextColor(50)
                    doc.text(`Video: ${vid.title}`, 25, y)
                    y += 6
                    doc.setTextColor(37, 99, 235) // Blue link
                    doc.textWithLink('Watch on YouTube', 25, y, { url: vid.url })
                    y += 10
                }

                // Docs
                if (topic.documentation && topic.documentation.length > 0) {
                    topic.documentation.slice(0, 2).forEach(d => {
                        doc.setTextColor(50)
                        doc.text(`Doc: ${d.title}`, 25, y)
                        y += 6
                        doc.setTextColor(37, 99, 235) // Blue link
                        doc.textWithLink('Read Documentation', 25, y, { url: d.url })
                        y += 8
                    })
                    y += 4
                }

                y += 10 // Spacing between topics
            })

            doc.save(`${course.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.pdf`)
        })
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
                <div className="header-left">
                    <button className="back-btn" onClick={onReset}>
                        ← New
                    </button>
                    <div className="action-buttons">
                        <button className="icon-btn" onClick={handleExport} title="Export to PDF">
                            📤 PDF
                        </button>
                    </div>
                </div>

                <div className="header-info">
                    <h1 className="course-title">{course.title}</h1>
                    <div className="header-badges">
                        <span className="platform-badge">{course.platform}</span>
                    </div>
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
