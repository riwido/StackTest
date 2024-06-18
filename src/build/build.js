// Original: https://github.com/kirjavascript/leaderboard/blob/master/src/build.js
const copyStaticFiles = require('esbuild-copy-static-files');
const esbuild = require('esbuild');
const path = require('path');
const devMode = process.argv.includes('--dev');

function buildPackage() {
    const config = {
        outdir: './src/stacktest/static/',
        entryPoints: {
            main: './src/webclient/main.jsx',
        },
        bundle: true,
        minify: !devMode,
        platform: 'browser',
        // format: 'iife',
        // metafile: true,
        banner: {
            js: `'use strict';\n`,
        },
        plugins: [
            statsPlugin(),
            // require('esbuild-plugin-solid').solidPlugin(),
            // require('esbuild-sass-plugin').sassPlugin(),
            copyStaticFiles({
                src: './static',
                dest: './src/stacktest/static/',
            }),
        ],
        //loader: {
        //    '.ttf': 'file',
        //},
        define: {
            __DEV__: String(devMode),
        },
    };

    if (devMode) {
        esbuild
            .context(config)
            .then((ctx) => ctx.watch())
            .catch(console.error);
    } else {
        esbuild.build(config).catch(console.error);
    }
}

function statsPlugin() {
    return {
        name: 'stats',
        setup(build) {
            build.onStart(() => console.time('build time'));
            build.onEnd((result) => {
                if (result.metafile) {
                    Object.entries(result.metafile.outputs).forEach(
                        ([file, { bytes }]) => {
                            const relPath = path.relative(process.cwd(), file);

                            const i = Math.floor(
                                Math.log(bytes) / Math.log(1024),
                            );
                            const humanBytes =
                                (bytes / Math.pow(1024, i)).toFixed(2) * 1 +
                                ['B', 'kB', 'MB', 'GB', 'TB'][i];
                            console.info(relPath, humanBytes);
                        },
                    );
                } else {
                    if ('errors' in result) {
                        console.info(
                            `build failed with ${result.errors.length} errors, ${result.warnings.length} warnings`,
                        );
                    } else {
                        console.error(result);
                    }
                }
                console.timeEnd('build time');
            });
        },
    };
}


buildPackage()
