'use client'

import React, { createContext, useContext, useState } from 'react'

interface TooltipContextType {
  showTooltip: (content: string, x: number, y: number) => void
  hideTooltip: () => void
}

const TooltipContext = createContext<TooltipContextType | undefined>(undefined)

export function TooltipProvider({ children }: { children: React.ReactNode }) {
  const [tooltip, setTooltip] = useState<{
    content: string
    x: number
    y: number
    visible: boolean
  }>({
    content: '',
    x: 0,
    y: 0,
    visible: false,
  })

  const showTooltip = (content: string, x: number, y: number) => {
    setTooltip({ content, x, y, visible: true })
  }

  const hideTooltip = () => {
    setTooltip(prev => ({ ...prev, visible: false }))
  }

  return (
    <TooltipContext.Provider value={{ showTooltip, hideTooltip }}>
      {children}
      {tooltip.visible && (
        <div
          className="fixed z-50 px-2 py-1 text-sm text-white bg-gray-900 rounded shadow-lg pointer-events-none"
          style={{
            left: tooltip.x + 10,
            top: tooltip.y - 10,
          }}
        >
          {tooltip.content}
        </div>
      )}
    </TooltipContext.Provider>
  )
}

export function useTooltip() {
  const context = useContext(TooltipContext)
  if (context === undefined) {
    throw new Error('useTooltip must be used within a TooltipProvider')
  }
  return context
}
