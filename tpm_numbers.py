"""Per-tab arithmetic and KPI reference; sample values are explicitly illustrative."""
import math
import streamlit as st


# Inputs: label, initial value, unit. Calculator functions do not call external services.
CALCS = {
    "Start": ("POC exit coverage", [("Passed criteria", 7, "count"), ("Total criteria", 10, "count")], lambda a,b: (a/b*100 if b else None), "%", "Passed / total × 100", "A gate is complete only when its evidence is attached; count alone is insufficient."),
    "Computer & TPM basics": ("Request latency budget", [("Network + API", 40, "ms"), ("Queue", 80, "ms"), ("Model", 600, "ms")], lambda a,b,c:a+b+c, "ms", "Network/API + queue + model", "Locate the dominant stage before assigning a performance owner."),
    "AI, ML & deep learning": ("Held-out evaluation count", [("Total labeled examples", 10000, "examples"), ("Held-out share", 20, "%")],lambda a,b:a*b/100,"examples","Total × held-out share / 100","Keep evaluation cases separate from training and tuning."),
    "System stack & accelerators": ("Weight-only memory", [("Parameters", 7, "billion"), ("Bytes per parameter", 2, "bytes")],lambda a,b:a*b,"decimal GB","Billion parameters × bytes/parameter","Add KV cache and runtime overhead before judging device fit."),
    "Data & model quality": ("F1 score", [("True positives",80,"count"),("False positives",10,"count"),("False negatives",20,"count")],lambda a,b,c:2*a/(2*a+b+c)*100 if 2*a+b+c else None,"%","2TP / (2TP + FP + FN) × 100","Check critical slices; one score can hide a severe failure."),
    "Training & tuning": ("Steps per epoch", [("Training examples",100000,"examples"),("Global batch size",256,"examples/step")],lambda a,b:math.ceil(a/b) if b else None,"steps","ceil(examples / global batch)","Multiply by epochs, then account for evaluation and checkpoints."),
    "LLM inference": ("Approx response time", [("TTFT",600,"ms"),("Output tokens",120,"tokens"),("ITL",30,"ms/token")],lambda a,b,c:a+max(b-1,0)*c,"ms","TTFT + (output tokens − 1) × ITL","Averages hide queue and tail latency; measure p95 under load."),
    "Intel platforms & porting": ("Illustrative VRAM headroom", [("Device capacity",32,"GB"),("Weights",14,"GB"),("KV + runtime",10,"GB")],lambda a,b,c:a-b-c,"GB","Capacity − weights − KV/runtime","A negative value flags a configuration that cannot fit; positive headroom still needs load testing."),
    "Benchmark & optimization": ("Latency speedup", [("Baseline latency",1200,"ms"),("Candidate latency",800,"ms")],lambda a,b:a/b if b else None,"×","Baseline / candidate","Both runs must use matched quality, inputs, concurrency and device count."),
    "Serving & Kubernetes": ("HPA scale estimate", [("Current replicas",4,"pods"),("Observed metric",90,"units"),("Target metric",60,"units")],lambda a,b,c:math.ceil(a*b/c) if c else None,"pods","ceil(current × observed / target)","Actual HPA also applies tolerance, limits, stabilization and metric availability."),
    "Observability & incidents": ("Allowed failed requests", [("Eligible requests",1000000,"requests"),("Availability SLO",99.9,"%")],lambda a,b:a*(1-b/100),"requests","Eligible × (1 − SLO/100)","Define the window and eligibility before using an error budget."),
    "RAG & agents": ("Grounded answer rate", [("Grounded answers",86,"answers"),("Reviewed answers",100,"answers")],lambda a,b:a/b*100 if b else None,"%","Grounded / reviewed × 100","Audit retrieval misses and unsafe tool actions separately."),
    "Customer engineering & career": ("Cost per million output tokens", [("All-in serving cost",8,"USD/hour"),("Output throughput",500000,"tokens/hour")],lambda a,b:a/b*1000000 if b else None,"USD / 1M tokens","Hourly cost / output tokens/hour × 1M","Include utilization, idle capacity and support costs in the all-in numerator."),
}

# Metric, calculation, illustrative before → after, decision implication.
METRICS = {
"Start":[("Exit pass rate","passed / total × 100","60% → 80%","Find which critical gate remains"),("Time to first run","first success − kickoff","10 d → 5 d","Remove setup blockers"),("Decision latency","decision − evidence ready","8 d → 3 d","Identify decision owner")],
"Computer & TPM basics":[("p95 latency","95th percentile of request times","1,200 → 900 ms","Locate bottleneck stage"),("Error rate","failed / eligible × 100","2% → 0.5%","Check interface and failure slices"),("Lead time","done − requested","14 → 10 d","Review dependency handoffs")],
"AI, ML & deep learning":[("Task pass rate","accepted / evaluated × 100","78% → 86%","Validate representative cases"),("Data leakage","overlap across train/test","2% → 0%","Repair split before claiming gain"),("Context length","input + output token budget","4k → 8k tokens","Test memory and quality at length")],
"System stack & accelerators":[("Peak VRAM","max device memory used","22 → 27 GB","Check headroom at concurrency"),("Device utilization","busy / available × 100","45% → 70%","Verify host/queue bottlenecks"),("Stack qualification","passed combos / planned","8/10 → 10/10","Pin drivers and runtimes")],
"Data & model quality":[("Precision","TP / (TP+FP)","0.80 → 0.89","Reduce costly false alarms"),("Recall","TP / (TP+FN)","0.70 → 0.85","Check missed positives"),("Critical-case pass","critical passes / critical cases","94% → 99%","Review remaining severe failures")],
"Training & tuning":[("Time to quality","time until eval target","12 → 9 h","Include checkpoint overhead"),("Training throughput","examples or tokens / s","800 → 1,000/s","Ensure quality still converges"),("Recovery time","resume − failure","60 → 15 min","Test checkpoints")],
"LLM inference":[("p95 TTFT","95th percentile first-token wait","1,200 → 700 ms","Investigate prefill and queue"),("p95 ITL","95th percentile token interval","55 → 35 ms","Investigate decode"),("Goodput","tokens/s inside SLO","2,000 → 2,600/s","Check quality and latency guardrails")],
"Intel platforms & porting":[("Functional parity","golden cases passed / total","90% → 99%","Resolve mismatches before perf"),("Memory headroom","capacity − peak usage","8 → 4 GB","Watch long contexts"),("Time to first run","success − setup start","4 → 2 d","Improve reproducible setup")],
"Benchmark & optimization":[("Speedup","baseline time / candidate time","1.0× → 1.4×","Verify matched workload"),("p95 latency","tail response time","1,000 → 750 ms","Confirm repeated runs"),("Cost/1M tokens","hourly cost / tokens/h × 1M","$18 → $13","Include all-in cost")],
"Serving & Kubernetes":[("Ready replicas","serving pods / desired pods","2/4 → 4/4","Inspect readiness/model load"),("Queue depth","requests waiting","60 → 15","Review capacity and autoscaling"),("Cold start","ready time − creation","180 → 90 s","Tune startup/rollout")],
"Observability & incidents":[("Availability","success / eligible × 100","99.8% → 99.95%","Compare with SLO window"),("MTTR","restore − detect","90 → 35 min","Practice rollback"),("Budget used","failed / allowed failures","80% → 30%","Slow risky releases if burn is high")],
"RAG & agents":[("Retrieval hit@k","queries with relevant top-k / total","75% → 90%","Fix search and freshness"),("Grounded rate","supported / reviewed answers","82% → 94%","Audit citations and claims"),("Tool success","valid completed calls / attempts","92% → 99%","Check retries and permissions")],
"Customer engineering & career":[("POC exit pass","passed gates / planned","2/4 → 4/4","Request sign-off"),("Aged blockers","issues beyond agreed age","7 → 2","Escalate with owner/date"),("Time to first value","first accepted outcome − kickoff","6 → 3 weeks","Remove customer friction")],
}

TREND = {
"Start":("POC exit pass rate",60,80,"higher"),"Computer & TPM basics":("p95 latency (ms)",1200,900,"lower"),
"AI, ML & deep learning":("Task pass rate (%)",78,86,"higher"),"System stack & accelerators":("Peak VRAM (GB)",22,27,"context"),
"Data & model quality":("Critical-case pass rate (%)",94,99,"higher"),"Training & tuning":("Time to quality (hours)",12,9,"lower"),
"LLM inference":("p95 TTFT (ms)",1200,700,"lower"),"Intel platforms & porting":("Functional parity (%)",90,99,"higher"),
"Benchmark & optimization":("p95 latency (ms)",1000,750,"lower"),"Serving & Kubernetes":("Queue depth",60,15,"lower"),
"Observability & incidents":("MTTR (minutes)",90,35,"lower"),"RAG & agents":("Grounded answer rate (%)",82,94,"higher"),
"Customer engineering & career":("POC exit pass rate (%)",50,100,"higher"),
}


def render_numbers(title: str) -> None:
    st.subheader("🧮 TPM numbers · calculator, KPI recipe, trend")
    name, inputs, fn, unit, formula, implication = CALCS[title]
    with st.expander(f"Calculate: {name}", expanded=True):
        cols=st.columns(len(inputs))
        values=[]
        for i,((label,default,input_unit),col) in enumerate(zip(inputs,cols)):
            with col:
                values.append(st.number_input(f"{label} ({input_unit})",min_value=0.0,max_value=100.0 if input_unit=="%" else None,value=float(default),step=1.0,key=f"calc_{title}_{i}"))
        result=fn(*values)
        st.metric(name,"Undefined" if result is None else f"{result:,.2f} {unit}")
        st.caption(f"Formula: {formula}. {implication} Inputs are illustrative until replaced with measurements.")
    st.markdown("**High-value KPI recipes and number trends**")
    st.dataframe([{"KPI":metric,"Formula or method":method,"Illustrative trend":sample,"TPM implication":action} for metric,method,sample,action in METRICS[title]],hide_index=True,use_container_width=True)
    label,before,after,direction=TREND[title]
    a,b=st.columns(2)
    baseline=a.number_input(f"Baseline · {label}",min_value=0.0,value=float(before),key=f"trend_base_{title}")
    current=b.number_input(f"Current · {label}",min_value=0.0,value=float(after),key=f"trend_now_{title}")
    change=(current-baseline)/baseline*100 if baseline else None
    st.bar_chart({"Illustrative comparison":{"Baseline":baseline,"Current":current}})
    if change is None:
        st.caption("Percent change is undefined when baseline is zero; report the absolute difference and context.")
    else:
        improved=(current>baseline if direction=="higher" else current<baseline if direction=="lower" else None)
        sense="directionally favorable" if improved else "directionally unfavorable" if improved is False else "requires context"
        st.caption(f"Change: {change:+.1f}%. This is {sense}; verify quality, workload and measurement conditions before claiming an outcome.")


def render_okr(title: str) -> None:
    metric=METRICS[title][0][0]
    st.markdown(f"**Example OKR recipe:** Objective: improve {title.lower()} for a named customer workload. Key result: move **{metric}** from a measured baseline to an agreed target by a dated milestone, while holding quality and reliability guardrails. Owner: named DRI; proof: reproducible report.")


def render_compendium(key_prefix: str) -> None:
    st.subheader("🧮 AI/ML KPI, formula and OKR compendium")
    focus=st.selectbox("Explore a focus area",["All domains"]+list(METRICS),key=f"{key_prefix}_focus")
    titles=list(METRICS) if focus=="All domains" else [focus]
    st.dataframe([{"Domain":title,"KPI":metric,"Formula or method":method,"Illustrative number trend":sample,"TPM implication":action} for title in titles for metric,method,sample,action in METRICS[title]],hide_index=True,use_container_width=True)
    st.markdown("**Reusable OKR pattern**")
    st.info("Objective: improve an agreed customer outcome. Key result: move a named metric from measured baseline to target by a date, while preserving quality and reliability. Name the owner, workload, version and proof artifact.")
    st.caption("Illustrative trends are teaching examples, not measured Intel product results or universal targets.")
