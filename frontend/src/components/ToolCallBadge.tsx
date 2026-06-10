import { CheckCircle, XCircle, Zap } from 'lucide-react'
import type { ToolCall } from '../types'

const TOOL_LABELS: Record<string, string> = {
  search_companies: 'Recherche entreprises',
  get_tax_calendar: 'Calendrier fiscal',
  validate_cnps_number: 'Validation CNPS',
  calculate_social_contributions: 'Cotisations sociales',
  get_public_datasets: 'Datasets publics',
}

interface Props {
  toolCalls: ToolCall[]
}

export function ToolCallBadge({ toolCalls }: Props) {
  if (!toolCalls || toolCalls.length === 0) return null

  return (
    <div className="flex flex-wrap gap-2 mb-2">
      {toolCalls.map((tc, i) => (
        <div
          key={i}
          className={`flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full font-medium border ${
            tc.status === 'success'
              ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
              : 'bg-red-50 text-red-700 border-red-200'
          }`}
        >
          <Zap size={11} />
          {TOOL_LABELS[tc.tool] || tc.tool}
          {tc.status === 'success'
            ? <CheckCircle size={11} />
            : <XCircle size={11} />
          }
        </div>
      ))}
    </div>
  )
}
