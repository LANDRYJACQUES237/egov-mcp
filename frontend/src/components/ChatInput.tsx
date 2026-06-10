import { useState } from 'react'
import type { KeyboardEvent } from 'react'
import { Send } from 'lucide-react'

interface Props {
  onSend: (message: string) => void
  isLoading: boolean
}

const SUGGESTIONS = [
  "Quelles sont les échéances fiscales de mars 2025 ?",
  "Vérifie le matricule CNPS C1234567A",
  "Calcule les cotisations pour Alice avec 300000 FCFA",
  "Montre-moi les datasets publics sur l'éducation",
  "Recherche des entreprises dans le secteur finance",
]

export function ChatInput({ onSend, isLoading }: Props) {
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (!input.trim() || isLoading) return
    onSend(input.trim())
    setInput('')
  }

  const handleKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="border-t border-slate-200 bg-white p-4">
      {/* Suggestions */}
      <div className="flex gap-2 mb-3 overflow-x-auto pb-1 scrollbar-hide">
        {SUGGESTIONS.map((s, i) => (
          <button
            key={i}
            onClick={() => onSend(s)}
            disabled={isLoading}
            className="flex-shrink-0 text-xs px-3 py-1.5 rounded-full border border-slate-200 text-slate-600 hover:bg-slate-50 hover:border-blue-300 hover:text-blue-600 transition-colors disabled:opacity-50"
          >
            {s.length > 40 ? s.slice(0, 40) + '…' : s}
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="flex gap-2 items-end">
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          disabled={isLoading}
          placeholder="Posez votre question en français ou en anglais..."
          rows={1}
          className="flex-1 resize-none rounded-xl border border-slate-200 px-4 py-3 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:opacity-50 max-h-32"
          style={{ height: 'auto' }}
          onInput={e => {
            const t = e.target as HTMLTextAreaElement
            t.style.height = 'auto'
            t.style.height = Math.min(t.scrollHeight, 128) + 'px'
          }}
        />
        <button
          onClick={handleSend}
          disabled={!input.trim() || isLoading}
          className="flex-shrink-0 w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center hover:bg-blue-700 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
        >
          <Send size={16} />
        </button>
      </div>
      <p className="text-xs text-slate-400 mt-2 text-center">
        Entrée pour envoyer · Shift+Entrée pour nouvelle ligne
      </p>
    </div>
  )
}
