import React, { useState } from 'react'
import { Terminal, ChevronDown, ChevronUp } from 'lucide-react'

export default function LiveLogsViewer({ logs = [] }) {
  const [isExpanded, setIsExpanded] = useState(false)

  const getStatusColor = (st) => {
    switch (st) {
      case 'SUCCESS': return 'text-emerald-400'
      case 'RUNNING': return 'text-blue-400'
      case 'APPROVAL_REQUIRED': return 'text-amber-400 font-bold'
      case 'ERROR': return 'text-rose-400'
      default: return 'text-slate-400'
    }
  }

  return (
    <div className="bg-slate-950/80 border border-slate-800/80 rounded-2xl overflow-hidden shadow-xl">
      <button 
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full px-6 py-3.5 flex items-center justify-between text-xs font-mono font-bold text-slate-400 hover:text-slate-200 bg-slate-900/50 hover:bg-slate-900/80 transition"
      >
        <div className="flex items-center gap-2">
          <Terminal className="w-4 h-4 text-blue-400" />
          <span>Agent Execution Trace & Webcmd Diagnostic Logs ({logs.length} events)</span>
        </div>
        {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
      </button>

      {isExpanded && (
        <div className="p-4 max-h-64 overflow-y-auto space-y-2 font-mono text-[11px] bg-slate-950">
          {logs.map((log, idx) => (
            <div key={idx} className="flex items-start gap-2.5 leading-relaxed">
              <span className="text-slate-600 shrink-0">[{log.timestamp}]</span>
              <span className="px-1.5 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800 text-[10px] shrink-0 font-bold">
                {log.stage}
              </span>
              <span className={getStatusColor(log.status)}>
                {log.message}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}