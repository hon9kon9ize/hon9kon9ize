module.exports = {
  extends: [
    'eslint-config-custom'
  ],
  env: {
    browser: true,
    es6: true,
    jest: true
  },
  globals: {
    Atomics: 'readonly',
    SharedArrayBuffer: 'readonly'
  },
  parserOptions: {
    project: './tsconfig.json',
    tsconfigRootDir: __dirname,
  },
  settings: {
    tailwindcss: {
      callees: [
        'cn'
      ],
      config: 'tailwind.config.js'
    }
  },
  rules: {
    'unicorn/filename-case': 'off',
    "@next/next/no-img-element": "off"
  }
}