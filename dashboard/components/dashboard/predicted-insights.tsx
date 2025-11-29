"use client"

import { Brain, Sparkles, Clock, AlertCircle, TrendingDown } from "lucide-react"

const insights = [
  {
    text: "Salary delayed by 2 days based on pattern analysis",
    icon: Clock,
    type: "info",
  },
  {
    text: "Overspend risk this week - ₹4,200 above budget",
    icon: AlertCircle,
    type: "warning",
  },
  {
    text: "Shortfall expected on 14th - ₹3,500 gap predicted",
    icon: TrendingDown,
    type: "alert",
  },
]

const typeStyles = {
  info: { icon: "text-blue-400", bg: "bg-blue-500/5" },
  warning: { icon: "text-yellow-400", bg: "bg-yellow-500/5" },
  alert: { icon: "text-red-400", bg: "bg-red-500/5" },
}

export function PredictedInsights() {
  return (
    <div className="glass-card rounded-xl p-5">
      <div className="flex items-center gap-2 mb-4">
        <div className="p-1.5 rounded-lg bg-gradient-to-br from-purple-500/20 to-blue-500/20">
          <Brain className="w-4 h-4 text-purple-400" />
        </div>
        <h3 className="text-lg font-semibold text-foreground">AI Insights</h3>
        <Sparkles className="w-4 h-4 text-purple-400 animate-pulse" />
      </div>

      <div className="space-y-3">
        {insights.map((insight, index) => {
          const styles = typeStyles[insight.type as keyof typeof typeStyles]
          return (
            <div key={index} className={`p-3 rounded-lg ${styles.bg} border border-white/5 flex items-start gap-3`}>
              <insight.icon className={`w-4 h-4 ${styles.icon} mt-0.5 shrink-0`} />
              <p className="text-sm text-foreground/90 leading-relaxed">{insight.text}</p>
            </div>
          )
        })}
      </div>

      <div className="mt-4 p-3 rounded-lg bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/20">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          <span className="text-xs text-muted-foreground">AI Analysis Updated</span>
          <span className="text-xs text-foreground ml-auto">2 mins ago</span>
        </div>
      </div>
    </div>
  )
}
