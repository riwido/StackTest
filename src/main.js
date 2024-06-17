const devMode = process.argv.includes('--dev');
require('./build')(devMode);
