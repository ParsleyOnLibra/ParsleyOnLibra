'use strict';
const $=id=>document.getElementById(id);
const escapeHtml=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let cases=[], selectedId=null, filter='ALL';

function renderList(){
  const query=$('search').value.trim().toLowerCase();
  const visible=cases.filter(item=>(filter==='ALL'||item.priority===filter)&&`${item.id} ${item.title} ${item.requirements.join(' ')}`.toLowerCase().includes(query));
  $('case-list').innerHTML=visible.length?visible.map(item=>`<button type="button" class="case-item ${item.id===selectedId?'selected':''}" data-id="${escapeHtml(item.id)}" aria-pressed="${item.id===selectedId}"><span class="id">${escapeHtml(item.id)} · ${escapeHtml(item.priority)} · ${escapeHtml(item.status)}</span><span class="title">${escapeHtml(item.title)}</span></button>`).join(''):'<p>조건에 맞는 케이스가 없습니다.</p>';
  $('case-list').querySelectorAll('button').forEach(button=>button.onclick=()=>selectCase(button.dataset.id));
}

function selectCase(id){
  const item=cases.find(row=>row.id===id);if(!item)return;
  selectedId=id;renderList();
  const steps=item.steps.map((step,index)=>`<div class="step"><h4>${index+1}. ${escapeHtml(step.command)}${step.value==null?'':` (${escapeHtml(step.value)})`}</h4><p>기대: <strong>${escapeHtml(step.expected.code)}</strong> · ${escapeHtml(step.expected.state)} · ${step.expected.accepted?'승인':'거부'}</p><p>실제: <strong>${escapeHtml(step.actual.code)}</strong> · ${escapeHtml(step.actual.state)} · ${step.actual.accepted?'승인':'거부'}</p></div>`).join('');
  const events=item.events.map(event=>`<li>#${event.seq} ${escapeHtml(event.from)} → <strong>${escapeHtml(event.to)}</strong> · ${escapeHtml(event.code)}</li>`).join('');
  $('case-detail').innerHTML=`<span class="badge ${item.status==='PASS'?'':'fail'}">${escapeHtml(item.status)}</span><p class="meta">${escapeHtml(item.id)} · ${escapeHtml(item.priority)} · ${escapeHtml(item.technique)} · ${escapeHtml(item.requirements.join(', '))}</p><h3>${escapeHtml(item.title)}</h3><p>명령별 기대·실제 결과</p>${steps}<h4>이벤트 로그</h4><ol class="timeline">${events}</ol>${item.failures.length?`<p class="meta">불일치: ${escapeHtml(item.failures.join('; '))}</p>`:''}`;
}

async function boot(){
  try{
    const [reportResponse, mutationResponse]=await Promise.all([fetch('data/latest.json'),fetch('data/mutations.json')]);
    if(!reportResponse.ok||!mutationResponse.ok)throw Error('결과 파일을 불러오지 못했습니다.');
    const report=await reportResponse.json(), mutation=await mutationResponse.json();
    cases=report.cases;
    $('total').textContent=report.total;
    $('passed').textContent=`${report.passed}/${report.total}`;
    $('mutations').textContent=`${mutation.mutations.filter(item=>item.caught).length}/${mutation.mutations.length}`;
    renderList();
    if(cases.length)selectCase(cases[0].id);
  }catch(error){$('case-list').textContent=error.message;$('case-detail').textContent='저장된 결과를 표시할 수 없습니다. GitHub 저장소의 JSON 보고서를 확인해 주세요.';}
}
$('search').oninput=renderList;
document.querySelectorAll('.filters button').forEach(button=>button.onclick=()=>{filter=button.dataset.filter;document.querySelectorAll('.filters button').forEach(b=>b.classList.toggle('active',b===button));renderList();});
boot();
