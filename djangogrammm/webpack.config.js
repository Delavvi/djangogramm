'use strict'
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const autoprefixer = require('autoprefixer');

module.exports = {
    mode: 'development',
    entry: './assets/scripts/register.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'polls', 'static')
    },
    devServer: {
    static: path.resolve(__dirname, 'dist'),
    port: 8080,
    hot: true
  },
    module: {
        rules:[
        {
            test: /\.(scss)$/,
            use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader']
        }
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
        filename: 'register.css',
        }),
    ]
}