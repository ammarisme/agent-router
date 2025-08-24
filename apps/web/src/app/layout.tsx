import React from 'react'
import '@/styles/globals.css'
import { ApiProvider } from '@/providers/ApiProvider'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <ApiProvider>
          {children}
        </ApiProvider>
      </body>
    </html>
  )
}
