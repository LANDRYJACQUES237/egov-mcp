export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  toolCalls?: ToolCall[]
  timestamp: Date
}

export interface ToolCall {
  tool: string
  input: Record<string, unknown>
  status: 'success' | 'error'
  error?: string
}

export interface ChatResponse {
  request_id: string
  response: string
  tool_calls: ToolCall[]
  history: HistoryMessage[]
}

export interface HistoryMessage {
  role: string
  content: string
}
