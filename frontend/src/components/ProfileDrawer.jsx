import React, { useState, useEffect } from 'react'
import { User, X, Save, Check, RefreshCw } from 'lucide-react'

export default function ProfileDrawer({ isOpen, onClose }) {
  const [profile, setProfile] = useState(null)
  const [isSaving, setIsSaving] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)

  useEffect(() => {
    if (isOpen) {
      fetch('/api/profile')
        .then(res => res.json())
        .then(data => setProfile(data))
        .catch(err => console.error('Error fetching profile:', err))
    }
  }, [isOpen])

  const handleSave = async () => {
    setIsSaving(true)
    try {
      const res = await fetch('/api/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ profile_data: profile })
      })
      if (res.ok) {
        setSaveSuccess(true)
        setTimeout(() => setSaveSuccess(false), 2000)
      }
    } catch (err) {
      console.error('Error saving profile:', err)
    } finally {
      setIsSaving(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-sm">
      <div className="w-full max-w-xl bg-slate-900 border-l border-slate-800 h-full p-6 overflow-y-auto flex flex-col justify-between shadow-2xl">
        <div className="space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
                <User className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-white">Student Demo Profile</h3>
                <p className="text-xs text-slate-400">Easily edit candidate credentials for demo testing</p>
              </div>
            </div>
            <button onClick={onClose} className="p-2 rounded-lg hover:bg-slate-800 text-slate-400 hover:text-white">
              <X className="w-5 h-5" />
            </button>
          </div>

          {profile ? (
            <div className="space-y-4 text-xs">
              {/* Personal Section */}
              <div className="space-y-3 p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <h4 className="font-bold uppercase tracking-wider text-slate-300">Personal Details</h4>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-slate-400 mb-1">Full Name</label>
                    <input 
                      type="text" 
                      value={profile.personal?.full_name || ''} 
                      onChange={e => setProfile({...profile, personal: {...profile.personal, full_name: e.target.value}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Email</label>
                    <input 
                      type="email" 
                      value={profile.personal?.email || ''} 
                      onChange={e => setProfile({...profile, personal: {...profile.personal, email: e.target.value}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Phone</label>
                    <input 
                      type="text" 
                      value={profile.personal?.phone || ''} 
                      onChange={e => setProfile({...profile, personal: {...profile.personal, phone: e.target.value}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Citizenship</label>
                    <input 
                      type="text" 
                      value={profile.personal?.citizenship || ''} 
                      onChange={e => setProfile({...profile, personal: {...profile.personal, citizenship: e.target.value}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                </div>
              </div>

              {/* Academic Section */}
              <div className="space-y-3 p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <h4 className="font-bold uppercase tracking-wider text-slate-300">Academic Background</h4>
                <div className="grid grid-cols-2 gap-3">
                  <div className="col-span-2">
                    <label className="block text-slate-400 mb-1">Institution</label>
                    <input 
                      type="text" 
                      value={profile.academic?.current_institution || ''} 
                      onChange={e => setProfile({...profile, academic: {...profile.academic, current_institution: e.target.value}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Degree</label>
                    <input 
                      type="text" 
                      value={profile.academic?.degree || 'B.Tech'} 
                      onChange={e => setProfile({...profile, academic: {...profile.academic, degree: e.target.value}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Current Year</label>
                    <input 
                      type="text" 
                      value={profile.academic?.current_year || 'Third Year'} 
                      onChange={e => setProfile({...profile, academic: {...profile.academic, current_year: e.target.value}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-slate-400 mb-1">Major</label>
                    <input 
                      type="text" 
                      value={profile.academic?.major || ''} 
                      onChange={e => setProfile({...profile, academic: {...profile.academic, major: e.target.value}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">Cumulative GPA</label>
                    <input 
                      type="number" 
                      step="0.01"
                      value={profile.academic?.gpa ?? 9.1} 
                      onChange={e => setProfile({...profile, academic: {...profile.academic, gpa: parseFloat(e.target.value)}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 mb-1">GPA Scale</label>
                    <input 
                      type="number" 
                      step="0.1"
                      value={profile.academic?.gpa_scale ?? 10.0} 
                      onChange={e => setProfile({...profile, academic: {...profile.academic, gpa_scale: parseFloat(e.target.value)}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500"
                    />
                  </div>
                </div>
              </div>

              {/* Financial Section */}
              <div className="space-y-3 p-4 rounded-xl bg-slate-950/60 border border-slate-800">
                <h4 className="font-bold uppercase tracking-wider text-slate-300">Financial Background</h4>
                <div>
                  <label className="block text-slate-400 mb-1">Annual Household Income (INR ₹)</label>
                  <div className="relative">
                    <input 
                      type="number" 
                      value={profile.financial?.annual_household_income_inr ?? 650000} 
                      onChange={e => setProfile({...profile, financial: {...profile.financial, annual_household_income_inr: parseInt(e.target.value)}})}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-white focus:outline-none focus:border-blue-500 font-mono"
                    />
                  </div>
                  <p className="text-[11px] text-slate-500 mt-1">
                    Equivalent: ~${Math.round((profile.financial?.annual_household_income_inr || 650000) / 83).toLocaleString()} USD / year
                  </p>
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-slate-500">Loading student profile...</div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="pt-4 border-t border-slate-800 flex justify-end gap-3">
          <button 
            onClick={onClose}
            className="px-4 py-2.5 rounded-lg border border-slate-700 text-slate-300 hover:bg-slate-800 text-xs font-semibold"
          >
            Cancel
          </button>
          <button 
            onClick={handleSave}
            disabled={isSaving}
            className="px-5 py-2.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold flex items-center gap-1.5 shadow-lg shadow-blue-500/20"
          >
            {saveSuccess ? <Check className="w-4 h-4 text-emerald-300" /> : <Save className="w-4 h-4" />}
            <span>{saveSuccess ? 'Saved!' : isSaving ? 'Saving...' : 'Save Changes'}</span>
          </button>
        </div>
      </div>
    </div>
  )
}