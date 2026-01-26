import { useState } from 'react'
import Login from './Login'
import Register from './Register'

export default function AuthPage() {
  const [showLogin, setShowLogin] = useState(true)

  return (
    <div className="min-h-screen bg-black flex items-center justify-center px-4">
      <div className="w-full max-w-md">
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
