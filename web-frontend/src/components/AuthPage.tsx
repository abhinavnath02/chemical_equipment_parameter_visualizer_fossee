import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Login from './Login'
import Register from './Register'

export default function AuthPage() {
  const [showLogin, setShowLogin] = useState(true)
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4 py-8 relative overflow-hidden">
      {/* Rainbow gradient border */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-gradient-to-br from-red-500/15 to-transparent blur-3xl"></div>
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-gradient-to-bl from-blue-500/15 to-transparent blur-3xl"></div>
        <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-gradient-to-tr from-purple-500/15 to-transparent blur-3xl"></div>
        <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-gradient-to-tl from-green-500/15 to-transparent blur-3xl"></div>
      </div>
      
      <div className="w-full max-w-md relative z-10">
        <button
          onClick={() => navigate('/')}
          className="mb-6 text-gray-400 hover:text-white text-sm transition-colors flex items-center gap-2"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to Home
        </button>
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Chemical Equipment Parameter Visualizer
          </h1>
          <p className="text-gray-400">Sign in to continue</p>
        </div>

        {showLogin ? <Login /> : <Register />}

        <div className="mt-6 text-center">
          <button
            onClick={() => setShowLogin(!showLogin)}
            className="text-gray-400 hover:text-white text-sm transition-colors"
          >
            {showLogin ? "Don't have an account? Register" : 'Already have an account? Login'}
          </button>
        </div>
      </div>
    </div>
  )
}
