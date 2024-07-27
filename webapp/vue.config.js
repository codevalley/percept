const { defineConfig } = require('@vue/cli-service')
module.exports = {
  chainWebpack: config => {
    const svgRule = config.module.rule('svg');

    svgRule.uses.clear();

    svgRule
      .use('vue-svg-loader')
      .loader('vue-svg-loader');
  },

  // to allow the app to read environment variables at runtime
  publicPath: process.env.PUBLIC_URL || '/'
};