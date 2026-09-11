(() => {
  const VIEW_BUTTON_ID = 'viewButton';
  const VIEWER_PATH = 'supersplat-viewer/index.html';

  const findSplatUrl = () => {
    for (const script of document.scripts) {
      const match = script.textContent.match(/addSplatScene\s*\(\s*(['"`])([^'"`]+?\.ply)\1/);
      if (match) return new URL(match[2], window.location.href);

      const dynamic = script.textContent.match(/(?:let|const|var)\s+path\s*=\s*([\x27\x22])([^\x27\x22]+)\1\s*\+[^;]+?\+\s*([\x27\x22])([^\x27\x22]*?\.ply)\3/);
      if (dynamic) return new URL(dynamic[2] + dynamic[4], window.location.href);
    }
    return null;
  };

  const disableLegacyModelViewer = (root) => {
    const elements = root.querySelectorAll?.('model-viewer[src]') ?? [];
    for (const element of elements) {
      element.dataset.legacySrc = element.getAttribute('src') ?? '';
      element.removeAttribute('src');
    }
  };

  disableLegacyModelViewer(document);
  new MutationObserver((records) => {
    for (const record of records) {
      for (const node of record.addedNodes) {
        if (node.nodeType !== Node.ELEMENT_NODE) continue;
        if (node.matches?.('model-viewer[src]')) {
          node.dataset.legacySrc = node.getAttribute('src') ?? '';
          node.removeAttribute('src');
        }
        disableLegacyModelViewer(node);
      }
    }
  }).observe(document.documentElement, { childList: true, subtree: true });

  document.addEventListener('DOMContentLoaded', () => {
    const button = document.getElementById(VIEW_BUTTON_ID);
    if (button) button.style.display = 'flex';
    disableLegacyModelViewer(document);
  });

  document.addEventListener('click', (event) => {
    const button = event.target.closest?.(`#${VIEW_BUTTON_ID}`);
    if (!button) return;

    event.preventDefault();
    event.stopImmediatePropagation();

    const contentUrl = findSplatUrl();
    if (!contentUrl) {
      console.error('SuperSplat AR launch failed: no PLY scene URL was found.');
      return;
    }

    const viewerUrl = new URL(VIEWER_PATH, window.location.href);
    viewerUrl.searchParams.set('content', contentUrl.href);
    viewerUrl.searchParams.set('webgl', '');
    window.location.assign(viewerUrl.href);
  }, true);
})();
