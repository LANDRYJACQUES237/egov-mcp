import { MessageSquare, Trash2, Zap, Globe } from 'lucide-react'

interface Props {
  onClear: () => void
  messageCount: number
}

const TOOLS = [
  { name: 'Calendrier fiscal', desc: 'Échéances DGI' },
  { name: 'Validation CNPS', desc: 'Vérif. matricule' },
  { name: 'Cotisations sociales', desc: 'Calcul CNPS/IRPP' },
  { name: 'Recherche entreprises', desc: 'Open Data Cameroun' },
  { name: 'Datasets publics', desc: 'data.gouv.cm' },
]

export function Sidebar({ onClear, messageCount }: Props) {
  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col h-full">
      {/* Logo */}
      <div className="p-5 border-b border-slate-700">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
            <Globe size={16} />
          </div>
          <div>
            <h1 className="font-semibold text-sm">eGov Cameroun</h1>
            <p className="text-xs text-slate-400">Assistant IA gouvernemental</p>
          </div>
        </div>
      </div>

      {/* Conversation */}
      <div className="p-4 border-b border-slate-700">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
            Conversation
          </span>
          {messageCount > 0 && (
            <button
              onClick={onClear}
              className="text-slate-400 hover:text-red-400 transition-colors"
              title="Effacer la conversation"
            >
              <Trash2 size={14} />
            </button>
          )}
        </div>
        <div className="flex items-center gap-2 text-sm text-slate-300">
          <MessageSquare size={14} />
          <span>{messageCount} message{messageCount !== 1 ? 's' : ''}</span>
        </div>
      </div>

      {/* Tools disponibles */}
      <div className="p-4 flex-1">
        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
          Tools MCP disponibles
        </span>
        <div className="mt-3 flex flex-col gap-2">
          {TOOLS.map((tool, i) => (
            <div key={i} className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-slate-800 transition-colors">
              <div className="w-6 h-6 bg-blue-500/20 rounded flex items-center justify-center flex-shrink-0 mt-0.5">
                <Zap size={11} className="text-blue-400" />
              </div>
              <div>
                <p className="text-xs font-medium text-slate-200">{tool.name}</p>
                <p className="text-xs text-slate-500">{tool.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="p-4 border-t border-slate-700">
        <p className="text-xs text-slate-500 text-center">
          Propulsé par Groq · Llama 3.3
        </p>
      </div>
    </aside>
  )
}
