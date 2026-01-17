import { useState, useEffect } from 'react'
import LandingHero from './components/LandingHero'
import RoadmapView from './components/RoadmapView'
import LoadingState from './components/LoadingState'
import ThemeToggle from './components/ThemeToggle'
import { generateRoadmap } from './api/roadmap'

const HISTORY_KEY = 'fpc_roadmap_history'
const MAX_HISTORY = 10

function App() {
    const [url, setUrl] = useState('')
    const [roadmapData, setRoadmapData] = useState(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [progress, setProgress] = useState({})
    const [history, setHistory] = useState([])

    // Load history from localStorage on mount
    useEffect(() => {
        const savedHistory = localStorage.getItem(HISTORY_KEY)
        if (savedHistory) {
            try {
                setHistory(JSON.parse(savedHistory))
            } catch (e) {
                console.error('Failed to parse history:', e)
            }
        }

        // Check for shared URL
        const params = new URLSearchParams(window.location.search)
        const courseUrl = params.get('course')
        if (courseUrl) {
            setUrl(courseUrl)
            handleGenerate(courseUrl)
        }
    }, [])

    const handleGenerate = async (courseUrl) => {
        setLoading(true)
        setError(null)

        try {
            const data = await generateRoadmap(courseUrl)
            setRoadmapData(data)
            saveToHistory(data)
            // Clean URL without refresh
            window.history.replaceState({}, '', window.location.pathname)
        } catch (err) {
            setError(err.message || 'Failed to generate roadmap from shared link')
        } finally {
            setLoading(false)
        }
    }

    // Load progress from localStorage
    useEffect(() => {
        if (roadmapData) {
            const key = `fpc_progress_${btoa(roadmapData.course.originalUrl).slice(0, 20)}`
            const saved = localStorage.getItem(key)
            if (saved) {
                setProgress(JSON.parse(saved))
            } else {
                // Initialize progress
                const initial = {}
                roadmapData.roadmap.forEach(topic => {
                    initial[topic.id] = { completed: false, completedAt: null }
                })
                setProgress(initial)
            }
        }
    }, [roadmapData])

    // Save progress to localStorage
    useEffect(() => {
        if (roadmapData && Object.keys(progress).length > 0) {
            const key = `fpc_progress_${btoa(roadmapData.course.originalUrl).slice(0, 20)}`
            localStorage.setItem(key, JSON.stringify(progress))
        }
    }, [progress, roadmapData])

    // Save roadmap to history
    const saveToHistory = (data) => {
        const historyItem = {
            id: Date.now(),
            title: data.course.title,
            platform: data.course.platform,
            originalUrl: data.course.originalUrl,
            totalTopics: data.course.totalTopics,
            generatedAt: data.generatedAt || new Date().toISOString(),
            roadmapData: data, // Store full roadmap data
        }

        setHistory(prev => {
            // Remove duplicate if exists
            const filtered = prev.filter(h => h.originalUrl !== data.course.originalUrl)
            // Add to front, limit to MAX_HISTORY
            const updated = [historyItem, ...filtered].slice(0, MAX_HISTORY)
            localStorage.setItem(HISTORY_KEY, JSON.stringify(updated))
            return updated
        })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!url.trim()) return

        setLoading(true)
        setError(null)

        try {
            const data = await generateRoadmap(url)
            setRoadmapData(data)
            saveToHistory(data)
        } catch (err) {
            setError(err.message || 'Failed to generate roadmap')
        } finally {
            setLoading(false)
        }
    }

    const loadFromHistory = (historyItem) => {
        setRoadmapData(historyItem.roadmapData)
        setUrl(historyItem.originalUrl)
    }

    const removeFromHistory = (id) => {
        setHistory(prev => {
            const updated = prev.filter(h => h.id !== id)
            localStorage.setItem(HISTORY_KEY, JSON.stringify(updated))
            return updated
        })
    }

    const clearHistory = () => {
        setHistory([])
        localStorage.removeItem(HISTORY_KEY)
    }

    const toggleComplete = (topicId) => {
        setProgress(prev => ({
            ...prev,
            [topicId]: {
                completed: !prev[topicId]?.completed,
                completedAt: !prev[topicId]?.completed ? new Date().toISOString() : null
            }
        }))
    }

    const handleReset = () => {
        setRoadmapData(null)
        setUrl('')
        setProgress({})
        setError(null)
    }

    // Calculate progress for history items
    const getHistoryProgress = (historyItem) => {
        const key = `fpc_progress_${btoa(historyItem.originalUrl).slice(0, 20)}`
        const saved = localStorage.getItem(key)
        if (saved) {
            try {
                const progress = JSON.parse(saved)
                const completed = Object.values(progress).filter(p => p.completed).length
                const total = historyItem.totalTopics
                return Math.round((completed / total) * 100)
            } catch (e) {
                return 0
            }
        }
        return 0
    }

    const completedCount = Object.values(progress).filter(p => p.completed).length
    const totalCount = roadmapData?.roadmap?.length || 0
    const progressPercent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0

    if (loading) {
        return (
            <>
                <ThemeToggle />
                <LoadingState />
            </>
        )
    }

    if (roadmapData) {
        return (
            <>
                <ThemeToggle />
                <RoadmapView
                    data={roadmapData}
                    progress={progress}
                    toggleComplete={toggleComplete}
                    onReset={handleReset}
                    progressPercent={progressPercent}
                    completedCount={completedCount}
                />
            </>
        )
    }

    return (
        <>
            <ThemeToggle />
            <LandingHero
                url={url}
                setUrl={setUrl}
                onSubmit={handleSubmit}
                error={error}
                history={history}
                onLoadHistory={loadFromHistory}
                onRemoveHistory={removeFromHistory}
                onClearHistory={clearHistory}
                getHistoryProgress={getHistoryProgress}
            />
        </>
    )
}

export default App
