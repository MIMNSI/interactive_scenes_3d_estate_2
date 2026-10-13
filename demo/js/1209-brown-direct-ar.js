(() => {
    document.addEventListener('DOMContentLoaded', () => {
        const button = document.getElementById('viewButton');
        const original = button.innerHTML;
        const label = document.createElement('span');
        button.replaceChildren(label);
        button.disabled = true;
        button.setAttribute('aria-busy', 'true');
        label.textContent = 'Preparing AR...';

        const status = document.createElement('p');
        status.setAttribute('role', 'status');
        status.style.cssText = 'margin:8px 16px 0;text-align:center;font-size:13px;color:var(--text-hi)';
        button.after(status);

        const frame = document.createElement('iframe');
        frame.title = 'SuperSplat AR';
        frame.allow = 'fullscreen; xr-spatial-tracking';
        frame.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;border:0;opacity:0;pointer-events:none;z-index:-1';
        const url = new URL('supersplat-viewer/direct-ar.html', location.href);
        url.searchParams.set('content', new URL('assets/data/1209_Brown/1209_Brown.ply', location.href).href);
        url.searchParams.set('webgl', '');
        url.searchParams.set('noui', '');
        frame.src = url.href;
        document.body.append(frame);

        let ready = false;
        let starting = false;
        let startTimer;
        const restore = () => {
            starting = false;
            clearTimeout(startTimer);
            frame.style.opacity = '0';
            frame.style.pointerEvents = 'none';
            frame.style.zIndex = '-1';
            button.disabled = !ready;
            button.setAttribute('aria-busy', 'false');
            button.innerHTML = original;
        };
        const loadTimer = setTimeout(() => {
            if (!ready) {
                button.setAttribute('aria-busy', 'false');
                label.textContent = 'AR unavailable';
                status.textContent = 'AR could not finish loading. Reload this page to try again.';
            }
        }, 120000);

        window.addEventListener('message', (event) => {
            if (event.origin !== location.origin || event.source !== frame.contentWindow || event.data?.type !== '1209-brown-ar') return;
            const { status: state, message } = event.data;
            if (state === 'ready') {
                clearTimeout(loadTimer);
                ready = true;
                restore();
                status.textContent = '';
            } else if (state === 'active') {
                clearTimeout(startTimer);
                frame.style.opacity = '1';
                frame.style.pointerEvents = 'auto';
                frame.style.zIndex = '10000';
            } else if (state === 'ended') {
                restore();
            } else if (state === 'unsupported' || state === 'error') {
                clearTimeout(loadTimer);
                restore();
                if (!ready) button.textContent = 'AR unavailable';
                status.textContent = message;
            }
        });

        button.addEventListener('click', () => {
            if (!ready || starting) return;
            starting = true;
            button.disabled = true;
            button.setAttribute('aria-busy', 'true');
            button.textContent = 'Opening camera...';
            status.textContent = '';
            startTimer = setTimeout(() => {
                restore();
                status.textContent = 'AR did not start. Please try again.';
            }, 30000);
            try {
                // Make the iframe renderable before handing its canvas to WebXR.
                // The parent's message loop may be throttled during immersive startup.
                frame.style.opacity = '1';
                frame.style.pointerEvents = 'auto';
                frame.style.zIndex = '10000';
                frame.contentWindow.startProductAR();
            } catch (error) {
                console.error(error);
                restore();
                status.textContent = 'Could not start AR. Please try again.';
            }
        });
    });
})();
