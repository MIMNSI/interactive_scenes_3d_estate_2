import * as http from 'node:http';
import * as https from 'node:https';
import * as fs from 'node:fs';
import * as path from 'node:path';

const args = process.argv.slice(2);
const option = (name, fallback) => {
  const index = args.indexOf(name);
  return index < 0 ? fallback : args[index + 1];
};
const directory = path.resolve(option('-d', './build/demo'));
const host = option('-h', '0.0.0.0');
const port = Number(option('-p', '8080'));
const tlsPort = Number(option('--https-port', '8081'));
const mime = {
  '.html': 'text/html', '.htm': 'text/html', '.js': 'text/javascript',
  '.css': 'text/css', '.json': 'application/json', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp',
  '.svg': 'image/svg+xml', '.wasm': 'application/wasm'
};

async function handle(request, response) {
  response.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
  response.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    let file = path.resolve(directory, '.' + pathname);
    if (file !== directory && !file.startsWith(directory + path.sep)) {
      response.writeHead(403).end('Forbidden');
      return;
    }
    let stats = await fs.promises.stat(file);
    if (stats.isDirectory()) {
      file = path.join(file, 'index.html');
      stats = await fs.promises.stat(file);
    }
    response.writeHead(200, {
      'Content-Type': mime[path.extname(file)] || 'application/octet-stream',
      'Content-Length': stats.size,
      'Cache-Control': 'no-store'
    });
    if (request.method === 'HEAD') response.end();
    else fs.createReadStream(file).on('error', () => response.destroy()).pipe(response);
  } catch (error) {
    response.writeHead(error.code === 'ENOENT' || error.code === 'ENOTDIR' ? 404 : 500);
    response.end('File unavailable');
  }
}

http.createServer(handle).listen(port, host, () => {
  console.log(`Local viewer: http://localhost:${port}/1209_Brown.html`);
});
https.createServer({
  key: fs.readFileSync('./certification/cert.key'),
  cert: fs.readFileSync('./certification/cert.pem')
}, handle).listen(tlsPort, host, () => {
  console.log(`HTTPS viewer: https://localhost:${tlsPort}/1209_Brown.html (requires a trusted, valid certificate)`);
});
