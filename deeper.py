"""Senior TPM depth: high-value details, metrics, interview answers and avoidable errors."""
DEPTH={
"Computer & TPM basics":{
"details":["Map request path: client → API → serving process → accelerator → response; identify the owner at each hop.","Distinguish a dependency from a risk: a dependency needs delivery from another team; a risk describes uncertain impact.","Define done with evidence: test artifact, metric threshold, owner, rollback and customer acknowledgement."],
"metrics":["p95 end-to-end latency (ms)","milestone slip (days)","open blockers by severity/owner"],
"interview":("A customer says the demo is slow. How do you triage?","Reproduce the exact workload, separate network, queue, model prefill/decode and device time, establish a baseline, assign owners and set a retest date."),
"mistakes":[("Reporting 'on track' without an exit test","Publish an acceptance criterion and dated evidence."),("Treating every blocker as a coding issue","Map stack layer, owner and dependency first.")]},
"AI, ML & deep learning":{
"details":["Separate classification, retrieval and generation because each needs different evaluation.","Training data, validation data and test data have different jobs; leakage inflates apparent quality.","A model's context window is a limit on tokens processed, not a guarantee of factual recall."],
"metrics":["task-specific pass rate (%)","data coverage by slice (%)","hallucination/unsupported-answer rate (%)"],
"interview":("How do you tell a stakeholder that an LLM demo works?","Show representative and adversarial task tests, a baseline, failure categories, human review criteria and limitations."),
"mistakes":[("Calling every AI feature an agent","Specify whether it predicts, generates, retrieves or invokes tools."),("Using one cherry-picked prompt","Create a representative golden set with failures.")]},
"System stack & accelerators":{
"details":["A compatibility matrix should pin OS/kernel, firmware, driver, runtime, framework, serving engine and model.","Memory fit includes weights, KV cache and transient/runtime allocation; a model that loads may still fail at concurrency.","Distinguish host bottlenecks, device bottlenecks and I/O bottlenecks before changing hardware."],
"metrics":["VRAM peak (GB)","device utilization (%)","versioned pass/fail matrix"],
"interview":("Model runs on CPU but not an Intel GPU; what do you request?","Capture exact stack and error, reproduce a minimal prompt, check device visibility/operator support/precision/memory, then route to the owning layer."),
"mistakes":[("Comparing SKU datasheets as if they were application results","Measure the exact end-to-end workload."),("Leaving software versions out of a bug","Attach a reproducible environment manifest.")]},
"Data & model quality":{
"details":["Golden cases should include common inputs, boundary cases, failure modes and customer-sensitive slices.","For imbalanced classification, accuracy can hide poor recall; choose a metric that matches business costs.","LLM judging needs a rubric and calibration against human examples; inspect disagreement."],
"metrics":["precision/recall/F1 (%)","slice pass rate (%)","label disagreement (%)"],
"interview":("A benchmark is faster but outputs differ; is it a win?","Only if quality remains within agreed tolerances on a representative evaluation set and the workload is comparable."),
"mistakes":[("Optimizing on test data","Separate tuning and held-out evaluation."),("Averaging away critical failures","Report slices and severe-case counts.")]},
"Training & tuning":{
"details":["Global batch = microbatch × gradient accumulation × data-parallel replicas, assuming matched configurations.","Track data lineage, random seed, checkpoint and optimizer settings for reproducibility.","Training throughput is useful only alongside convergence and evaluation quality."],
"metrics":["samples/s or tokens/s","time to quality target (hours)","checkpoint recovery time"],
"interview":("Why can a faster step time still delay a training project?","More steps may be required to reach quality; compare time-to-target including data loading, checkpoints and failures."),
"mistakes":[("Reporting loss without held-out quality","Pair training curves with evaluation."),("Treating OOM only as a hardware defect","Review batch, sequence length, precision and optimizer state.")]},
"LLM inference":{
"details":["Decompose TTFT into queue, tokenization, prefill and first decode where instrumentation allows.","Long prompts stress prefill; long outputs stress decode. Report both lengths.","Concurrency improves throughput until queueing or KV memory drives p95 latency up."],
"metrics":["p50/p95 TTFT (ms)","p95 ITL (ms)","goodput at SLO (tokens/s)"],
"interview":("Throughput improves but p95 TTFT doubles. What do you do?","Check arrival rate and queue, then adjust concurrency/batching under an agreed latency SLO; report the trade-off."),
"mistakes":[("Quoting tokens/s without latency","Show a throughput-latency curve at fixed workload."),("Mixing prefill and decode effects","Record prompt/output length and stage timings.")]},
"Intel platforms & porting":{
"details":["Qualification means functional correctness, supported operators/precision, memory fit, and reproducible performance on exact SKU.","A model's nominal weight size excludes KV cache and runtime overhead.","Some software features differ by device, stack and release; verify official support rather than infer parity."],
"metrics":["model coverage (%)","unsupported-operator count","time to first correct run"],
"interview":("How would you port an Nvidia customer workload to Intel?","Pin baseline, choose an Intel-supported runtime, confirm model and precision, pass golden tests, then benchmark equal workloads and capture gaps."),
"mistakes":[("Claiming B60/B70 parity from architecture alone","Test both exact systems."),("Benchmarking before functional validation","Gate performance on correctness and support.")]},
"Benchmark & optimization":{
"details":["Separate cold start from warmed steady state; report both when customer usage requires them.","Report hardware count, power, precision, version, prompt/output distribution and concurrency.","MLPerf Offline and Server scenarios answer different throughput/latency questions; do not merge their headline numbers."],
"metrics":["p95 TTFT/ITL","SLO-compliant goodput","cost per 1M tokens"],
"interview":("Vendor A claims 2x throughput. How do you validate?","Reproduce model, workload, quality target, device count, power and software; compare latency at matched throughput and total cost."),
"mistakes":[("Comparing unmatched precisions or quality","Normalize settings and validate outputs."),("Publishing one best run","Repeat runs and show variance.")]},
"Serving & Kubernetes":{
"details":["Readiness failure removes a pod from service; liveness failure can restart it; startup probes protect slow initialization.","A GPU pod can be ready at the HTTP layer while model weights are not loaded; design readiness for actual service readiness.","HPA scales from chosen metrics, but capacity and warm-up constrain response to bursts."],
"metrics":["ready replicas","cold-start time (s)","queue depth and p95 latency"],
"interview":("Why is a rollout receiving 503s despite healthy pods?","Check readiness definition, Service endpoints, model load, routing, capacity and rollout settings; roll back if impact exceeds SLO."),
"mistakes":[("Using liveness to restart slow model initialization","Add suitable startup and readiness probes."),("Autoscaling only on CPU for GPU bottlenecks","Use relevant workload metrics and load tests.")]},
"Observability & incidents":{
"details":["An SLO needs a denominator and time window; define what counts as a successful eligible request.","Correlate model, image, driver and configuration changes with latency/error charts.","Preserve incident timeline, mitigation, root cause and prevention action with owners."],
"metrics":["error-budget burn","MTTD/MTTR","affected requests or tenants"],
"interview":("A customer's p95 regresses after deployment; how do you lead?","Quantify impact, decide rollback/mitigation, compare versions and traces, communicate updates, then assign root-cause follow-up."),
"mistakes":[("Troubleshooting without an impact statement","Quantify users, duration and severity first."),("Closing after rollback alone","Document mechanism and preventive tests.")]},
"RAG & agents":{
"details":["RAG quality depends on document freshness, chunking, retrieval relevance and answer grounding.","A tool-using agent needs explicit permissions, timeouts, retries, idempotency and action logs.","Evaluate each stage and the end-to-end workflow; a good model cannot fix stale retrieval."],
"metrics":["retrieval hit rate (%)","grounded answer rate (%)","tool success rate (%)"],
"interview":("An agent cites the wrong runbook and opens bad tickets; how do you fix it?","Check retrieval and permissions, require citation validation and approval before side effects, add failing cases to eval and monitor."),
"mistakes":[("Treating tool output as trusted instructions","Constrain tools and validate external content."),("Measuring only final answer quality","Instrument retrieval, tool and model stages.")]},
"Customer engineering & career":{
"details":["Run POCs with written customer workload, baseline, exit criteria and decision owner before optimization.","Create a gap register that distinguishes product defect, unsupported feature, environment issue and documentation gap.","Translate technical metrics into customer impact and a decision: proceed, mitigate, defer or stop."],
"metrics":["time to first working run","POC exit pass rate (%)","aged blockers and adoption"],
"interview":("Tell me about a disputed benchmark across vendors.","Explain how you aligned workload and quality, resolved methodological disagreements, documented trade-offs and secured a decision."),
"mistakes":[("A POC with no decision gate","Agree on pass criteria and decision date at kickoff."),("Overstating influence in interviews","Separate your actions from the team's and quantify the result.")]},
}
