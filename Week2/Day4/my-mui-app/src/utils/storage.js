export function saveToStorage(key, value) {
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (e) {
    // ignore quota errors in environments that disallow localStorage
    console.warn('saveToStorage error', e);
  }
}

export function loadFromStorage(key) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch (e) {
    console.warn('loadFromStorage error', e);
    return null;
  }
}
