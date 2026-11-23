// Index and query rules are taken from this build's Just the Docs search code.
let docs;
let index;

function search(input) {
  /* QUERY_RULES */
  return results;
}

self.onmessage = async ({ data }) => {
  try {
    if (data.type === 'init') {
      const request = fetch(data.indexUrl);
      importScripts(data.libraryUrl);
      const response = await request;
      if (!response.ok) throw new Error('Search data unavailable');
      docs = await response.json();
      /* INDEX_RULES */
      self.postMessage({ type: 'ready' });
    } else if (data.type === 'query' && index) {
      const results = search(data.input);
      const matches = {};
      results.forEach(result => { matches[result.ref] = docs[result.ref]; });
      self.postMessage({ type: 'results', id: data.id, results, docs: matches });
    } else {
      throw new Error('Search is not ready');
    }
  } catch {
    self.postMessage({ type: 'error' });
  }
};
