import React from 'react'
import { Award, Clock, CheckCircle, AlertTriangle, XCircle, Calendar, ExternalLink, GraduationCap, Building2 } from 'lucide-react'

export default function EligibilityCard({ data }) {
  if (!data) return null

  const { program_info = {}, deadline = {}, eligibility_evaluation = {}, application_steps = [], important_conditions = [] } = data
  const overallStatus = eligibility_evaluation?.overall_status || 'ELIGIBLE'
  const matchPct = eligibility_evaluation?.match_score_percentage || 100
  const criteria = eligibility_evaluation?.criteria_evaluations || []

  const getStatusBadge = (st) => {
    switch (st) {
      case 'ELIGIBLE':
      case 'MATCH':
        return { bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400', icon: CheckCircle, text: 'Eligible / Matched' }
      case 'NEEDS_VERIFICATION':
      case 'WARNING':
        return { bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400', icon: AlertTriangle, text: 'Review Required' }
      case 'NOT_ELIGIBLE':
      case 'FAIL':
        return { bg: 'bg-rose-500/10 border-rose-500/30 text-rose-400', icon: XCircle, text: 'Not Eligible' }
      default:
        return { bg: 'bg-blue-500/10 border-blue-500/30 text-blue-400', icon: CheckCircle, text: st }
    }
  }

  const badge = getStatusBadge(overallStatus)
  const BadgeIcon = badge.icon

  return (
    <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl backdrop-blur-sm space-y-6">
      {/* Header Info */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-5">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
              {program_info.type || 'Scholarship'}
            </span>
            <span className="text-xs text-slate-400 flex items-center gap-1">
              <Building2 className="w-3 h-3" /> {program_info.organization || 'Hosting Institution'}
            </span>
          </div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            {program_info.name || 'Opportunity Overview'}
          </h2>
          <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
            {program_info.description}
          </p>
        </div>

        {/* Overall Status Badge */}
        <div className={`p-4 rounded-xl border flex items-center gap-3 self-start md:self-auto ${badge.bg}`}>
          <BadgeIcon className="w-7 h-7 shrink-0" />
          <div>
            <div className="text-xs uppercase font-extrabold tracking-wider">{badge.text}</div>
            <div className="text-lg font-black">{matchPct}% Match</div>
          </div>
        </div>
      </div>

      {/* Deadline & Urgency */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
            <Calendar className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Submission Deadline</div>
            <div className="text-sm font-bold text-white">{deadline.date || deadline.raw_text || 'October 15, 2026'}</div>
            <div className="text-[11px] text-amber-400 font-medium">{deadline.raw_text}</div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <GraduationCap className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Target Level</div>
            <div className="text-sm font-bold text-white">Undergraduate (Junior / Senior)</div>
            <div className="text-[11px] text-slate-400">Full-Time Enrollment</div>
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <Award className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Award Coverage</div>
            <div className="text-sm font-bold text-white">Tuition & Research Mentorship</div>
            <div className="text-[11px] text-emerald-400 font-medium">Up to $15,000 USD</div>
          </div>
        </div>
      </div>

      {/* Criterion Breakdown Table */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2">
          <span>Detailed Eligibility Verification</span>
          <span className="text-[11px] text-slate-500 font-normal">({criteria.length} criteria evaluated)</span>
        </h4>

        <div className="space-y-2">
          {criteria.map((c, i) => {
            const itemBadge = getStatusBadge(c.status)
            const ItemIcon = itemBadge.icon
            return (
              <div key={i} className="p-3.5 rounded-xl bg-slate-950/50 border border-slate-800/80 hover:border-slate-700 transition flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs">
                <div className="space-y-1 max-w-md">
                  <div className="font-bold text-slate-200">{c.criterion}</div>
                  <div className="text-[11px] text-slate-400">Requirement: <span className="text-slate-300">{c.requirement}</span></div>
                </div>

                <div className="flex items-center gap-3 justify-between md:justify-end">
                  <div className="text-right">
                    <div className="text-[11px] text-slate-400">Candidate Vault:</div>
                    <div className="font-semibold text-slate-200">{c.candidate_value}</div>
                  </div>
                  <span className={`px-2.5 py-1 rounded-lg border font-bold flex items-center gap-1.5 shrink-0 ${itemBadge.bg}`}>
                    <ItemIcon className="w-3.5 h-3.5" />
                    {c.status}
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Application Steps & Conditions */}
      {application_steps.length > 0 && (
        <div className="grid md:grid-cols-2 gap-4 pt-2 border-t border-slate-800">
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">Application Steps</h4>
            <ul className="space-y-1.5 text-xs text-slate-400">
              {application_steps.map((step, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-blue-400 font-bold shrink-0">{idx + 1}.</span>
                  <span>{step}</span>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">Key Program Conditions</h4>
            <ul className="space-y-1.5 text-xs text-slate-400">
              {important_conditions.map((cond, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="text-amber-400 font-bold shrink-0">•</span>
                  <span>{cond}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}