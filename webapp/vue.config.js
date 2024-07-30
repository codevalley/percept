const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  chainWebpack: config => {
    // Existing SVG configuration
    const svgRule = config.module.rule('svg');
    svgRule.uses.clear();
    svgRule.use('vue-svg-loader').loader('vue-svg-loader');

    // Ensure images are being processed
    const imageRule = config.module.rule('images')
    imageRule.uses.clear()
    imageRule.use('url-loader')
      .loader('url-loader')
      .options({
        limit: 4096, // This means files smaller than 4kb will be inlined, larger will be copied to the output directory
        fallback: {
          loader: 'file-loader',
          options: {
            name: 'img/[name].[hash:8].[ext]'
          }
        }
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