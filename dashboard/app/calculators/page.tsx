"use client"

import { AuthGuard } from "@/components/auth-guard"
import { DashboardHeader } from "@/components/dashboard/header"
import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import Link from "next/link"
import { Calculator, FileText, User, Home } from "lucide-react"
import { Button } from "@/components/ui/button"
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts"

export default function CalculatorsPage() {
  const [sipAmount, setSipAmount] = useState(5000)
  const [sipReturn, setSipReturn] = useState([12])
  const [sipYears, setSipYears] = useState([10])

  const [emiAmount, setEmiAmount] = useState(1000000)
  const [emiRate, setEmiRate] = useState([8.5])
  const [emiTenure, setEmiTenure] = useState([20])

  const calculateSIP = (monthly: number, rate: number, years: number) => {
    const monthlyRate = rate / 100 / 12
    const months = years * 12
    const totalInvestment = monthly * months

    if (monthlyRate === 0) {
      return {
        totalInvestment,
        estimatedReturns: 0,
        maturityValue: totalInvestment,
      }
    }

    const maturityValue =
      monthly *
      ((Math.pow(1 + monthlyRate, months) - 1) / monthlyRate) *
      (1 + monthlyRate)

    return {
      totalInvestment: Math.round(totalInvestment),
      estimatedReturns: Math.round(maturityValue - totalInvestment),
      maturityValue: Math.round(maturityValue),
    }
  }

  const calculateEMI = (principal: number, rate: number, tenureYears: number) => {
    const monthlyRate = rate / 100 / 12
    const months = tenureYears * 12

    if (monthlyRate === 0) {
      return {
        emi: Math.round(principal / months),
        totalInterest: 0,
        totalAmount: principal,
      }
    }

    const emi =
      (principal * monthlyRate * Math.pow(1 + monthlyRate, months)) /
      (Math.pow(1 + monthlyRate, months) - 1)

    const totalAmount = emi * months
    const totalInterest = totalAmount - principal

    return {
      emi: Math.round(emi),
      totalInterest: Math.round(totalInterest),
      totalAmount: Math.round(totalAmount),
    }
  }

  const sipResult = calculateSIP(sipAmount, sipReturn[0], sipYears[0])
  const emiResult = calculateEMI(emiAmount, emiRate[0], emiTenure[0])

  const sipChartData = [
    { name: "Investment", value: sipResult.totalInvestment },
    { name: "Returns", value: sipResult.estimatedReturns },
  ]

  const emiChartData = [
    { name: "Principal", value: emiAmount },
    { name: "Interest", value: emiResult.totalInterest },
  ]

  const COLORS = ["#3b82f6", "#a855f7"]

  return (
    <AuthGuard>
      <div className="min-h-screen bg-background p-4 lg:p-6">
        <div className="mx-auto max-w-7xl">
          <DashboardHeader />

          {/* Navigation */}
          <div className="mt-4 mb-6 flex gap-2">
            <Link href="/">
              <Button variant="ghost" size="sm">
                <Home className="w-4 h-4 mr-2" />
                Dashboard
              </Button>
            </Link>
            <Link href="/calculators">
              <Button variant="default" size="sm">
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

          <h1 className="text-3xl font-bold mb-6">🧮 Financial Calculators</h1>
          <p className="text-muted-foreground mb-8">
            Calculate your investments, loans, and tax estimates
          </p>

          <Tabs defaultValue="sip" className="space-y-6">
            <TabsList>
              <TabsTrigger value="sip">📈 SIP Calculator</TabsTrigger>
              <TabsTrigger value="emi">🏦 EMI Calculator</TabsTrigger>
              <TabsTrigger value="tax">💼 Tax Calculator</TabsTrigger>
            </TabsList>

            <TabsContent value="sip">
              <Card>
                <CardHeader>
                  <CardTitle>SIP Calculator</CardTitle>
                  <CardDescription>
                    Calculate returns on your Systematic Investment Plan
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-6">
                      <div className="space-y-2">
                        <Label>Monthly Investment (₹)</Label>
                        <Input
                          type="number"
                          value={sipAmount}
                          onChange={(e) => setSipAmount(Number(e.target.value))}
                          min={500}
                          max={1000000}
                          step={500}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>Expected Annual Return: {sipReturn[0]}%</Label>
                        <Slider
                          value={sipReturn}
                          onValueChange={setSipReturn}
                          min={1}
                          max={30}
                          step={1}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>Investment Period: {sipYears[0]} Years</Label>
                        <Slider
                          value={sipYears}
                          onValueChange={setSipYears}
                          min={1}
                          max={30}
                          step={1}
                        />
                      </div>
                    </div>
                    <div className="space-y-6">
                      <div className="grid grid-cols-3 gap-4">
                        <div className="p-4 bg-blue-500/10 rounded-lg">
                          <p className="text-xs text-muted-foreground mb-1">Total Investment</p>
                          <p className="text-xl font-bold">
                            ₹{sipResult.totalInvestment.toLocaleString()}
                          </p>
                        </div>
                        <div className="p-4 bg-green-500/10 rounded-lg">
                          <p className="text-xs text-muted-foreground mb-1">Estimated Returns</p>
                          <p className="text-xl font-bold">
                            ₹{sipResult.estimatedReturns.toLocaleString()}
                          </p>
                        </div>
                        <div className="p-4 bg-purple-500/10 rounded-lg">
                          <p className="text-xs text-muted-foreground mb-1">Maturity Value</p>
                          <p className="text-xl font-bold">
                            ₹{sipResult.maturityValue.toLocaleString()}
                          </p>
                        </div>
                      </div>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <PieChart>
                            <Pie
                              data={sipChartData}
                              cx="50%"
                              cy="50%"
                              innerRadius={60}
                              outerRadius={100}
                              dataKey="value"
                            >
                              {sipChartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                              ))}
                            </Pie>
                            <Tooltip />
                            <Legend />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="emi">
              <Card>
                <CardHeader>
                  <CardTitle>EMI Calculator</CardTitle>
                  <CardDescription>
                    Calculate your Equated Monthly Installment for loans
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-6">
                      <div className="space-y-2">
                        <Label>Loan Amount (₹)</Label>
                        <Input
                          type="number"
                          value={emiAmount}
                          onChange={(e) => setEmiAmount(Number(e.target.value))}
                          min={10000}
                          max={100000000}
                          step={50000}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>Interest Rate: {emiRate[0]}% per annum</Label>
                        <Slider
                          value={emiRate}
                          onValueChange={setEmiRate}
                          min={1}
                          max={20}
                          step={0.1}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label>Loan Tenure: {emiTenure[0]} Years</Label>
                        <Slider
                          value={emiTenure}
                          onValueChange={setEmiTenure}
                          min={1}
                          max={30}
                          step={1}
                        />
                      </div>
                    </div>
                    <div className="space-y-6">
                      <div className="grid grid-cols-3 gap-4">
                        <div className="p-4 bg-blue-500/10 rounded-lg">
                          <p className="text-xs text-muted-foreground mb-1">Monthly EMI</p>
                          <p className="text-xl font-bold">₹{emiResult.emi.toLocaleString()}</p>
                        </div>
                        <div className="p-4 bg-red-500/10 rounded-lg">
                          <p className="text-xs text-muted-foreground mb-1">Total Interest</p>
                          <p className="text-xl font-bold">
                            ₹{emiResult.totalInterest.toLocaleString()}
                          </p>
                        </div>
                        <div className="p-4 bg-purple-500/10 rounded-lg">
                          <p className="text-xs text-muted-foreground mb-1">Total Amount</p>
                          <p className="text-xl font-bold">
                            ₹{emiResult.totalAmount.toLocaleString()}
                          </p>
                        </div>
                      </div>
                      <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                          <PieChart>
                            <Pie
                              data={emiChartData}
                              cx="50%"
                              cy="50%"
                              innerRadius={60}
                              outerRadius={100}
                              dataKey="value"
                            >
                              {emiChartData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                              ))}
                            </Pie>
                            <Tooltip />
                            <Legend />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="tax">
              <Card>
                <CardHeader>
                  <CardTitle>Income Tax Calculator</CardTitle>
                  <CardDescription>Compare Old vs New tax regimes</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-12">
                    <p className="text-muted-foreground mb-4">
                      🚧 Advanced tax calculator coming soon!
                    </p>
                    <p className="text-sm text-muted-foreground">
                      For now, use our AI agent to get personalized tax advice.
                    </p>
                    <Link href="/">
                      <Button className="mt-4">📞 Talk to Tax Planning Agent</Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </AuthGuard>
  )
}

