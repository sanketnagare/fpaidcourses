import { useState, useEffect } from 'react'
import './ThemeToggle.css'

function ThemeToggle() {
    const [theme, setTheme] = useState(() => {
        // Check localStorage first, then system preference
        const saved = localStorage.getItem('fpc_theme')
        if (saved) return saved
        return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'
    })

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme)
        localStorage.setItem('fpc_theme', theme)
    }, [theme])

    const toggleTheme = () => {
        setTheme(prev => prev === 'dark' ? 'light' : 'dark')
    }

    return (
        <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
            <span className="theme-toggle-icon">
                {theme === 'dark' ? '🌙' : '☀️'}
            </span>
            <span className="theme-toggle-text">
                {theme === 'dark' ? 'Dark' : 'Light'}
            </span>
        </button>
    )
}

export default ThemeToggle
