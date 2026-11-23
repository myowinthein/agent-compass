let compassSearchStarted = false;
let compassSearchReady = false;
let compassSearchFailedState = false;
let compassSearchUIReady = false;
let compassSearchPendingTimer;
let compassSearchErrorTimer;
let compassSearchInput;
let compassSearchStatus;
let compassSearchRetry;
let compassSearchWorker;
let compassSearchQueryId = 0;
const compassSearchQueries = new Map();

function clearCompassSearchFeedback() {
  clearTimeout(compassSearchPendingTimer);
  clearTimeout(compassSearchErrorTimer);
  compassSearchStatus.textContent = '';
}

function compassSearchFailed() {
  clearCompassSearchFeedback();
  compassSearchStarted = false;
  compassSearchReady = false;
  compassSearchFailedState = true;
  compassSearchWorker?.terminate();
  compassSearchWorker = null;
  compassSearchQueries.forEach(query => query.reject(new Error('Search unavailable')));
  compassSearchQueries.clear();
  compassSearchInput.removeAttribute('aria-busy');
  compassSearchRetry.disabled = false;
  compassSearchRetry.hidden = false;
  compassSearchStatus.textContent = 'Search unavailable. Press Enter or select Retry search.';
  const dismiss = () => {
    if (document.activeElement === compassSearchStatus) compassSearchErrorTimer = setTimeout(dismiss, 500);
    else compassSearchStatus.textContent = '';
  };
  compassSearchErrorTimer = setTimeout(dismiss, 4000);
}

const compassSearchClient = {
  search(input) {
    return new Promise((resolve, reject) => {
      if (!compassSearchReady || !compassSearchWorker) return reject(new Error('Search unavailable'));
      const id = ++compassSearchQueryId;
      compassSearchQueries.set(id, { resolve, reject });
      compassSearchWorker.postMessage({ type: 'query', id, input });
    });
  }
};

function initSearch(retry = false) {
  if (compassSearchStarted || (compassSearchFailedState && retry !== true)) return;
  compassSearchStarted = true;
  compassSearchFailedState = false;
  clearCompassSearchFeedback();
  compassSearchRetry.disabled = true;
  compassSearchInput.setAttribute('aria-busy', 'true');
  compassSearchPendingTimer = setTimeout(() => { compassSearchStatus.textContent = 'Loading search…'; }, 200);
  try {
    const worker = new Worker("/* WORKER_URL */");
    compassSearchWorker = worker;
    worker.onerror = event => {
      event.preventDefault();
      if (compassSearchWorker === worker) compassSearchFailed();
    };
    worker.onmessageerror = () => {
      if (compassSearchWorker === worker) compassSearchFailed();
    };
    worker.onmessage = ({ data }) => {
      if (compassSearchWorker !== worker) return;
      if (data.type === 'ready') {
        compassSearchReady = true;
        clearCompassSearchFeedback();
        compassSearchRetry.hidden = true;
        compassSearchInput.removeAttribute('aria-busy');
        if (!compassSearchUIReady) {
          searchLoaded(compassSearchClient, {});
          compassSearchUIReady = true;
        }
        if (document.activeElement === compassSearchInput) compassSearchInput.dispatchEvent(new Event('docs-search-ready'));
      } else if (data.type === 'results') {
        const query = compassSearchQueries.get(data.id);
        if (!query) return;
        compassSearchQueries.delete(data.id);
        query.resolve(data);
      } else {
        compassSearchFailed();
      }
    };
    worker.postMessage({ type: 'init', libraryUrl: "/* LIBRARY_URL */", indexUrl: "/* INDEX_URL */" });
  } catch {
    compassSearchFailed();
  }
}
