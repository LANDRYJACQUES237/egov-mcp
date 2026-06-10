import { useEffect, useRef } from 'react'
import { useChat } from './hooks/useChat'
import { ChatMessage } from './components/ChatMessage'
import { ChatInput } from './components/ChatInput'
import { Sidebar } from './components/Sidebar'
import { Bot, Loader2 } from 'lucide-react'

export default function App() {
  const { messages, isLoading, error, sendMessage, clearMessages } = useChat()
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      {/* Sidebar */}
      <Sidebar onClear={clearMessages} messageCount={messages.length} />

      {/* Main */}
      <main className="flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="bg-white border-b border-slate-200 px-6 py-4 flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
            <Bot size={16} className="text-white" />
          </div>
          <div>
            <h2 className="font-semibold text-slate-800 text-sm">Assistant eGov</h2>
            <p className="text-xs text-slate-500">
              Services gouvernementaux du Cameroun · FR / EN
            </p>
          </div>
          <div className="ml-auto flex items-center gap-1.5">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs text-slate-500">En ligne</span>
          </div>
        </header>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-6 py-6 flex flex-col gap-4">
          {messages.length === 0 && (
            <div className="flex-1 flex flex-col items-center justify-center text-center gap-4">
              <div className="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center">
                <Bot size={32} className="text-blue-600" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-700 mb-1">
                  Bonjour ! Comment puis-je vous aider ?
                </h3>
                <p className="text-sm text-slate-500 max-w-sm">
                  Posez vos questions sur les obligations fiscales, 
                  cotisations CNPS, ou les données publiques camerounaises.
                </p>
              </div>
            </div>
          )}

          {messages.map(message => (
            <ChatMessage key={message.id} message={message} />
          ))}

          {/* Loading */}
          {isLoading && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center flex-shrink-0">
                <Bot size={16} className="text-slate-600" />
              </div>
              <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm flex items-center gap-2">
                <Loader2 size={14} className="text-blue-600 animate-spin" />
                <span className="text-sm text-slate-500">Traitement en cours...</span>
              </div>
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-3 rounded-xl">
              {error}
            </div>
          )}

          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <ChatInput onSend={sendMessage} isLoading={isLoading} />
      </main>
    </div>
  )
}
