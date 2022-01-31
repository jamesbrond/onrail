const webpack = require('webpack');
const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = {
	mode: 'development',
	module: {
		rules: [
			{
        test: /\.css$/,
        use: [
          { loader: MiniCssExtractPlugin.loader },
          { loader: 'css-loader', options: { importLoaders: 1 } }
        ]
      }
		]
	},
	externals: {
		jquery: 'jQuery',
		$: 'jQuery'
	},
	entry: './web/index.js',
	output: {
		path: path.resolve(__dirname, 'dist'),
		filename: 'cal.js'
	},
	resolve: {
    extensions: [ '.js' ]
  },
	target: 'web',
	plugins: [
    new MiniCssExtractPlugin({
      filename: 'style.css'
    })
  ]
};
