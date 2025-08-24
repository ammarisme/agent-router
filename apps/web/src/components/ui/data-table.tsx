import React from 'react'
import { cn } from '@/lib/utils'

interface DataTableProps<T> {
  data: T[]
  columns: Array<{
    key: keyof T
    header: string
    render?: (value: T[keyof T], row: T) => React.ReactNode
  }>
  className?: string
}

export function DataTable<T>({ data, columns, className }: DataTableProps<T>) {
  return (
    <div className={cn("overflow-x-auto", className)}>
      <table className="w-full border-collapse border border-border">
        <thead>
          <tr className="bg-muted">
            {columns.map((column) => (
              <th
                key={String(column.key)}
                className="border border-border px-4 py-2 text-left font-medium"
              >
                {column.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex} className="hover:bg-muted/50">
              {columns.map((column) => (
                <td
                  key={String(column.key)}
                  className="border border-border px-4 py-2"
                >
                  {column.render
                    ? column.render(row[column.key], row)
                    : String(row[column.key] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
