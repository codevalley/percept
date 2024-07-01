const colors = require('tailwindcss/colors')

module.exports = {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2A2731',
          light: '#3C3844',
        },
        secondary: '#787885',
        accent: '#F6655A',
        neutral: {
          100: '#EEECF1',
          200: '#DDDAE3',
          300: '#9590A0',
          400: '#F1F2F4',
          500: '#F7F7F8',
        },
      },
      fontFamily: {
        sans: ['IBM Plex Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}