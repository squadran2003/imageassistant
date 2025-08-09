const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: 'dist',
  publicPath: '/static/',

  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title = "ImageAssistant - AI Image Generation Tool | Create Stunning AI Art";
        return args;
      });
  }
})
