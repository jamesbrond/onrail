const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
    module: {
        rules: [{
            test: /\.css$/,
            use: [
                { loader: MiniCssExtractPlugin.loader },
                { loader: 'css-loader', options: { importLoaders: 1 } }
            ]
        }]
    },
    externals: {
        jquery: 'jQuery',
        $: 'jQuery'
    },
    entry: './src/web/index.js',
    output: {
        filename: 'cal.js'
    },
    resolve: {
        extensions: [ '.js' ],
    },
    target: 'web',
    plugins: [
        new MiniCssExtractPlugin({filename: 'style.css'})
    ]
};
