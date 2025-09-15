/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'arcane': {
          'dark': '#0f0f23',
          'medium': '#1a1a2e', 
          'light': '#16213e',
          'accent': '#64ffda',
          'gold': '#ffd700',
          'purple': '#9d4edd',
          'blue': '#4cc9f0',
        }
      },
      fontFamily: {
        'magical': ['Cinzel', 'serif'],
        'code': ['Fira Code', 'monospace'],
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite alternate',
        'float': 'float 3s ease-in-out infinite',
        'magical-spin': 'magical-spin 4s linear infinite',
      },
      keyframes: {
        'pulse-glow': {
          '0%': { 
            boxShadow: '0 0 5px currentColor',
            transform: 'scale(1)',
          },
          '100%': { 
            boxShadow: '0 0 20px currentColor, 0 0 30px currentColor',
            transform: 'scale(1.05)',
          },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'magical-spin': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
    },
  },
  plugins: [],
}