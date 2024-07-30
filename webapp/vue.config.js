const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  chainWebpack: config => {
    // Existing SVG configuration
    const svgRule = config.module.rule('svg');
    svgRule.uses.clear();
    svgRule.use('vue-svg-loader').loader('vue-svg-loader');

    // Add CopyWebpackPlugin
    config.plugin('copy').use(CopyWebpackPlugin, [
      {
        patterns: [
          {
            from: 'public',
            to: '',
            globOptions: {
              ignore: ['.DS_Store'],
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