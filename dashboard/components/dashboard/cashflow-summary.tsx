"use client"

import { useEffect, useState } from "react"
import { TrendingUp, TrendingDown, ArrowUpRight, ArrowDownRight } from "lucide-react"
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip } from "recharts"
import { getUser } from "@/lib/auth"

const cashflowData = [
  { month: "Aug", inflow: 42000, outflow: 38000 },
  { month: "Sep", inflow: 48000, outflow: 41000 },
  { month: "Oct", inflow: 35000, outflow: 39000 },
  { month: "Nov", inflow: 52000, outflow: 44000 },
  { month: "Dec", inflow: 58000, outflow: 48000 },
  { month: "Jan", inflow: 45200, outflow: 42800 },
]

export function CashflowSummary() {
  const [financialData, setFinancialData] = useState({
    income: 75000,
    expenses: 50000,
    savings: 25000,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      const user = getUser()
      if (!user) return

      try {
        const response = await fetch(`/api/financial-data?phone=${encodeURIComponent(user.phone)}`)
        if (response.ok) {
          const data = await response.json()
          setFinancialData({
            income: data.income || 75000,
            expenses: data.expenses || 50000,
            savings: data.savings || 25000,
          })
        }
      } catch (error) {
        console.error("Failed to fetch financial data:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const currentInflow = financialData.income
  const currentOutflow = financialData.expenses
  const inflowTrend = 8.2
  const outflowTrend = -3.5

  return (
    <div className="glass-card rounded-xl p-5">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="text-lg font-semibold text-foreground">Cashflow Summary</h3>
          <p className="text-xs text-muted-foreground">January 2025</p>
        </div>
        <div className="flex gap-4">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-blue-500" />
            <span className="text-xs text-muted-foreground">Inflow</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-purple-500" />
            <span className="text-xs text-muted-foreground">Outflow</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-5">
        <div className="p-4 bg-blue-500/10 rounded-xl border border-blue-500/20">
          <div className="flex items-center justify-between mb-2">
            <TrendingUp className="w-5 h-5 text-blue-400" />
            <div className="flex items-center gap-1 text-green-400 text-xs">
              <ArrowUpRight className="w-3 h-3" />
              <span>+{inflowTrend}%</span>
            </div>
          </div>
          <p className="text-2xl font-bold text-foreground neon-text-blue">₹{currentInflow.toLocaleString()}</p>
          <p className="text-xs text-muted-foreground mt-1">Total Inflow</p>
        </div>

        <div className="p-4 bg-purple-500/10 rounded-xl border border-purple-500/20">
          <div className="flex items-center justify-between mb-2">
            <TrendingDown className="w-5 h-5 text-purple-400" />
            <div className="flex items-center gap-1 text-green-400 text-xs">
              <ArrowDownRight className="w-3 h-3" />
              <span>{outflowTrend}%</span>
            </div>
          </div>
          <p className="text-2xl font-bold text-foreground neon-text-purple">₹{currentOutflow.toLocaleString()}</p>
          <p className="text-xs text-muted-foreground mt-1">Total Outflow</p>
        </div>
      </div>

      <div className="h-48">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={cashflowData}>
            <defs>
              <linearGradient id="inflowGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="outflowGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#a855f7" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#a855f7" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis dataKey="month" stroke="rgba(255,255,255,0.3)" fontSize={11} tickLine={false} axisLine={false} />
            <YAxis
              stroke="rgba(255,255,255,0.3)"
              fontSize={11}
              tickLine={false}
              axisLine={false}
              tickFormatter={(v) => `₹${v / 1000}k`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "rgba(15, 20, 35, 0.95)",
                border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: "8px",
                boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
              }}
              labelStyle={{ color: "rgba(255,255,255,0.7)" }}
              formatter={(value: number) => [`₹${value.toLocaleString()}`, ""]}
            />
            <Area type="monotone" dataKey="inflow" stroke="#3b82f6" strokeWidth={2} fill="url(#inflowGradient)" />
            <Area type="monotone" dataKey="outflow" stroke="#a855f7" strokeWidth={2} fill="url(#outflowGradient)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
