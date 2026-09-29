"""Accessible, self-contained animated SVG explainers for every app tab."""
from html import escape
from streamlit.components.v1 import html as render_html


# Four short steps show a real relationship rather than decorative motion.
# Each pair is (stage label, meaning). Speech is the memory cue from the guide.
SCENES = {
    "Start": ([('Customer goal', 'What matters?'), ('Workload', 'What runs?'), ('Evidence', 'What passed?'), ('Decision', 'Who acts?')], 'A TPM turns a vague request into a measured decision.', 'goal → evidence → decision'),
    "Computer & TPM basics": ([('Client', 'Sends request'), ('API', 'Accepts input'), ('Process', 'Runs model'), ('Response', 'Returns result')], 'When it is slow, locate the stage and its owner.', 'request path'),
    "AI, ML & deep learning": ([('Examples', 'Learning data'), ('Training', 'Updates weights'), ('Model', 'Saved behavior'), ('Inference', 'Uses weights')], 'A prompt uses a model; it normally does not train one.', 'learn → serve'),
    "System stack & accelerators": ([('App', 'Model call'), ('Framework', 'Runs operators'), ('Runtime', 'Maps to device'), ('Intel GPU', 'Executes work')], 'Pin every software layer before comparing hardware.', 'software stack'),
    "Data & model quality": ([('Data', 'Representative?'), ('Golden set', 'Expected cases'), ('Evaluate', 'By failure slice'), ('Release gate', 'Quality holds')], 'A speed win is useful only when quality holds.', 'quality gate'),
    "Training & tuning": ([('Batch', 'Examples'), ('Forward', 'Prediction'), ('Loss', 'Error signal'), ('Update', 'New weights')], 'Track time to quality, not just time per step.', 'training loop'),
    "LLM inference": ([('Prompt', 'Input tokens'), ('Prefill', 'Initial compute'), ('First token', 'TTFT'), ('Decode', 'Later tokens')], 'Long inputs affect prefill; long outputs affect decode.', 'two latency phases'),
    "Intel platforms & porting": ([('Baseline', 'Known result'), ('Target SKU', 'Exact device'), ('Parity', 'Correct output'), ('Benchmark', 'Fair workload')], 'Qualify correctness before performance on the exact SKU.', 'porting gates'),
    "Benchmark & optimization": ([('Fix workload', 'Same inputs'), ('Warm up', 'Stable state'), ('Measure', 'Latency + speed'), ('Check quality', 'No regression')], 'Compare under matched settings and repeat the run.', 'fair comparison'),
    "Serving & Kubernetes": ([('Request', 'Incoming load'), ('Service', 'Routes traffic'), ('Ready pod', 'Model loaded'), ('GPU', 'Generates')], 'A healthy pod must actually be ready to serve.', 'serving path'),
    "Observability & incidents": ([('Signal', 'SLO breach'), ('Impact', 'Who is affected?'), ('Mitigate', 'Restore service'), ('Learn', 'Prevent repeat')], 'Quantify impact, restore service, then find the cause.', 'incident loop'),
    "RAG & agents": ([('Question', 'User intent'), ('Retrieve', 'Find evidence'), ('Reason', 'Ground answer'), ('Tool', 'Act with approval')], 'External context informs answers; tools need permissions.', 'grounded agent'),
    "Customer engineering & career": ([('POC goal', 'Agree criteria'), ('Evidence', 'Qualify result'), ('Trade-off', 'Explain risk'), ('Sign-off', 'Decision owner')], 'Tell the customer what the data means and what happens next.', 'customer decision'),
    "Calculators": ([('Inputs', 'Units + scope'), ('Assumptions', 'What is omitted?'), ('Estimate', 'Simple math'), ('Validate', 'Real workload')], 'An estimate starts the conversation; measurement settles it.', 'estimate ≠ benchmark'),
    "Master cheatsheet": ([('Recall', 'Core concepts'), ('Apply', 'Customer case'), ('Test', 'Answer aloud'), ('Decide', 'Next action')], 'Use the sheet to retrieve a concept, then apply it.', 'learn → apply'),
}


def _scene_markup(title: str) -> str:
    steps, speech, tag = SCENES[title]
    boxes = []
    for i, (label, detail) in enumerate(steps):
        x = 28 + i * 218
        boxes.append(f'''<g class="card card-{i}" aria-label="Step {i+1}: {escape(label)}; {escape(detail)}">
          <rect x="{x}" y="75" width="186" height="110" rx="17" fill="#fff" stroke="#9dc6de" stroke-width="2"/>
          <circle cx="{x+26}" cy="104" r="15" fill="#087e8b"/>
          <text x="{x+26}" y="110" text-anchor="middle" class="number">{i+1}</text>
          <text x="{x+18}" y="140" class="stage">{escape(label)}</text>
          <text x="{x+18}" y="164" class="detail">{escape(detail)}</text>
        </g>''')
    links = ''.join(
        f'<path class="travel" d="M {214+i*218} 130 H {246+i*218}" marker-end="url(#arrow)"/>'
        for i in range(3)
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"/>
    <style>
      body{{margin:0;background:transparent;font-family:system-ui,-apple-system,Segoe UI,sans-serif;color:#17324a}}
      .wrap{{max-width:920px;margin:0 auto;background:linear-gradient(135deg,#eff9fb,#f6f2ff);border:1px solid #c9e2e8;border-radius:20px;padding:8px;box-sizing:border-box}}
      svg{{width:100%;height:auto;display:block}}
      .title{{font-size:21px;font-weight:750;fill:#17324a}}
      .tag{{font-size:13px;fill:#456579}}
      .stage{{font-size:17px;font-weight:700;fill:#17324a}}
      .detail{{font-size:13px;fill:#42627a}}
      .number{{font-size:14px;font-weight:700;fill:#fff}}
      .speech{{font-size:15px;font-weight:600;fill:#17324a}}
      .travel{{fill:none;stroke:#087e8b;stroke-width:4;stroke-dasharray:10 7;animation:move 1.3s linear infinite}}
      .card{{transform-origin:center;animation:glow 4.8s ease-in-out infinite}}
      .card-1{{animation-delay:1.2s}}.card-2{{animation-delay:2.4s}}.card-3{{animation-delay:3.6s}}
      .guide{{transform-origin:785px 274px;animation:bob 2.4s ease-in-out infinite}}
      .eye{{animation:blink 5s infinite;transform-origin:center}}
      @keyframes move{{to{{stroke-dashoffset:-34}}}}
      @keyframes glow{{0%,75%,100%{{opacity:.84}}15%{{opacity:1;filter:drop-shadow(0 3px 5px #6cbec790)}}}}
      @keyframes bob{{50%{{transform:translateY(-5px)}}}}
      @keyframes blink{{0%,94%,98%,100%{{transform:scaleY(1)}}96%{{transform:scaleY(.12)}}}}
      @media (max-width:650px){{.wrap{{overflow-x:auto}}svg{{min-width:760px}}}}
      @media (prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important;transition:none!important}}.card{{opacity:1}}}}
    </style></head><body><div class="wrap">
    <svg viewBox="0 0 910 360" role="img" aria-labelledby="t d">
      <title id="t">{escape(title)} animated concept cartoon</title>
      <desc id="d">Four stages: {escape(' to '.join(label for label,_ in steps))}. {escape(speech)}</desc>
      <defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7" fill="#087e8b"/></marker></defs>
      <text x="28" y="37" class="title">{escape(title)}</text>
      <text x="28" y="58" class="tag">{escape(tag)} · follow the moving path from left to right</text>
      {links}{''.join(boxes)}
      <rect x="28" y="218" width="676" height="103" rx="18" fill="#fff" stroke="#c9e2e8"/>
      <path d="M688 258 L728 272 L688 281" fill="#fff" stroke="#c9e2e8"/>
      <text x="48" y="253" class="speech">TPM guide says:</text>
      <foreignObject x="48" y="266" width="630" height="46"><div xmlns="http://www.w3.org/1999/xhtml" style="font-size:15px;line-height:1.35;color:#17324a">{escape(speech)}</div></foreignObject>
      <g class="guide" aria-label="Smiling cartoon TPM guide holding a checklist">
        <ellipse cx="796" cy="321" rx="79" ry="10" fill="#aac9cf" opacity=".45"/>
        <rect x="747" y="243" width="88" height="75" rx="23" fill="#087e8b"/>
        <circle cx="792" cy="216" r="38" fill="#f6cd9b" stroke="#ba865f" stroke-width="2"/>
        <path d="M756 210 Q755 173 792 175 Q830 173 829 210 Q810 193 792 190 Q777 202 756 210" fill="#354463"/>
        <ellipse class="eye" cx="779" cy="219" rx="3.6" ry="5" fill="#21394b"/>
        <ellipse class="eye" cx="805" cy="219" rx="3.6" ry="5" fill="#21394b"/>
        <path d="M780 234 Q792 246 806 233" fill="none" stroke="#8d4f43" stroke-width="3" stroke-linecap="round"/>
        <rect x="828" y="255" width="43" height="51" rx="5" fill="#fff" stroke="#3a6476" stroke-width="2"/>
        <path d="M836 267 h25 M836 277 h25 M836 287 h20" stroke="#54a6aa" stroke-width="2"/>
        <path d="M747 277 Q724 267 714 286" fill="none" stroke="#f6cd9b" stroke-width="12" stroke-linecap="round"/>
      </g>
    </svg></div></body></html>'''


def show_visual(title: str) -> None:
    """Render inline; CSS motion is automatically disabled by reduced-motion settings."""
    render_html(_scene_markup(title), height=390, scrolling=False)
