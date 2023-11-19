module.exports = {
  content: [
    "./web/web_app/templates/**/*.html",
    "./web/web_app/static/**/*.js",
    "./web/web_app/**/*.py",
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
