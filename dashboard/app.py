from pathlib import Path
import sys,pandas as pd,plotly.express as px,plotly.graph_objects as go,streamlit as st
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.data_loader import load_unified_data,split_records
from src.forecasting import build_forecast
st.set_page_config(page_title="Ethiopia FI Forecast",page_icon="🇪🇹",layout="wide")
df=load_unified_data(ROOT/"data/raw/ethiopia_fi_unified_data.csv");R=split_records(df);o,e,i,t=R["observation"],R["event"],R["impact_link"],R["target"]
st.title("🇪🇹 Ethiopia Financial Inclusion Forecasting")
c1,c2,c3,c4=st.columns(4);c1.metric("Account ownership","49%","2024");c2.metric("Digital payments","35%","2024");c3.metric("Mobile money","9.45%","+4.75 pp");c4.metric("M-Pesa active share","65.7%")
tabs=st.tabs(["Overview","Trends","Event impacts","Forecasts","Projections"])
with tabs[0]: st.plotly_chart(px.bar(df.record_type.value_counts().reset_index(),x="record_type",y="count",title="Records by type"),use_container_width=True);st.dataframe(df,use_container_width=True)
with tabs[1]:
 sel=st.multiselect("Indicators",["ACC_OWNERSHIP","DIGITAL_PAYMENT","MOBILE_MONEY_ACCOUNT","ACC_OWNERSHIP_FEMALE","ACC_OWNERSHIP_MALE"],default=["ACC_OWNERSHIP","DIGITAL_PAYMENT","MOBILE_MONEY_ACCOUNT"]);z=o[o.indicator_code.isin(sel)].copy();z["year"]=z.observation_date.dt.year;fig=px.line(z,x="year",y="value_numeric",color="indicator",markers=True);[fig.add_vline(x=x.year,line_dash="dot",opacity=.3) for x in e.observation_date];st.plotly_chart(fig,use_container_width=True);ch=o[o.indicator_code.isin(["P2P_TX_COUNT","ATM_TX_COUNT"])];st.plotly_chart(px.bar(ch,x="indicator",y="value_numeric",title="Channel comparison"),use_container_width=True)
with tabs[2]: m=i.pivot_table(index="parent_id",columns="related_indicator",values="impact_magnitude",fill_value=0);st.plotly_chart(px.imshow(m,text_auto=True,aspect="auto",title="Event-indicator association matrix"),use_container_width=True);st.dataframe(i,use_container_width=True)
with tabs[3]:
 s=st.selectbox("Scenario",["Base","Optimistic","Pessimistic"]);code=st.radio("Dimension",["ACC_OWNERSHIP","DIGITAL_PAYMENT"],horizontal=True);f=build_forecast(o,i,code,scenario=s);h=o[o.indicator_code.eq(code)].copy();h["year"]=h.observation_date.dt.year;fig=go.Figure();fig.add_scatter(x=h.year,y=h.value_numeric,mode="lines+markers",name="Observed");fig.add_scatter(x=f.year,y=f.forecast,mode="lines+markers",name="Forecast");fig.add_scatter(x=list(f.year)+list(f.year[::-1]),y=list(f.upper)+list(f.lower[::-1]),fill="toself",line={"width":0},name="95% interval",opacity=.2);st.plotly_chart(fig,use_container_width=True);st.dataframe(f.round(2))
with tabs[4]:
 s=st.select_slider("Scenario",options=["Pessimistic","Base","Optimistic"],value="Base");a=build_forecast(o,i,"ACC_OWNERSHIP",scenario=s);u=build_forecast(o,i,"DIGITAL_PAYMENT",scenario=s);st.plotly_chart(px.line(pd.concat([a.assign(dimension="Access"),u.assign(dimension="Usage")]),x="year",y="forecast",color="dimension",markers=True,title="2025–2027 projections"),use_container_width=True);st.progress(min(float(a.iloc[-1].forecast)/60,1.0),text="Access progress toward 60% analytical benchmark");st.progress(min(float(u.iloc[-1].forecast)/50,1.0),text="Usage progress toward 50% analytical benchmark")
st.info("Scenario-based decision support, not causal or official projections.")
