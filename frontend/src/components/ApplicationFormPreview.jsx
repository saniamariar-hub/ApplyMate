import React from 'react'
import { ShieldCheck, ShieldAlert, CheckCircle2, AlertTriangle, ExternalLink, Lock } from 'lucide-react'

export default function ApplicationFormPreview({ data }) {
  if (!data) return null

  const { form_url = '', safe_fields_filled = [], sensitive_fields_skipped = [], safety_checkpoint = '' } = data

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <h3 className="text-lg font-bold text-white">Browser Form Preparation</h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Webcmd navigated and populated safe non-sensitive inputs. Submission is guarded.
          </p>
        </div>

        {form_url && (
          <a 
            href={form_url} 
            target="_blank" 
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-500/10 text-blue-400 hover:bg-blue-500/20 border border-blue-500/20 text-xs font-semibold transition"
          >
            <span>Inspect Live Form</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </a>
        )}
      </div>

      {/* Safe Fields Populated */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>Safe Fields Populated ({safe_fields_filled.length})</span>
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
          {safe_fields_filled.map((field, idx) => (
            <div key={idx} className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 flex justify-between items-center text-xs">
              <span className="text-slate-400 font-mono capitalize">{field.field.replace(/_/g, ' ')}:</span>
              <span className="font-semibold text-slate-200 truncate max-w-[200px]" title={field.value}>
                {field.value}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Sensitive Fields Protected */}
      <div className="space-y-3 pt-2">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <Lock className="w-4 h-4 text-amber-400" />
          <span>Protected Sensitive Fields (Intentionally Excluded)</span>
        </h4>

        <div className="space-y-2">
          {sensitive_fields_skipped.map((sens, idx) => (
            <div key={idx} className="p-3 rounded-xl bg-amber-950/20 border border-amber-500/20 flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-amber-400" />
                <span className="font-bold text-amber-200">{sens.field}</span>
              </div>
              <span className="text-[11px] text-amber-400/80">{sens.reason}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}