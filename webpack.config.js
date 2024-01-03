const path = require('path');

module.exports = {
    module: {
        rules: [
            {
                test: /\.s[ac]ss$/i,
                use: [
                  "style-loader",
                  "css-loader",
                  "sass-loader",
                ]
              }
            ]
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
        extensions: [ '.js', '.scss' ],
    },
    target: 'web',
};
