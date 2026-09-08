const dollarFormatter = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
})

export function formatDollars(value: number): string {
  return dollarFormatter.format(value)
}

const compactNumberFormatter = new Intl.NumberFormat('en-US', {
  maximumFractionDigits: 2,
})

export function formatCompactDollars(value: number): string {
  if (Math.abs(value) >= 1_000_000_000) {
    return `$${compactNumberFormatter.format(value / 1_000_000_000)}B`
  }

  if (Math.abs(value) >= 1_000_000) {
    return `$${compactNumberFormatter.format(value / 1_000_000)}M`
  }

  return formatDollars(value)
}

export function formatFundingPriority(value: number): string {
  return Number.isInteger(value) ? String(value) : value.toFixed(1)
}
