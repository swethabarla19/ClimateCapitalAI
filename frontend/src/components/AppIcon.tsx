interface AppIconProps {
  name:
    | 'explore'
    | 'plan'
    | 'benchmark'
    | 'methodology'
    | 'help'
    | 'sparkle'
    | 'map'
    | 'layers'
  size?: number
}

export function AppIcon({ name, size = 20 }: AppIconProps) {
  const common = {
    width: size,
    height: size,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 1.8,
    strokeLinecap: 'round' as const,
    strokeLinejoin: 'round' as const,
    'aria-hidden': true,
  }

  if (name === 'explore') {
    return (
      <svg {...common}>
        <circle cx="12" cy="12" r="8" />
        <path d="m15.5 8.5-2.1 4.9-4.9 2.1 2.1-4.9 4.9-2.1Z" />
      </svg>
    )
  }

  if (name === 'plan') {
    return (
      <svg {...common}>
        <rect x="5" y="4" width="14" height="16" rx="2" />
        <path d="M9 4.5V3m6 1.5V3M8.5 9h7M8.5 13h5M8.5 17h3" />
      </svg>
    )
  }

  if (name === 'benchmark') {
    return (
      <svg {...common}>
        <path d="M4 19V9m5 10V5m5 14v-7m5 7V3" />
        <path d="M3 19.5h18" />
      </svg>
    )
  }

  if (name === 'methodology') {
    return (
      <svg {...common}>
        <path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5v-15Z" />
        <path d="M4 20.5A2.5 2.5 0 0 1 6.5 18H20M8 7h8m-8 4h6" />
      </svg>
    )
  }

  if (name === 'help') {
    return (
      <svg {...common}>
        <circle cx="12" cy="12" r="9" />
        <path d="M9.8 9a2.4 2.4 0 1 1 3.5 2.15c-.85.45-1.3.9-1.3 1.85m0 3.3v.2" />
      </svg>
    )
  }

  if (name === 'sparkle') {
    return (
      <svg {...common}>
        <path d="M12 2.5c.7 4.7 2.8 6.8 7.5 7.5-4.7.7-6.8 2.8-7.5 7.5-.7-4.7-2.8-6.8-7.5-7.5C9.2 9.3 11.3 7.2 12 2.5Z" />
        <path d="M19 16.5c.25 1.45 1.05 2.25 2.5 2.5-1.45.25-2.25 1.05-2.5 2.5-.25-1.45-1.05-2.25-2.5-2.5 1.45-.25 2.25-1.05 2.5-2.5Z" />
      </svg>
    )
  }

  if (name === 'layers') {
    return (
      <svg {...common}>
        <path d="m12 3 9 5-9 5-9-5 9-5Z" />
        <path d="m3 12 9 5 9-5M3 16l9 5 9-5" />
      </svg>
    )
  }

  return (
    <svg {...common}>
      <path d="M4 6.5 9 4l6 2.5L20 4v13.5L15 20l-6-2.5L4 20V6.5Z" />
      <path d="M9 4v13.5M15 6.5V20" />
    </svg>
  )
}
