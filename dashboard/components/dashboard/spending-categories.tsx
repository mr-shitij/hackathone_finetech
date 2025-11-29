"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts"

const spendingData = [
  { name: "Food & Dining", value: 12500, color: "#3b82f6" },
  { name: "Travel", value: 8200, color: "#14b8a6" },
  { name: "Bills & Utilities", value: 9800, color: "#a855f7" },
  { name: "UPI Transfers", value: 6300, color: "#f59e0b" },
  { name: "Shopping", value: 6000, color: "#ec4899" },
]

export function SpendingCategories() {
  const total = spendingData.reduce((sum, item) => sum + item.value, 0)

  return (
    <div className="glass-card rounded-xl p-5">
      <h3 className="text-lg font-semibold text-foreground mb-4">Spending Categories</h3>

      <div className="flex items-center gap-4">
        <div className="relative w-32 h-32">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={spendingData}
                cx="50%"
                cy="50%"
                innerRadius={35}
                outerRadius={55}
                paddingAngle={3}
                dataKey="value"
                strokeWidth={0}
              >
                {spendingData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(15, 20, 35, 0.95)",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: "8px",
                }}
                formatter={(value: number) => [`₹${value.toLocaleString()}`, ""]}
              />
            </PieChart>
          </ResponsiveContainer>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center">
              <p className="text-lg font-bold text-foreground">₹{(total / 1000).toFixed(1)}k</p>
              <p className="text-[10px] text-muted-foreground">Total</p>
            </div>
          </div>
        </div>

        <div className="flex-1 space-y-2">
          {spendingData.map((item, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                <span className="text-xs text-muted-foreground">{item.name}</span>
              </div>
              <span className="text-xs font-medium text-foreground">₹{(item.value / 1000).toFixed(1)}k</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
