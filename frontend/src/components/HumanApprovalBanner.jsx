import React from 'react'
import { ShieldAlert, CheckCircle2, ArrowRight, UserCheck, AlertTriangle } from 'lucide-react'

export default function HumanApprovalBanner({ state, formUrl, onApprove, isApproved }) {
  if (state !== 'WAITING_FOR_APPROVAL' && !isApproved) return null

  return (
    <div className={`rounded-2xl p-6 border shadow-2xl transition-all duration-500 ${
      isApproved 
        ? 'bg-emerald-950/40 border-emerald-500/50 shadow-emerald-500/10'
        : 'bg-gradient-to-r from-amber-950/50 via-slate-900 to-amber-950/50 border-amber-500/60 shadow-amber-500/15 animate-glow'
    }`}>
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-2xl">
          <div className="flex items-center gap-2.5">
            {isApproved ? (
              <div className="p-2 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                <CheckCircle2 className="w-6 h-6" />
              </div>
            ) : (
              <div className="p-2 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/30 animate-bounce">
                <ShieldAlert className="w-6 h-6" />
              </div>
            )}
            <div>
              <span className={`text-xs uppercase font-extrabold tracking-wider px-2.5 py-0.5 rounded-full ${
                isApproved ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
              }`}>
                {isApproved ? 'Human Verified & Approved' : 'Mandatory Human Approval Checkpoint'}
              </span>
              <h3 className="text-xl font-bold text-white mt-1">
                {isApproved ? 'Application Cleared for Candidate Review' : 'Application Prepared. Review Required Before Final Submission.'}
              </h3>
            </div>
          </div>

          <p className="text-xs text-slate-300 leading-relaxed pl-1">
            {isApproved 
              ? 'You have approved the pre-filled parameters. Open the target application form to perform final inspection and manual submission.'
              : 'Our strict safety boundary ensures no agent submits applications automatically. All safe fields are pre-filled, and sensitive credentials remain protected in your control.'}
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3 w-full md:w-auto shrink-0">
          {!isApproved ? (
            <button
              onClick={onApprove}
              className="px-6 py-3.5 rounded-xl bg-gradient-to-r from-amber-500 to-emerald-500 hover:from-amber-600 hover:to-emerald-600 text-slate-950 font-black text-sm shadow-lg shadow-amber-500/20 transition transform active:scale-95 flex items-center justify-center gap-2"
            >
              <UserCheck className="w-4 h-4" />
              <span>Review & Approve Readiness</span>
            </button>
          ) : (
            <a
              href={formUrl || 'http://localhost:8000/demo-portal/apply'}
              target="_blank"
              rel="noopener noreferrer"
              className="px-6 py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-black text-sm shadow-lg shadow-emerald-500/20 transition transform active:scale-95 flex items-center justify-center gap-2"
            >
              <span>Open Pre-filled Portal</span>
              <ArrowRight className="w-4 h-4" />
            </a>
          )}
        </div>
      </div>
    </div>
  )
}