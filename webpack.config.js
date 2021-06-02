var debug = process.env.NODE_ENV !== "production";
var webpack = require('webpack');
var path = require('path');
const { CleanWebpackPlugin } = require("clean-webpack-plugin")

module.exports = {
    mode: "development",
    context: path.resolve(__dirname, "assets"),
    entry: path.resolve(__dirname, './assets/src/js/app.tsx'),
    output: {
        path: path.resolve(__dirname + "/assets/js/"),
        filename: "go-react.min.js"
    },
    devtool: "cheap-module-source-map",
    resolve: {
        extensions: ['.js', ".ts", ".tsx", ".json"]
    },
    module: {
        rules: [{
            test: /\.tsx?$/,
            exclude: /node_modules/,
            use: [{
                loader: 'ts-loader',

            }]
        }]
    },
    plugins: debug ? [] : [
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.optimize.UglifyJsPlugin({ mangle: false, sourcemap: false }),
    ],
};