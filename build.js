import esbuild from "esbuild";
import { sassPlugin } from "esbuild-sass-plugin";
import babel from "esbuild-plugin-babel";
const args = process.argv.slice(2);

const pluginCache = new Map();
esbuild.build({
  entryPoints: [`${args[0]}`],
  outfile: `${args[1]}`,
  bundle: true,
  loader: {
    ".svg": "dataurl",
    '.png': 'dataurl',
    '.woff': 'dataurl',
    '.woff2': 'dataurl',
    '.eot': 'dataurl',
    '.ttf': 'dataurl',
  },
  plugins: [
    sassPlugin({
      implementation: "node-sass",
      cache: pluginCache,
    }),
    // babel({
    //   filter: /.*/,
    //   namespace: '',
    //   presets: ["@babel/preset-env", "@babel/preset-react"],
    //   plugins: [
    //     "transform-react-pug",
    //     "transform-react-jsx",
    //   ],
    // }),
  ],
});

