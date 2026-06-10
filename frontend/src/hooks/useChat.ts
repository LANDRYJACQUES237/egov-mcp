import { useState, useCallback } from 'react'
import axios from 'axios'
import type { Message, ToolCall, HistoryMessage } from '../types'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [history, setHistory] = useState<HistoryMessage[]>([])

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.post(`${API_URL}/mcp/chat`, {
        message: content,
        history,
      })

      const data = response.data
      const toolCalls: ToolCall[] = data.tool_calls || []

      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: data.response,
        toolCalls,
        timestamp: new Date(),
      }

      setMessages(prev => [...prev, assistantMessage])
      setHistory(data.history || [])
    } catch (err) {
      setError('Une erreur est survenue. Veuillez réessayer.')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }, [history])

  const clearMessages = useCallback(() => {
    setMessages([])
    setHistory([])
    setError(null)
  }, [])

  return { messages, isLoading, error, sendMessage, clearMessages }
}
