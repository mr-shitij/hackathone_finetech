"use client"

import { CheckCircle2, RefreshCw, Shield } from "lucide-react"

export function AAConsentStatus() {
  return (
    <div className="glass-card rounded-xl p-5">
      <div className="flex items-center gap-2 mb-4">
        <Shield className="w-5 h-5 text-teal-400" />
        <h3 className="font-semibold text-foreground">AA Consent Status</h3>
      </div>

      <div className="flex items-center gap-4">
        <div className="p-3 rounded-xl bg-green-500/10 border border-green-500/20 glow-teal">
          <CheckCircle2 className="w-8 h-8 text-green-400" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="text-lg font-semibold text-green-400 neon-text-teal">Active</span>
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          </div>
          <p className="text-xs text-muted-foreground mt-1">All 8 accounts linked</p>
        </div>
      </div>

      <div className="mt-4 p-3 rounded-lg bg-secondary/30 flex items-center justify-between">
        <div>
          <p className="text-xs text-muted-foreground">Last Sync</p>
          <p className="text-sm font-medium text-foreground">Today, 10:45 AM</p>
        </div>
        <button className="p-2 rounded-lg bg-teal-500/10 hover:bg-teal-500/20 transition-colors group">
          <RefreshCw className="w-4 h-4 text-teal-400 group-hover:animate-spin" />
        </button>
      </div>

      <div className="mt-3 grid grid-cols-4 gap-2">
        {["SBI", "HDFC", "ICICI", "+5"].map((bank, i) => (
          <div key={i} className="p-2 rounded-lg bg-secondary/20 text-center">
            <span className="text-xs font-medium text-muted-foreground">{bank}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
