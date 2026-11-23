"""Build static QA process pages from reviewed project records."""

from html import escape
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PHASES = [
    ("planning", "Test planning", "목표·범위·위험·완료 기준을 정합니다."),
    ("monitoring", "Test monitoring", "계획과 실제 진행, 커버리지와 결함 상태를 비교합니다."),
    ("control", "Test control", "관찰 결과에 따라 우선순위·범위·방법을 조정합니다."),
    ("analysis", "Test analysis", "자료와 요구사항에서 무엇을 시험할지 찾습니다."),
    ("design", "Test design", "조건을 입력·예상 결과·테스트케이스로 구체화합니다."),
    ("implementation", "Test implementation", "테스트 데이터·환경·절차·스크립트를 준비합니다."),
    ("execution", "Test execution", "테스트를 실행하고 예상 결과와 실제 결과를 비교합니다."),
    ("completion", "Test completion", "미해결 항목, 배운 점, 종료 판단을 기록합니다."),
]


def links(items):
    return "".join(
        f'<li><a href="{escape(item["url"], quote=True)}">{escape(item["label"])}</a></li>'
        for item in items
    )


def render(project):
    title = escape(project["title"])
    slug = project["slug"]
    stages = project["stages"]
    if set(stages) != {phase_id for phase_id, _, _ in PHASES}:
        raise ValueError(f"Exactly eight test stages are required: {slug}")
    nav = "".join(
        f'<li><a href="#{phase_id}"><span>{number:02d}</span>{label}</a></li>'
        for number, (phase_id, label, _) in enumerate(PHASES, 1)
    )
    blocks = []
    for number, (phase_id, label, purpose) in enumerate(PHASES, 1):
        stage = stages[phase_id]
        evidence = stage.get("links", [])
        evidence_html = f'<ul class="links">{links(evidence)}</ul>' if evidence else ""
        blocks.append(
            f'<section class="stage" id="{phase_id}" aria-labelledby="{phase_id}-title">'
            f'<div class="stage-heading"><span class="step">{number:02d}</span>'
            f'<div><h2 id="{phase_id}-title">{label}</h2><p>{escape(purpose)}</p></div>'
            '<span class="state">공개 작업 중</span></div>'
            '<div class="stage-grid">'
            '<div class="record"><h3>현재 확인되는 자료</h3>'
            f'<p>{escape(stage["record"])}</p>{evidence_html}</div>'
            '<div class="decision"><h3>종수님 판단 대기</h3>'
            f'<p>{escape(stage["question"])}</p></div>'
            '</div></section>'
        )
    return f'''<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{title}의 QA 작업 기록: 계획부터 완료까지 8단계의 근거와 남은 판단을 공개합니다.">
  <title>{title} · QA 작업 기록 | Jongsoo Yang</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip" href="#main">본문으로 바로가기</a>
  <header class="site-header"><div class="wrap header-inner"><a class="brand" href="../index.html">JS / JONGSOO YANG</a><a href="../index.html#projects">프로젝트 목록으로 돌아가기 ↗</a></div></header>
  <main class="wrap" id="main">
    <section class="hero"><p class="eyebrow">QA PROCESS / OPEN WORKSPACE</p><h1>{title}</h1>
      <p class="lead">{escape(project["summary"])}</p>
      <p class="status">{escape(project["status"])}</p>
      <p class="notice">이 페이지는 공개 작업 기록입니다. 기존 코드와 실행 결과에는 AI 보조 작업이 포함됩니다. 아래의 질문과 미실행 항목은 종수님이 직접 판단·검증하기 전까지 본인 수행 성과로 표시하지 않습니다.</p>
      <ul class="hero-links">{links(project["links"])}</ul>
    </section>
    <nav class="phase-nav" aria-label="QA 단계 바로가기"><p>8단계 바로가기</p><ol>{nav}</ol></nav>
    {''.join(blocks)}
    <footer><p>단계 설명은 <a href="https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf">ISTQB CTFL v4.0.1</a>의 테스트 활동을 참고해 간단히 풀어 썼습니다.</p><a href="../index.html#projects">← 프로젝트 목록</a></footer>
  </main>
</body>
</html>
'''


def main():
    data = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
    for project in data["projects"]:
        (ROOT / f'{project["slug"]}.html').write_text(render(project), encoding="utf-8")
    print(f'Built {len(data["projects"])} QA process pages.')


if __name__ == "__main__":
    main()
