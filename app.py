"""Intel AI/ML TPM Compass: staged, source-linked, interactive quick reference."""
import streamlit as st
from curriculum import LESSONS, REF
from deeper import DEPTH
from concept_cards import CARDS, CORE_TABLES, LEARNING

st.set_page_config(page_title="Intel AI/ML TPM Compass",page_icon="🧭",layout="wide")
st.title("🧭 Intel AI/ML TPM Compass")
st.caption("Basic → intermediate → advanced · Customer engineering quick reference · Reviewed 25 September 2026")
st.info("Examples are educational. Hardware support, software versions and performance change. Verify the exact stack against linked official documentation.")
tabs=st.tabs(["🏠 Start"]+[f"{i:02d} · {x['title']}" for i,x in enumerate(LESSONS,1)]+["🧮 Calculators","📚 Master cheatsheet"])
with tabs[0]:
 st.subheader("Learning path at a glance")
 st.dataframe([{"Step":i,"Focus":x["title"],"Level":x["level"],"Key KPI":x["metric"]} for i,x in enumerate(LESSONS,1)],hide_index=True,use_container_width=True)
 st.markdown("**How to use it:** Pick a tab, explain its concepts aloud, solve its two questions, and use the KPI and example in your next project review.")
for tab,x in zip(tabs[1:1+len(LESSONS)],LESSONS):
 with tab:
  st.header(x["title"])
  st.caption(x["level"]+" · Intel AI/ML customer-engineering TPM")
  st.subheader("Bare minimum concepts")
  st.dataframe([{"Concept":name,"Intuitive example or use case":example,"TPM takeaway":takeaway,"Key metric or formula":metric} for name,example,takeaway,metric in CARDS[x["title"]]],hide_index=True,use_container_width=True)
  left,right=st.columns(2)
  left.metric("KPI to discuss",x["metric"])
  right.info("**Formula / estimate**\n\n"+x["formula"])
  st.markdown("**Practical customer example:** "+x["example"])
  extra=DEPTH[x["title"]]
  st.subheader("One level deeper · what a senior TPM should know")
  for item in extra["details"]: st.markdown("- "+item)
  st.markdown("**Additional high-value metrics:** "+" · ".join(extra["metrics"]))
  st.subheader("Test yourself · essential questions")
  for i,(q,ideal) in enumerate(x["quiz"]):
   with st.expander(f"Q{i+1}. {q}"):
    st.text_area("Try your answer first",key=f"draft_{x['title']}_{i}",height=75)
    if st.checkbox("Show ideal practical answer",key=f"show_{x['title']}_{i}"): st.success(ideal)
  st.subheader("Senior technical TPM interview question")
  question,ideal=extra["interview"]
  with st.expander(question):
   st.text_area("Practice a concise answer",key="interview_"+x["title"],height=90)
   if st.checkbox("Show strong expected answer",key="interview_reveal_"+x["title"]): st.success(ideal)
  st.markdown("**Official references:** "+" · ".join(f"[{r}]({REF[r]})" for r in x["refs"]))
  st.subheader("Most costly common mistakes · and how to avoid them")
  st.dataframe([{"Mistake":mistake,"Better practice":fix} for mistake,fix in extra["mistakes"]],hide_index=True,use_container_width=True)
  st.caption("Always state units, workload, software versions and test conditions with a metric.")
with tabs[-2]:
 st.header("🧮 TPM quick calculators")
 choice=st.selectbox("Choose a calculator",["Model weight memory","LLM response-time estimate","Throughput and cost","Classification quality"])
 if choice=="Model weight memory":
  p=st.number_input("Model parameters (billions)",0.01,1000.0,7.0)
  precision=st.selectbox("Nominal precision",["FP32","FP16/BF16","INT8","4-bit ideal packing"])
  factor={"FP32":4.0,"FP16/BF16":2.0,"INT8":1.0,"4-bit ideal packing":0.5}[precision]
  st.metric("Approx weight memory only",f"{p*factor:.2f} GB")
  st.bar_chart({"Weight memory (GB)":{label:p*bytes_per for label,bytes_per in [("FP32",4.0),("FP16/BF16",2.0),("INT8",1.0),("4-bit ideal",0.5)]}})
  st.caption("Decimal GB. Excludes KV cache, activations, runtime, fragmentation and quantization metadata.")
 elif choice=="LLM response-time estimate":
  ttft=st.number_input("TTFT (seconds)",0.0,1000.0,0.6)
  tokens=st.number_input("Generated tokens",1,100000,120)
  itl=st.number_input("ITL (milliseconds)",0.0,10000.0,30.0)
  st.metric("Approx response time",f"{ttft+(tokens-1)*itl/1000:.2f} s")
  st.caption("Assumes constant inter-token latency. Queueing and load cause variation.")
 elif choice=="Throughput and cost":
  output=st.number_input("Output tokens per hour",1,10000000000,1000000)
  cost=st.number_input("All-in serving cost per hour (USD)",0.0,1000000.0,5.0)
  st.metric("Cost per 1M output tokens",f"USD {cost/output*1000000:.2f}")
  st.caption("Include relevant infrastructure and operations. Keep input/output token denominators distinct.")
 else:
  tp=st.number_input("True positives",0,10000000,80)
  fp=st.number_input("False positives",0,10000000,10)
  fn=st.number_input("False negatives",0,10000000,20)
  st.metric("Precision",f"{tp/(tp+fp):.1%}" if tp+fp else "Undefined")
  st.metric("Recall",f"{tp/(tp+fn):.1%}" if tp+fn else "Undefined")
  st.caption("Choose metrics appropriate to the task and the cost of errors.")
with tabs[-1]:
 st.header("📚 Master cheatsheet")
 st.dataframe([{"Stage":x["level"],"Topic":x["title"],"Three concepts":" · ".join(x["terms"]),"KPI":x["metric"],"Additional metrics":" · ".join(DEPTH[x["title"]]["metrics"]),"Formula":x["formula"],"Example":x["example"]} for x in LESSONS],hide_index=True,use_container_width=True)
 st.subheader("Core AI/ML learning tables")
 for heading,rows in CORE_TABLES.items():
  st.markdown("**"+heading+"**")
  st.dataframe([{"Concept or stage":a,"Plain-language meaning":b,"Use case or focus":c,"Metric or risk":d,"Source":LEARNING.get(e,REF.get(e,""))} for a,b,c,d,e in rows],hide_index=True,use_container_width=True,column_config={"Source":st.column_config.LinkColumn("Source")})
 st.markdown("**Foundational learning references:** "+" · ".join(f"[{name}]({url})" for name,url in LEARNING.items()))
 st.subheader("Intuitive latency visual · illustrative")
 prompt_ms=st.slider("Prompt processing + queue (ms)",0,3000,450,50,key="visual_prompt")
 decode_ms=st.slider("Decode time (ms)",0,6000,1200,50,key="visual_decode")
 st.bar_chart({"Illustrative latency (ms)":{"Prompt + queue":prompt_ms,"Decode":decode_ms}})
 st.caption("Values are user-selected teaching examples, not measured Intel or model performance. Total = prompt + queue + decode in this simplified view.")
 st.subheader("Four customer POC gates")
 st.dataframe([{"Gate":"1 · Functional","Proof":"Named model loads; representative outputs pass; exact stack pinned"},{"Gate":"2 · Portability","Proof":"Intel target supports model, operators, precision and drivers"},{"Gate":"3 · Performance","Proof":"Comparable latency and throughput at equal quality and workload"},{"Gate":"4 · Production","Proof":"SLO, monitoring, load test, rollback, owner and sign-off"}],hide_index=True,use_container_width=True)
 st.subheader("Official references")
 st.dataframe([{"Resource":name,"URL":url} for name,url in REF.items()],hide_index=True,use_container_width=True,column_config={"URL":st.column_config.LinkColumn("URL")})
 st.caption("Editorial essentials, not a measured top-1% ranking. Verify current product and framework support.")
