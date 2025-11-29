"use client"

import { Bell, Settings, Search, Sparkles, LogOut } from "lucide-react"
import { useRouter } from "next/navigation"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { getUser, logout } from "@/lib/auth"
import { useEffect, useState } from "react"

export function DashboardHeader() {
  const router = useRouter()
  const [user, setUser] = useState<{ phone: string; name: string } | null>(null)

  useEffect(() => {
    setUser(getUser())
  }, [])

  const handleLogout = () => {
    logout()
    router.push("/login")
  }

  const initials = user?.name
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2) || "U"

  return (
    <header className="glass-card rounded-xl px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-teal-400 flex items-center justify-center glow-blue">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-foreground neon-text-blue">FinanceBot</h1>
            <p className="text-xs text-muted-foreground">AI Financial Advisor</p>
          </div>
        </div>
      </div>

      <div className="hidden md:flex items-center gap-2 glass-card rounded-lg px-4 py-2 min-w-[300px]">
        <Search className="w-4 h-4 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search transactions, insights..."
          className="bg-transparent border-none outline-none text-sm text-foreground placeholder:text-muted-foreground flex-1"
        />
        <kbd className="text-xs text-muted-foreground bg-secondary px-2 py-0.5 rounded">⌘K</kbd>
      </div>

      <div className="flex items-center gap-3">
        <Button variant="ghost" size="icon" className="relative">
          <Bell className="w-5 h-5 text-muted-foreground" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full animate-pulse" />
        </Button>
        <Button variant="ghost" size="icon" onClick={handleLogout} title="Logout">
          <LogOut className="w-5 h-5 text-muted-foreground" />
        </Button>
        <Avatar className="w-9 h-9 ring-2 ring-blue-500/30">
          <AvatarImage src="/indian-professional-man.png" />
          <AvatarFallback className="bg-gradient-to-br from-blue-500 to-purple-500 text-white text-sm">
            {initials}
          </AvatarFallback>
        </Avatar>
      </div>
    </header>
  )
}
