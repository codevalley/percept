const { defineConfig } = require('@vue/cli-service')
const CopyWebpackPlugin = require('copy-webpack-plugin')

module.exports = defineConfig({
  chainWebpack: config => {
    // Existing SVG configuration
    const svgRule = config.module.rule('svg');
    svgRule.uses.clear();
    svgRule.use('vue-svg-loader').loader('vue-svg-loader');

    // Remove the existing copy plugin if it exists
    config.plugins.delete('copy');

    // Add a new copy plugin configuration
    const CopyWebpackPlugin = require('copy-webpack-plugin')
    config.plugin('copy').use(CopyWebpackPlugin, [
      {
        patterns: [
          {
            from: 'public',
            to: '',
            globOptions: {
              ignore: ['**/index.html'], // Ignore index.html to prevent conflict
            },
          },
        ],
      },
    ]);
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