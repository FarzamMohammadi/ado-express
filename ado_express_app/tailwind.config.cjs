module.exports = {
  purge: {
    content: [
      './src/**/*.html',
      './src/**/*.svelte',
    ],
    options: {
      safelist: [/^bg-/, /^text-/, /^border-/, /^dark:/],
    },
  },
  darkMode: 'class',
};
