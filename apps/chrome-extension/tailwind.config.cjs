/* eslint-disable import/no-unresolved, global-require, import/no-extraneous-dependencies */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./src/**/*.html"],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        'space-mono': ['"Space Mono"', 'monospace'],
      },
    },
  },
  variants: {},
  plugins: [require("@tailwindcss/typography"), require("tailwindcss-animate"), require("@tailwindcss/forms")],
};
