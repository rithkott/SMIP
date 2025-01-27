"use client"
 
import { Line, LineChart } from "recharts"
import { ChartConfig, ChartContainer } from "@/components/ui/chart"

const chartConfig = {
  desktop: {
    label: "Desktop",
    color: "#2563eb",
  },
  mobile: {
    label: "Mobile",
    color: "#60a5fa",
  },
} satisfies ChartConfig

const chartData = [
    { month: "January", desktop: 186, mobile: 80 },
    { month: "February", desktop: 305, mobile: 200 },
    { month: "March", desktop: 237, mobile: 120 },
    { month: "April", desktop: 73, mobile: 190 },
    { month: "May", desktop: 209, mobile: 130 },
    { month: "June", desktop: 214, mobile: 140 },
  ]

export async function Component() {
    return (
      <ChartContainer config={chartConfig} className="min-h-[200px] w-full">
        <LineChart accessibilityLayer data={chartData}>
          <Line dataKey="desktop" fill="var(--color-desktop)" radius={4} />
          <Line dataKey="mobile" fill="var(--color-mobile)" radius={4} />
        </LineChart>
      </ChartContainer>
    )
  }

export default function Trades(){
    return (
        <div>
            <h2>My Trades Page</h2>
            <Component/>
        </div>
    )
}

