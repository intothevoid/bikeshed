const cssnano = require('cssnano');
const tailwindcss = require('tailwindcss');
const autoprefixer = require('autoprefixer');
const purgecss = require('@fullhuman/postcss-purgecss');

module.exports = {
  plugins: [
    tailwindcss,
    autoprefixer,
    ...(process.env.NODE_ENV === 'production'
      ? [purgecss({ content: ['./**/*.html', './**/*.svelte'] }), cssnano]
      : []),
  ],
};
