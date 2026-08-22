import React, { useState, useEffect } from 'react'
import { 
  Sparkles, Globe, ShieldCheck, ArrowRight, RefreshCw, User, CheckCircle2, 
  Search, Play, AlertCircle, Compass, Layers
} from 'lucide-react'

import WorkflowProgress from './components/WorkflowProgress'
import EligibilityCard from './components/EligibilityCard'
import DocumentReadinessCard from './components/DocumentReadinessCard'
import ApplicationFormPreview from './components/ApplicationFormPreview'
import HumanApprovalBanner from './components/HumanApprovalBanner'
import ProfileDrawer from './components/ProfileDrawer'
import LiveLogsViewer from './components/LiveLogsViewer'

export default function App() {
  const [url, setUrl] = useState('http://localhost:8000/demo-portal')
  const [programName, setProgramName] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [workflowState, setWorkflowState] = useState(null)
  const [isApproved, setIsApproved] = useState(false)
  const [isProfileOpen, setIsProfileOpen] = useState(false)
  const [presets, setPresets] = useState([])
  const [candidateName, setCandidateName] = useState('Aarohi Nair')

  useEffect(() => {
    fetch('/api/presets')
      .then(res => res.json())
      .then(data => setPresets(data))
      .catch(() => {})

    fetch('/api/profile')
      .then(res => res.json())
      .then(p => {
        if (p?.personal?.full_name) {
          setCandidateName(p.personal.full_name)
        }
      })
      .catch(() => {})
  }, [])

  const startAnalysis = async () => {
    if (!url.trim()) return
    setIsRunning(true)
    setIsApproved(false)
    setWorkflowState(null)

    try {
      const response = await fetch('/api/workflow/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url.trim(), program_name: programName.trim() })
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.substring(6))
              setWorkflowState(data)
              if (data.state === 'APPROVED_BY_USER') {
                setIsApproved(true)
              }
            } catch (err) {
              console.error('Error parsing SSE data:', err)
            }
          }
        }
      }
    } catch (error) {
      console.error('Workflow error:', error)
    } finally {
      setIsRunning(false)
    }
  }

  const handleApprove = async () => {
    if (!workflowState?.workflow_id) return
    try {
      const res = await fetch(`/api/workflow/approve/${workflowState.workflow_id}`, { method: 'POST' })
      const data = await res.json()
      if (res.ok && data.ok) {
        setIsApproved(true)
        if (data.workflow) {
          setWorkflowState(data.workflow)
        }
      }
    } catch (err) {
      console.error('Approval failed:', err)
    }
  }

  const selectPreset = (preset) => {
    setUrl(preset.url)
    setProgramName(preset.name)
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between">
      {/* Navigation Header */}
      <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-base tracking-tight text-white">Application Readiness Agent</span>
                <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  Webcmd 0.7.4
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Autonomous Browser Copilot for Scholarships, Internships & Grants</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setIsProfileOpen(true)}
              className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs font-semibold text-slate-300 hover:text-white flex items-center gap-2 transition"
            >
              <User className="w-4 h-4 text-blue-400" />
              <span>Student Vault ({candidateName})</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Body */}
      <main className="max-w-7xl mx-auto px-6 py-8 space-y-8 flex-1 w-full">
        {/* Input & Preset Launcher Card */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-3xl p-6 shadow-2xl backdrop-blur-sm space-y-5">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                <Compass className="w-5 h-5 text-blue-400" />
                <span>Opportunity Target Configuration</span>
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                Enter any public opportunity website URL or select a built-in live demo target.
              </p>
            </div>

            {/* Quick Pick Presets */}
            {presets.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {presets.map(p => (
                  <button
                    key={p.id}
                    onClick={() => selectPreset(p)}
                    className={`px-3 py-1.5 rounded-lg border text-xs font-semibold transition ${
                      url === p.url 
                        ? 'bg-blue-600/20 border-blue-500/40 text-blue-300' 
                        : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {p.name.split(' ')[0]} {p.name.split(' ')[1]}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-2 space-y-1.5">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Opportunity Website URL</label>
              <div className="relative">
                <Globe className="w-4 h-4 text-slate-500 absolute left-3.5 top-3.5" />
                <input
                  type="text"
                  value={url}
                  onChange={e => setUrl(e.target.value)}
                  placeholder="https://example.org/scholarship-2026"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-3 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400">Program / Opportunity Hint</label>
              <input
                type="text"
                value={programName}
                onChange={e => setProgramName(e.target.value)}
                placeholder="Global STEM Fellowship 2026"
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-xs text-white focus:outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={startAnalysis}
              disabled={isRunning || !url.trim()}
              className="px-7 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-blue-500/25 transition transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isRunning ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-blue-200" />
                  <span>Agent Executing Pipeline...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 text-blue-200 fill-blue-200" />
                  <span>Analyze Application Readiness</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Real-time Agent Progress */}
        {workflowState && (
          <WorkflowProgress 
            state={workflowState.state} 
            progressPct={workflowState.progress_pct} 
            logs={workflowState.logs} 
          />
        )}

        {/* Human Approval Checkpoint Banner */}
        {workflowState && (
          <HumanApprovalBanner 
            state={workflowState.state} 
            formUrl={workflowState.application_data?.form_url}
            onApprove={handleApprove}
            isApproved={isApproved}
          />
        )}

        {/* Main Analysis Results Grid */}
        {workflowState && (
          <div className="space-y-8">
            {/* Eligibility & Program Details */}
            {workflowState.eligibility_data && (
              <EligibilityCard data={workflowState.eligibility_data} />
            )}

            {/* Document Vault & Form Preparation Side-by-Side */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {workflowState.document_data && (
                <DocumentReadinessCard data={workflowState.document_data} />
              )}
              {workflowState.application_data && (
                <ApplicationFormPreview data={workflowState.application_data} />
              )}
            </div>

            {/* Execution Trace & Diagnostic Terminal */}
            <LiveLogsViewer logs={workflowState.logs} />
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-6 text-center text-xs text-slate-500">
        <p>Application Readiness Agent • Hackathon MVP Edition • Powered by Webcmd 0.7.4 & OpenAI</p>
      </footer>

      {/* Student Profile Drawer */}
      <ProfileDrawer 
        isOpen={isProfileOpen} 
        onClose={() => setIsProfileOpen(false)} 
      />
    </div>
  )
}