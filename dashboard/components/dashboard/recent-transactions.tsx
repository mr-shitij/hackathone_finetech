"use client"

import { CreditCard, Smartphone, Banknote, ArrowUpRight, ArrowDownLeft } from "lucide-react"

const transactions = [
  {
    id: 1,
    merchant: "Swiggy",
    category: "Food & Dining",
    amount: -542,
    type: "UPI",
    icon: Smartphone,
    time: "Today, 2:34 PM",
    status: "completed",
  },
  {
    id: 2,
    merchant: "Salary Credit",
    category: "Income",
    amount: 45200,
    type: "NEFT",
    icon: Banknote,
    time: "Today, 9:00 AM",
    status: "completed",
  },
  {
    id: 3,
    merchant: "Amazon",
    category: "Shopping",
    amount: -2499,
    type: "Card",
    icon: CreditCard,
    time: "Yesterday, 6:12 PM",
    status: "completed",
  },
  {
    id: 4,
    merchant: "Electricity Bill",
    category: "Bills",
    amount: -1850,
    type: "UPI",
    icon: Smartphone,
    time: "Yesterday, 11:30 AM",
    status: "completed",
  },
  {
    id: 5,
    merchant: "ATM Withdrawal",
    category: "Cash",
    amount: -5000,
    type: "ATM",
    icon: Banknote,
    time: "23 Jan, 4:45 PM",
    status: "completed",
  },
]

const typeColors = {
  UPI: "bg-teal-500/20 text-teal-400",
  Card: "bg-purple-500/20 text-purple-400",
  NEFT: "bg-blue-500/20 text-blue-400",
  ATM: "bg-yellow-500/20 text-yellow-400",
}

export function RecentTransactions() {
  return (
    <div className="glass-card rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-foreground">Recent Transactions</h3>
        <button className="text-xs text-blue-400 hover:text-blue-300 transition-colors">View All</button>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-white/5">
              <th className="text-left py-3 px-2 text-xs font-medium text-muted-foreground">Merchant</th>
              <th className="text-left py-3 px-2 text-xs font-medium text-muted-foreground">Type</th>
              <th className="text-left py-3 px-2 text-xs font-medium text-muted-foreground">Time</th>
              <th className="text-right py-3 px-2 text-xs font-medium text-muted-foreground">Amount</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((tx) => (
              <tr key={tx.id} className="border-b border-white/5 hover:bg-white/5 transition-colors">
                <td className="py-3 px-2">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${tx.amount > 0 ? "bg-green-500/10" : "bg-secondary/50"}`}>
                      <tx.icon className={`w-4 h-4 ${tx.amount > 0 ? "text-green-400" : "text-muted-foreground"}`} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-foreground">{tx.merchant}</p>
                      <p className="text-xs text-muted-foreground">{tx.category}</p>
                    </div>
                  </div>
                </td>
                <td className="py-3 px-2">
                  <span className={`text-xs px-2 py-1 rounded-full ${typeColors[tx.type as keyof typeof typeColors]}`}>
                    {tx.type}
                  </span>
                </td>
                <td className="py-3 px-2">
                  <span className="text-xs text-muted-foreground">{tx.time}</span>
                </td>
                <td className="py-3 px-2 text-right">
                  <div className="flex items-center justify-end gap-1">
                    {tx.amount > 0 ? (
                      <ArrowDownLeft className="w-3 h-3 text-green-400" />
                    ) : (
                      <ArrowUpRight className="w-3 h-3 text-red-400" />
                    )}
                    <span className={`text-sm font-medium ${tx.amount > 0 ? "text-green-400" : "text-foreground"}`}>
                      {tx.amount > 0 ? "+" : ""}₹{Math.abs(tx.amount).toLocaleString()}
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
