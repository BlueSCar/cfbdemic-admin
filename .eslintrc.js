module.exports = {
    root: true,
    env: {
      node: true
    },
    extends: [
      'plugin:vue/essential',
      '@vue/airbnb'
    ],
    rules: {
      'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
      'comma-dangle': ['error', 'never'],
      'indent': 'off',
      'linebreak-style': ['warn', 'windows'],
      'no-tabs': 'off',
      'no-restricted-syntax': 'off',
      'max-len': 'off',
      'no-plusplus': 'off'
    },
    parserOptions: {
      parser: 'babel-eslint'
    },
  };
