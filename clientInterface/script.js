  const BASE = "http://127.0.0.1:8000";
  let token = null, lastRawResponse = '', requestLog = [];

  const val = id => document.getElementById(id).value;
  const num = id => parseInt(val(id));
  const $   = id => document.getElementById(id);

  function switchSection(name, el) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    $('section-' + name).classList.add('active');
    el.classList.add('active');
    $('section-title').textContent = el.textContent.trim();
  }

  $('prod-filter-type').addEventListener('change', function() {
    const input = $('prod-filter-value');
    input.disabled = !this.value;
    if (!this.value) input.value = '';
    else input.focus();
  });

  async function request(method, path, body = null, auth = true) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth && token) headers['Authorization'] = `Token ${token}`;
    const t_start = performance.now();
    try {
      const res = await fetch(BASE + path, { method, headers, body: body ? JSON.stringify(body) : undefined });
      const elapsed = Math.round(performance.now() - t_start);
      const text = await res.text();
      let data; try { data = JSON.parse(text); } catch { data = text; }
      renderResponse(res.status, method, path, data, elapsed);
      addLog(res.status, method, path, elapsed, data);
      return { status: res.status, data };
    } catch (e) {
      renderError(e.message, method, path);
      return null;
    }
  }

  function renderResponse(status, method, path, data, elapsed) {
    $('empty-state')?.remove();
    const badge = $('status-badge');
    badge.textContent = status;
    badge.className = status >= 200 && status < 300 ? 'ok' : status >= 400 ? 'err' : 'warn';
    $('response-method').textContent = method;
    $('response-url').textContent    = path;
    $('response-time').textContent   = elapsed + 'ms';
    const raw = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
    lastRawResponse = raw;
    $('response-body').innerHTML = '<pre>' + highlight(raw) + '</pre>';
  }

  function renderError(msg, method, path) {
    $('status-badge').textContent    = 'ERR';
    $('status-badge').className      = 'err';
    $('response-method').textContent = method;
    $('response-url').textContent    = path;
    $('response-time').textContent   = '';
    $('response-body').innerHTML     = `<pre style="color:#f87171">Errore di connessione:\n${msg}\n\nAssicurati che il server Django sia avviato su ${BASE}</pre>`;
  }

  function highlight(json) {
    return json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, m => {
        const cls = /^"/.test(m) ? (/:$/.test(m) ? 'json-key' : 'json-string')
                  : /true|false/.test(m) ? 'json-bool' : /null/.test(m) ? 'json-null' : 'json-number';
        return `<span class="${cls}">${m}</span>`;
      });
  }

  function addLog(status, method, path, elapsed, data) {
    requestLog.unshift({ status, method, path, elapsed, data });
    renderLog();
  }

  function renderLog() {
    $('log-panel').innerHTML = '<div id="log-label">Request History</div>' +
      requestLog.slice(0, 20).map((r, i) =>
        `<div class="log-entry log-${r.status}" onclick="showHistoryItem(${i})">
          <span class="log-method">${r.method}</span>
          <span class="log-status">${r.status}</span>
          <span class="log-url">${r.path}</span>
          <span class="log-time">${r.elapsed}ms</span>
        </div>`
      ).join('');
  }

  function showHistoryItem(i) {
    const r = requestLog[i];
    const raw = typeof r.data === 'string' ? r.data : JSON.stringify(r.data, null, 2);
    lastRawResponse = raw;
    $('response-body').innerHTML     = '<pre>' + highlight(raw) + '</pre>';
    $('response-method').textContent = r.method;
    $('response-url').textContent    = r.path;
    $('status-badge').textContent    = r.status;
  }

  function setAuth(t, label) {
    token = t;
    const el = $('token-status');
    t ? el.classList.add('logged') : el.classList.remove('logged');
    $('auth-label').textContent = t ? (label || 'Autenticato') : 'Non autenticato';
  }

  async function doLogin() {
    const r = await request('POST', '/api/auth/login/', { username: val('login-username'), password: val('login-password') }, false);
    if (r?.data.token)
     setAuth(r.data.token, val('login-username'));
  }

  async function doRegister() {
    const r = await request('POST', '/api/auth/register/', {
      username: val('reg-username'), email: val('reg-email'),
      password: val('reg-password'), password2: val('reg-password2'),
      role: val('reg-role'), first_name: val('reg-first-name'), last_name: val('reg-last-name'),
    }, false);
    if (r?.data.token)
     setAuth(r.data.token, val('reg-username'));
  }

  async function updateProfile() {
    const body = {};
    if (val('profile-email'))   body.email        = val('profile-email');
    if (val('profile-address')) body.address      = val('profile-address');
    if (val('profile-phone'))   body.phone_number = val('profile-phone');
    await request('PATCH', '/api/auth/profile/', body);
  }

  async function doLogout() {
    const r = await request('POST', '/api/auth/logout/');
    if (r?.status === 200) setAuth(null);
  }

  async function listProducts() {
    const type = val('prod-filter-type'), value = val('prod-filter-value'), ordering = val('prod-ordering');
    const params = new URLSearchParams();
    if (value) params.append(type, value);
    if (ordering) params.append('ordering', ordering);
    await request('GET', `/api/catalog/products/${params.size ? '?' + params : ''}`, null, !!token);
  }

  async function createProduct() {
    await request('POST', '/api/catalog/products/', {
      name: val('prod-name'), price: parseFloat(val('prod-price')),
      stock_quantity: num('prod-stock'), category: num('prod-cat'),
      available: val('prod-available') === 'true',
    });
  }