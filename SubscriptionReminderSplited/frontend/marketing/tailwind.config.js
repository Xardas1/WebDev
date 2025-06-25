// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    fontFamily: {
      // pick whichever you want as the default!
      sans: ['Inter', 'sans-serif']
      // heading: ['Poppins', 'sans-serif'],   // optional second family
    },
    extend: {},
  },
  plugins: [],
};
