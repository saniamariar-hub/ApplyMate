import React from 'react'
import { CheckCircle2, Circle, Clock, ShieldAlert, Sparkles, Globe, FileText, Check, AlertCircle } from 'lucide-react'

export default function WorkflowProgress({ state, progressPct, logs = [] }) {
  const steps = [
    { id: 'NAVIGATING_WEBSITE', label: 'Website Opened', desc: 'Webcmd 0.7.4 Inspection', icon: Globe },
    { id: 'EXTRACTING_REQUIREMENTS', label: 'Analysis Complete', desc: 'Requirements Extracted', icon: Sparkles },
    { id: 'CHECKING_DOCUMENTS', label: 'Documents Checked', desc: 'Vault Match Verified', icon: FileText },
    { id: 'PREPARING_APPLICATION', label: 'Application Prepared', desc: 'Safe Fields Populated', icon: CheckCircle2 },
    { id: 'WAITING_FOR_APPROVAL', label: 'Waiting for Human Approval', desc: 'Manual Review Required', icon: ShieldAlert },
  ]

  const getStepStatus = (stepId, index) => {
    if (state === 'APPROVED_BY_USER') return 'COMPLETED'
    
    const stepOrder = [
      'NAVIGATING_WEBSITE',
      'EXTRACTING_REQUIREMENTS',
      'CHECKING_DOCUMENTS',
      'PREPARING_APPLICATION',
      'WAITING_FOR_APPROVAL'
    ]
    const currentIndex = stepOrder.indexOf(state)
    
    if (currentIndex === -1) {
      if (state === 'INITIALIZED') return index === 0 ? 'ACTIVE' : 'PENDING'
      return 'PENDING'
    }
    
    if (index < currentIndex) return 'COMPLETED'
    if (index === currentIndex) return state === 'WAITING_FOR_APPROVAL' ? 'APPROVAL_REQUIRED' : 'ACTIVE'
    return 'PENDING'
  }

  const getStatusSummary = () => {
    if (state === 'APPROVED_BY_USER') return '100% Complete • Approved by Candidate'
    if (state === 'WAITING_FOR_APPROVAL') return 'Application Prepared • Waiting for Human Approval (90%)'
    if (state === 'PREPARING_APPLICATION') return 'Application Prepared (85%)'
    if (state === 'CHECKING_DOCUMENTS') return 'Documents Checked (75%)'
    if (state === 'EXTRACTING_REQUIREMENTS') return 'Analysis Complete (55%)'
    if (state === 'NAVIGATING_WEBSITE') return 'Website Opened (15%)'
    return `${progressPct}% In Progress`
  }

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2.5">
          <div className="w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse" />
          <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300">Live Agent Pipeline</h3>
        </div>
        <span className={`text-xs font-mono font-semibold px-2.5 py-1 rounded-full border ${
          state === 'APPROVED_BY_USER'
            ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
            : state === 'WAITING_FOR_APPROVAL'
            ? 'bg-amber-500/10 text-amber-400 border-amber-500/20'
            : 'bg-blue-500/10 text-blue-400 border-blue-500/20'
        }`}>
          {getStatusSummary()}
        </span>
      </div>

      {/* Progress Track */}
      <div className="w-full bg-slate-800/80 rounded-full h-2 mb-6 overflow-hidden">
        <div 
          className={`h-2 rounded-full transition-all duration-500 ease-out ${
            state === 'APPROVED_BY_USER'
              ? 'bg-gradient-to-r from-blue-500 via-indigo-500 to-emerald-400'
              : 'bg-gradient-to-r from-blue-500 to-amber-400'
          }`}
          style={{ width: `${state === 'APPROVED_BY_USER' ? 100 : Math.min(progressPct, 90)}%` }}
        />
      </div>

      {/* Step Pills */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {steps.map((step, idx) => {
          const status = getStepStatus(step.id, idx)
          const Icon = step.icon

          return (
            <div 
              key={step.id}
              className={`p-3.5 rounded-xl border transition-all duration-300 flex flex-col justify-between ${
                status === 'COMPLETED'
                  ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-300'
                  : status === 'APPROVAL_REQUIRED'
                  ? 'bg-amber-950/40 border-amber-500/60 text-amber-300 shadow-lg shadow-amber-500/10'
                  : status === 'ACTIVE'
                  ? 'bg-blue-950/40 border-blue-500/50 text-blue-300 animate-pulse'
                  : 'bg-slate-900/40 border-slate-800/60 text-slate-500'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className={`p-1.5 rounded-lg ${
                  status === 'COMPLETED' ? 'bg-emerald-500/20 text-emerald-400' :
                  status === 'APPROVAL_REQUIRED' ? 'bg-amber-500/20 text-amber-400' :
                  status === 'ACTIVE' ? 'bg-blue-500/20 text-blue-400' : 'bg-slate-800 text-slate-500'
                }`}>
                  <Icon className="w-4 h-4" />
                </div>
                {status === 'COMPLETED' && <Check className="w-4 h-4 text-emerald-400" />}
                {status === 'APPROVAL_REQUIRED' && <AlertCircle className="w-4 h-4 text-amber-400 animate-bounce" />}
                {status === 'ACTIVE' && <div className="w-2 h-2 rounded-full bg-blue-400 animate-ping" />}
              </div>
              <div>
                <div className="text-xs font-bold leading-tight">{step.label}</div>
                <div className="text-[10px] text-slate-400 mt-0.5 truncate">{step.desc}</div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}