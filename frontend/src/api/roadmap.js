// API configuration
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function generateRoadmap(url) {
    const response = await fetch(`${API_BASE}/generate-roadmap`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
    })

    const data = await response.json()

    if (!response.ok) {
        throw new Error(data.detail?.message || data.message || 'Failed to generate roadmap')
    }

    if (!data.success) {
        throw new Error(data.message || 'Failed to generate roadmap')
    }

    return data
}
