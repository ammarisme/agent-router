import React from 'react'
import { cn } from '@/lib/utils'

interface StepperProps {
  steps: Array<{ title: string; description?: string }>
  currentStep: number
  onStepClick?: (step: number) => void
}

export function Stepper({ steps, currentStep, onStepClick }: StepperProps) {
  return (
    <div className="flex items-center space-x-4">
      {steps.map((step, index) => (
        <div key={index} className="flex items-center">
          <button
            onClick={() => onStepClick?.(index)}
            className={cn(
              "flex h-8 w-8 items-center justify-center rounded-full border-2 text-sm font-medium",
              index <= currentStep
                ? "border-primary bg-primary text-primary-foreground"
                : "border-muted-foreground text-muted-foreground"
            )}
          >
            {index + 1}
          </button>
          {index < steps.length - 1 && (
            <div className="h-0.5 w-8 bg-muted mx-2" />
          )}
        </div>
      ))}
    </div>
  )
}
