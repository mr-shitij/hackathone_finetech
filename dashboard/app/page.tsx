"use client"

import { DashboardHeader } from "@/components/dashboard/header"
import { CashflowSummary } from "@/components/dashboard/cashflow-summary"
import { FinancialSummary } from "@/components/dashboard/financial-summary"
import { SpendingCategories } from "@/components/dashboard/spending-categories"
import { UpcomingRisks } from "@/components/dashboard/upcoming-risks"
import { PredictedInsights } from "@/components/dashboard/predicted-insights"
import { RecentTransactions } from "@/components/dashboard/recent-transactions"
import { AAConsentStatus } from "@/components/dashboard/aa-consent-status"
import { AIVoiceCoach } from "@/components/dashboard/ai-voice-coach"
import { UserSnapshot } from "@/components/dashboard/user-snapshot"
import { EventTimeline } from "@/components/dashboard/event-timeline"
import { AuthGuard } from "@/components/auth-guard"
import Link from "next/link"
import { Calculator, FileText, User } from "lucide-react"
import { Button } from "@/components/ui/button"

export default function DashboardPage() {
  return (
    <AuthGuard>
      <div className="min-h-screen bg-background p-4 lg:p-6">
        <div className="mx-auto max-w-[1800px]">
          <DashboardHeader />

          {/* Navigation */}
          <div className="mt-4 mb-6 flex gap-2">
            <Link href="/">
              <Button variant="default" size="sm">📊 Dashboard</Button>
            </Link>
            <Link href="/calculators">
              <Button variant="ghost" size="sm">
                <Calculator className="w-4 h-4 mr-2" />
                Calculators
              </Button>
            </Link>
            <Link href="/reports">
              <Button variant="ghost" size="sm">
                <FileText className="w-4 h-4 mr-2" />
                Reports
              </Button>
            </Link>
            <Link href="/profile">
              <Button variant="ghost" size="sm">
                <User className="w-4 h-4 mr-2" />
                Profile
              </Button>
            </Link>
          </div>

          <div className="mt-6 grid grid-cols-12 gap-4 lg:gap-5">
            {/* Left Column */}
            <div className="col-span-12 lg:col-span-3 space-y-4 lg:space-y-5">
              <UserSnapshot />
              <AAConsentStatus />
              <AIVoiceCoach />
            </div>

            {/* Middle Column */}
            <div className="col-span-12 lg:col-span-6 space-y-4 lg:gap-5">
              <FinancialSummary />
              <CashflowSummary />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-5">
                <SpendingCategories />
                <PredictedInsights />
              </div>
              <RecentTransactions />
            </div>

            {/* Right Column */}
            <div className="col-span-12 lg:col-span-3 space-y-4 lg:space-y-5">
              <UpcomingRisks />
              <EventTimeline />
            </div>
          </div>
        </div>
      </div>
    </AuthGuard>
  )
}
