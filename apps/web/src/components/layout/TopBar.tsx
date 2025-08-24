import React from 'react'

export function TopBar() {
  return (
    <header className="h-16 bg-card border-b border-border flex items-center justify-between px-6">
      <div className="flex items-center space-x-4">
        <h1 className="text-xl font-semibold">My Next.js App</h1>
      </div>
      <div className="flex items-center space-x-4">
        {/* User menu and notifications will go here */}
      </div>
    </header>
  )
}
