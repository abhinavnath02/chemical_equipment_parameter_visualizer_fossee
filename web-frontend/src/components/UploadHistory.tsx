interface HistoryItem {
  filename: string
  uploaded_at: string
  total_equipment: number
}

interface UploadHistoryProps {
  history: HistoryItem[]
  onRefresh: () => void
  isOpen: boolean
  onToggle: () => void
}

export default function UploadHistory({ history, onRefresh, isOpen, onToggle }: UploadHistoryProps) {
  return (
    <>
      {/* Mobile/Tablet Toggle Button */}
      <button
        onClick={onToggle}
        className="lg:hidden fixed top-20 right-4 z-50 bg-zinc-900 border border-zinc-700 text-white p-3 rounded-lg shadow-lg hover:bg-zinc-800 transition-colors"
      >
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>

      {/* Sidebar */}
      <div
        className={`fixed lg:relative top-0 right-0 h-screen bg-zinc-900 border-l border-zinc-800 transition-transform duration-300 z-40 flex flex-col ${
          isOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0'
        } w-80`}
      >
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b border-zinc-800 flex-shrink-0">
          <h2 className="text-lg font-semibold text-white">Recent Uploads</h2>
          <div className="flex items-center gap-2">
            <button
              onClick={onRefresh}
              className="text-gray-400 hover:text-white transition-colors p-1"
              title="Refresh"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
            <button
              onClick={onToggle}
              className="lg:hidden text-gray-400 hover:text-white transition-colors p-1"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* History List */}
        <div className="flex-1 overflow-y-auto p-4">
          {history.length === 0 ? (
            <p className="text-gray-500 text-center py-8 text-sm">
              No uploads yet
            </p>
          ) : (
            <div className="space-y-2">
              {history.map((item, index) => (
                <div
                  key={index}
                  className="border border-zinc-800 rounded-lg p-3 hover:bg-zinc-800 transition-colors"
                >
                  <div className="flex justify-between items-start gap-2">
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-white text-sm truncate">
                        {item.filename}
                      </p>
                      <p className="text-xs text-gray-400 mt-1">
                        {new Date(item.uploaded_at).toLocaleDateString()} {new Date(item.uploaded_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </p>
                    </div>
                    <span className="bg-zinc-800 border border-zinc-700 text-gray-300 text-xs font-medium px-2 py-0.5 rounded whitespace-nowrap">
                      {item.total_equipment}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
          onClick={onToggle}
        />
      )}
    </>
  )
}
