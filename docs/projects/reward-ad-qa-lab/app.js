'use strict';
const $ = id => document.getElementById(id);
const escapeHtml = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
let cases = [];
let selectedId = null;

function renderList() {
  const query = $('search').value.trim().toLowerCase();
  const visible = cases.filter(item => `${item.id} ${item.title} ${item.requirements.join(' ')}`.toLowerCase().includes(query));
  $('case-list').innerHTML = visible.length
    ? visible.map(item => `<button type="button" class="case-item ${item.id === selectedId ? 'selected' : ''}" data-id="${escapeHtml(item.id)}" aria-pressed="${item.id === selectedId}"><span class="id">${escapeHtml(item.id)} · ${escapeHtml(item.status)} · ${escapeHtml(item.requirements.join(', '))}</span><span class="title">${escapeHtml(item.title)}</span></button>`).join('')
    : '<p>조건에 맞는 케이스가 없습니다.</p>';
  $('case-list').querySelectorAll('button').forEach(button => { button.onclick = () => selectCase(button.dataset.id); });
}

function selectCase(id) {
  const item = cases.find(row => row.id === id);
  if (!item) return;
  selectedId = id;
  renderList();
  const steps = item.steps.map((step, index) => `<div class="step"><h4>${index + 1}. ${escapeHtml(step.expected.action)}${step.expected.value == null ? '' : ` (${escapeHtml(step.expected.value)})`}</h4><p>기대: <strong>${escapeHtml(step.expected.code)}</strong> · ${escapeHtml(step.expected.state)} · ${step.expected.accepted ? '승인' : '거부'}</p><p>실제: <strong>${escapeHtml(step.actual.code)}</strong> · ${escapeHtml(step.actual.state)} · ${step.actual.accepted ? '승인' : '거부'}</p></div>`).join('');
  const snapshot = item.snapshot;
  const events = item.events.map(event => `<li>#${event.seq} ${escapeHtml(event.from)} → <strong>${escapeHtml(event.to)}</strong> · ${escapeHtml(event.code)}${event.txn == null ? '' : ` · ${escapeHtml(event.txn)}`}</li>`).join('');
  $('case-detail').innerHTML = `<span class="badge ${item.status === 'PASS' ? '' : 'fail'}">${escapeHtml(item.status)}</span><p class="meta">${escapeHtml(item.id)} · ${escapeHtml(item.requirements.join(', '))}</p><h3>${escapeHtml(item.title)}</h3><div class="snapshot"><p><strong>최종 상태:</strong> ${escapeHtml(snapshot.state)} · <strong>노출:</strong> ${escapeHtml(snapshot.impressions)}건</p><p><strong>보상 기록:</strong> ${escapeHtml(snapshot.credit_events.join(', ') || '없음')} · <strong>대기:</strong> ${escapeHtml(snapshot.pending.join(', ') || '없음')}</p></div><p>명령별 기대·실제 결과</p>${steps}<h4>이벤트 로그</h4><ol class="timeline">${events}</ol>${item.failures.length ? `<p class="meta">불일치: ${escapeHtml(item.failures.join('; '))}</p>` : ''}`;
}

async function boot() {
  try {
    const [normalResponse, mutationResponse] = await Promise.all([fetch('data/latest.json'), fetch('data/mutation.json')]);
    if (!normalResponse.ok || !mutationResponse.ok) throw Error('결과 JSON을 불러오지 못했습니다.');
    const normal = await normalResponse.json();
    const mutation = await mutationResponse.json();
    cases = normal.cases;
    $('passed').textContent = `${normal.passed}/${normal.total}`;
    $('steps').textContent = `${normal.steps}단계 자동 실행`;
    const caught = mutation.cases.filter(item => item.status === 'FAIL');
    $('mutations').textContent = `${caught.length}건`;
    $('mutation-detail').innerHTML = caught.length
      ? `중복 보상을 의도적으로 주입하자 <strong>${escapeHtml(caught.map(item => item.id).join(', '))}</strong>에서 불일치가 나타났습니다. ${escapeHtml(caught[0].failures.join('; '))}. 실제 광고 제품에서 발견한 결함은 아닙니다. <a href="data/mutation.json">결함 주입 원본 결과 ↗</a>`
      : '저장된 결함 주입 결과에서 실패 케이스를 찾지 못했습니다.';
    renderList();
    if (cases.length) selectCase(cases[0].id);
  } catch (error) {
    $('case-list').textContent = error.message;
    $('case-detail').textContent = 'GitHub 저장소의 JSON 보고서를 확인해 주세요.';
    $('mutation-detail').textContent = '결함 주입 결과를 표시할 수 없습니다.';
  }
}

$('search').oninput = renderList;
boot();
