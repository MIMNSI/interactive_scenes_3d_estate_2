import { main } from './index.js';

const report = (status, message = '') => {
    parent.postMessage({ type: '1209-brown-ar', status, message }, location.origin);
};

const fail = (error) => {
    console.error('SuperSplat AR:', error);
    report('error', 'Could not start AR. Please try again.');
};

window.addEventListener('unhandledrejection', (event) => fail(event.reason));

try {
    const supported = navigator.xr && await navigator.xr.isSessionSupported('immersive-ar');
    if (!supported) {
        report('unsupported', 'AR is unavailable in this browser. Try Chrome on an AR-supported Android phone.');
    } else {
        const { config, settings } = window.sse;
        config.contents = config.contents.then((response) => {
            if (!response.ok) throw new Error(`Model download failed: ${response.status}`);
            return response;
        });
        let firstFrame = false;
        window.firstFrame = () => {
            firstFrame = true;
            report('ready');
        };
        const viewer = await main(document.getElementById('application-canvas'), await settings, config);
        const { app, events } = viewer.global;
        app.xr.on('start', () => report('active'));
        app.xr.on('end', () => report('ended'));
        app.xr.on('error', fail);
        // Called synchronously by the parent click; no navigation or async hop.
        window.startProductAR = () => {
            if (!firstFrame) throw new Error('The AR model is not ready.');
            if (app.xr.active) return;
            if (!app.xr.isAvailable('immersive-ar')) {
                throw new Error('An immersive AR session is not available.');
            }
            app.renderNextFrame = true;
            events.fire('startAR');
        };
    }
} catch (error) {
    fail(error);
}
