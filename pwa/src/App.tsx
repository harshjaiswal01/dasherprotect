import React from 'react'
import Camera from './components/Camera'
import IdentifyPanel from './components/IdentifyPanel'

export default function App() {
    return (
        <div className="p-4 max-w-3xl mx-auto">
            <h1 className="text-2xl font-bold">Dasher Protect — MVP (M0)</h1>
            <p className="text-sm opacity-80">PWA scaffold: camera preview + API test.</p>
            <Camera />
            <IdentifyPanel />
        </div>
    )
}
