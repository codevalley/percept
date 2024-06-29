/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],

  theme: {
    extend: {
      fontFamily: {
        sans: ['IBM Plex Sans', 'sans-serif'],
      },
      colors: {
        'custom-gray': {
          100: '#F7F7F8',
          200: '#F1F2F4',
          300: '#EEECF1',
          400: '#DDDAE3',
          500: '#9590A0',
          600: '#787885',
          700: '#2A2731',
        },
      },
    },
  },
  plugins: [
    require('daisyui'),
  ],
}