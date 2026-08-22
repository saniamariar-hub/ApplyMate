import React from 'react'
import { FileCheck, FileX, AlertCircle, FileText, UploadCloud, FolderCheck } from 'lucide-react'

export default function DocumentReadinessCard({ data }) {
  if (!data) return null

  const { readiness_score = 0, status = 'INCOMPLETE', summary = '', document_items = [] } = data

  const getStatusBadge = (st) => {
    switch (st) {
      case 'READY':
        return { bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400', icon: FileCheck, label: 'Vault Ready' }
      case 'ATTENTION_NEEDED':
        return { bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400', icon: AlertCircle, label: 'Review Draft' }
      case 'MISSING':
      default:
        return { bg: 'bg-rose-500/10 border-rose-500/30 text-rose-400', icon: FileX, label: 'Missing' }
    }
  }

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm space-y-5">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <FolderCheck className="w-5 h-5 text-indigo-400" />
            <h3 className="text-lg font-bold text-white">Document Vault Cross-Match</h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">{summary}</p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <div className="text-[11px] text-slate-400 uppercase font-semibold">Vault Readiness</div>
            <div className="text-lg font-black text-emerald-400">{readiness_score}% Ready</div>
          </div>
          <div className="w-12 h-12 rounded-full border-4 border-slate-800 flex items-center justify-center relative">
            <div 
              className="absolute inset-0 rounded-full border-4 border-emerald-500 border-t-transparent animate-spin-slow"
              style={{ transform: `rotate(${readiness_score * 3.6}deg)` }}
            />
            <span className="text-xs font-bold text-white">{readiness_score}%</span>
          </div>
        </div>
      </div>

      {/* Document Items List */}
      <div className="space-y-2.5">
        {document_items.map((doc, idx) => {
          const badge = getStatusBadge(doc.match_status)
          const BadgeIcon = badge.icon

          return (
            <div 
              key={idx}
              className="p-3.5 rounded-xl bg-slate-950/50 border border-slate-800/80 hover:border-slate-700 transition flex flex-col md:flex-row md:items-center justify-between gap-3"
            >
              <div className="flex items-start gap-3">
                <div className="p-2 rounded-lg bg-slate-900 border border-slate-800 text-slate-400 shrink-0 mt-0.5">
                  <FileText className="w-4 h-4 text-blue-400" />
                </div>
                <div>
                  <div className="text-xs font-bold text-slate-200 flex items-center gap-2">
                    {doc.required_name}
                    {doc.mandatory && (
                      <span className="text-[10px] uppercase px-1.5 py-0.5 rounded bg-rose-500/10 text-rose-400 border border-rose-500/20">
                        Mandatory
                      </span>
                    )}
                  </div>
                  <div className="text-[11px] text-slate-400 mt-0.5">
                    {doc.matched_file ? (
                      <span className="text-emerald-400/90 font-mono">Matched: {doc.matched_file}</span>
                    ) : (
                      <span className="text-slate-500">{doc.notes}</span>
                    )}
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-2 self-end md:self-auto">
                <span className={`px-2.5 py-1 rounded-lg border text-xs font-bold flex items-center gap-1.5 ${badge.bg}`}>
                  <BadgeIcon className="w-3.5 h-3.5" />
                  {badge.label}
                </span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}