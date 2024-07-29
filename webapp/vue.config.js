const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  chainWebpack: config => {
    // SVG loader configuration
    const svgRule = config.module.rule('svg');
    svgRule.uses.clear();
    svgRule.use('vue-svg-loader').loader('vue-svg-loader');

    // HTML plugin configuration for injecting environment variables
    config
      .plugin('html')
      .tap(args => {
        args[0].VUE_APP_BASE_URL = process.env.VUE_APP_BASE_URL || '/'
        return args
      })
  },

  // Public path configuration
  publicPath: process.env.VUE_APP_BASE_URL || '/',

  // Dev server configuration
  devServer: {
    historyApiFallback: true,
    proxy: {
      '/v1': {
        target: process.env.VUE_APP_API_URL || 'http://localhost:5001',
        changeOrigin: true
      }
    }
  }
});