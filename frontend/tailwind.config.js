/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.{vue,js,ts}",
    "./pages/**/*.{vue,js,ts}",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', 'system-ui', 'sans-serif'],
      },
      colors: {
        pricetravelBlue: "#0047BB",
        pricetravelPink: "#E6007E",
        pricetravelPurple: "#662D91",
        pricetravelCyan: "#00AEEF",
        pricetravelYellow: "#FBB03B",
      },
    },
  },
  plugins: [],
}
