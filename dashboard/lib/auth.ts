"use client"

export interface User {
  phone: string
  name: string
}

export function isAuthenticated(): boolean {
  if (typeof window === "undefined") return false
  return localStorage.getItem("authenticated") === "true"
}

export function getUser(): User | null {
  if (typeof window === "undefined") return null
  const userStr = localStorage.getItem("user")
  if (!userStr) return null
  try {
    return JSON.parse(userStr)
  } catch {
    return null
  }
}

export function logout(): void {
  if (typeof window === "undefined") return
  localStorage.removeItem("authenticated")
  localStorage.removeItem("user")
}

export function setUser(user: User): void {
  if (typeof window === "undefined") return
  localStorage.setItem("user", JSON.stringify(user))
  localStorage.setItem("authenticated", "true")
}

