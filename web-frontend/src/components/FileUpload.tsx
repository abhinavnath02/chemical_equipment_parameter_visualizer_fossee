interface FileUploadProps {
  file: File | null
  loading: boolean
  error: string | null
  onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  onUpload: () => void
}

export default function FileUpload({
  file,
  loading,
  error,
  onFileChange,
  onUpload,
}: FileUploadProps) {
  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
      <h2 className="text-xl font-semibold mb-6 text-white">Upload CSV File</h2>
      
      <div className="space-y-4">
        <div className="relative">
          <input
            type="file"
            accept=".csv"
            onChange={onFileChange}
            className="block w-full text-sm text-gray-300 border border-zinc-700 rounded-lg cursor-pointer bg-zinc-800 p-3 hover:bg-zinc-750 transition-colors file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-medium file:bg-white file:text-black hover:file:bg-gray-200 file:cursor-pointer"
          />
          {file && (
            <p className="mt-3 text-sm text-gray-400">
              ✓ {file.name}
            </p>
          )}
        </div>

        <button
          onClick={onUpload}
          disabled={loading || !file}
          className="w-full bg-white text-black py-3 px-4 rounded-lg hover:bg-gray-200 disabled:bg-zinc-700 disabled:text-gray-500 disabled:cursor-not-allowed transition-all font-medium"
        >
          {loading ? 'Uploading...' : 'Upload & Analyze'}
        </button>

        {error && (
          <div className="bg-red-950 border border-red-800 text-red-300 p-3 rounded-lg text-sm">
            {error}
          </div>
        )}
      </div>
    </div>
  )
}
