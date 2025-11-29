"use client"

import { useEffect, useState } from "react"
import { Wallet, TrendingUp, TrendingDown, PiggyBank } from "lucide-react"
import { getUser } from "@/lib/auth"

export function FinancialSummary() {
  const [financialData, setFinancialData] = useState({
    income: 75000,
    expenses: 50000,
    savings: 25000,
    savingsRate: 33.3,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      const user = getUser()
      if (!user) {
        setLoading(false)
        return
      }

      try {
        const response = await fetch(`/api/financial-data?phone=${encodeURIComponent(user.phone)}`)
        if (response.ok) {
          const data = await response.json()
          const savingsRate = data.income > 0 
            ? ((data.savings || 0) / data.income) * 100 
            : 0
          setFinancialData({
            income: data.income || 75000,
            expenses: data.expenses || 50000,
            savings: data.savings || 25000,
            savingsRate: savingsRate || 33.3,
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

  if (loading) {
    return (
      <div className="glass-card rounded-xl p-5">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-secondary rounded w-1/2"></div>
          <div className="grid grid-cols-4 gap-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-20 bg-secondary rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="glass-card rounded-xl p-5">
      <h3 className="text-lg font-semibold text-foreground mb-5">📊 Financial Summary</h3>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 bg-blue-500/10 rounded-xl border border-blue-500/20">
          <div className="flex items-center gap-2 mb-2">
            <Wallet className="w-4 h-4 text-blue-400" />
            <span className="text-xs text-muted-foreground">Monthly Income</span>
          </div>
          <p className="text-xl font-bold text-foreground neon-text-blue">
            ₹{financialData.income.toLocaleString()}
          </p>
          <p className="text-xs text-green-400 mt-1">+5.2%</p>
        </div>

        <div className="p-4 bg-green-500/10 rounded-xl border border-green-500/20">
          <div className="flex items-center gap-2 mb-2">
            <PiggyBank className="w-4 h-4 text-green-400" />
            <span className="text-xs text-muted-foreground">Savings</span>
          </div>
          <p className="text-xl font-bold text-foreground neon-text-green">
            ₹{financialData.savings.toLocaleString()}
          </p>
          <p className="text-xs text-green-400 mt-1">+10,000</p>
        </div>

        <div className="p-4 bg-purple-500/10 rounded-xl border border-purple-500/20">
          <div className="flex items-center gap-2 mb-2">
            <TrendingDown className="w-4 h-4 text-purple-400" />
            <span className="text-xs text-muted-foreground">Expenses</span>
          </div>
          <p className="text-xl font-bold text-foreground neon-text-purple">
            ₹{financialData.expenses.toLocaleString()}
          </p>
          <p className="text-xs text-red-400 mt-1">-5,000</p>
        </div>

        <div className="p-4 bg-teal-500/10 rounded-xl border border-teal-500/20">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-teal-400" />
            <span className="text-xs text-muted-foreground">Savings Rate</span>
          </div>
          <p className="text-xl font-bold text-foreground neon-text-teal">
            {financialData.savingsRate.toFixed(1)}%
          </p>
          <p className="text-xs text-green-400 mt-1">+2.5%</p>
        </div>
      </div>
    </div>
  )
}

