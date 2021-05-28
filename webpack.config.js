var debug = process.env.NODE_ENV !== "production";
var webpack = require('webpack');
var path = require('path');
const { CleanWebpackPlugin } = require("clean-webpack-plugin")

module.exports = {
    context: path.join(__dirname, "assets"),
    entry: "./src/js/go-react.js",
    module: {
        rules: [{
            test: /\.jsx?$/,
            exclude: /node_modules/,
            use: [{
                loader: 'babel-loader',
                options: {
                    presets: ['@babel/preset-react', '@babel/preset-env']
                }
            }]
        }]
    },
    output: {
        path: path.join(__dirname + "/assets/js/"),
        filename: "go-react.min.js"
    },
    plugins: debug ? [] : [
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
    ],
    mode: "development"
};