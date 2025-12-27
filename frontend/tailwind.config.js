/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        simulation: {
          vehicle: {
            normal: '#3b82f6',
            emergency: '#ef4444',
            bus: '#10b981',
            truck: '#8b5cf6',
          },
          trafficLight: {
            green: '#22c55e',
            yellow: '#eab308',
            red: '#ef4444',
          },
          road: {
            normal: '#94a3b8',
            congested: '#f59e0b',
            free: '#22c55e',
          }
        }
      },
      screens: {
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px',
      }
    },
  },
  plugins: [],
};
