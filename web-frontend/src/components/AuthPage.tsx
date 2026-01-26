import { useState } from 'react'
import Login from './Login'
import Register from './Register'

export default function AuthPage() {
  const [showLogin, setShowLogin] = useState(true)

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
