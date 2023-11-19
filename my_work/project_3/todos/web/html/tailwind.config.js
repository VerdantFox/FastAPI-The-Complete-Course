module.exports = {
  content: [
    "./web/html/templates/**/*.html",
    "./web/html/static/**/*.js",
    "./web/html/**/*.py",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Roboto", "sans-serif"],
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
