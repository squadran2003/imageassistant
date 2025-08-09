const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: 'dist',
  publicPath: process.env.NODE_ENV === 'production' 
    ? 'https://d203745bu6qd7u.cloudfront.net/static/' 
    : '/static/',
  
  chainWebpack: config => {
    config
      .plugin('html')
      .tap(args => {
        args[0].title = "ImageAssistant - AI Image Generation Tool | Create Stunning AI Art";
        return args;
      });
  }
})
