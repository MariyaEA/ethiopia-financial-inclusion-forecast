from pathlib import Path
import pandas as pd
REQ={"record_id","record_type","parent_id","pillar","indicator_code","value_numeric","observation_date","confidence"}
def load_unified_data(path):
 p=Path(path)
 if not p.exists(): raise FileNotFoundError(f"Dataset not found: {p}")
 df=pd.read_csv(p); missing=REQ-set(df.columns)
 if missing: raise ValueError(f"Missing columns: {sorted(missing)}")
 df["observation_date"]=pd.to_datetime(df["observation_date"],errors="coerce"); df["value_numeric"]=pd.to_numeric(df["value_numeric"],errors="coerce"); return df
def split_records(df): return {k:df[df.record_type.eq(k)].copy() for k in ["observation","event","impact_link","target"]}
def validate_schema(df):
 e=[]; event_ids=set(df.loc[df.record_type.eq("event"),"record_id"]); orphans=df.loc[df.record_type.eq("impact_link") & ~df.parent_id.isin(event_ids),"record_id"].tolist()
 if orphans:e.append(f"Orphaned impact links: {orphans}")
 if df.loc[df.record_type.eq("event"),"pillar"].fillna("").str.strip().ne("").any():e.append("Events must have blank pillar")
 return e
