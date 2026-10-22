"""Interactive historical data explorer, readiness gate, and hypothetical scenario calculator."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pandas as pd
import plotly.express as px
import streamlit as st
from src.pipeline import load_and_validate, long_form, contiguous_scope_segments, diagnostics
from src.models import evaluate_eligibility

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'/'annual_quarterly_totals.csv'
st.set_page_config(page_title='Program Finance Intelligence',page_icon='📈',layout='wide')
st.markdown('''<style>
.block-container {max-width:1320px; padding-top:1.4rem}
h1,h2,h3 {letter-spacing:-.03em}
div[data-testid="stMetric"] {padding:1rem;border:1px solid rgba(140,150,160,.28);border-radius:14px}
</style>''',unsafe_allow_html=True)

@st.cache_data
def get_data():
    annual,recon=load_and_validate(DATA)
    quarter=long_form(annual)
    annual_diag,outliers=diagnostics(quarter)
    return annual,pd.DataFrame(recon),quarter,annual_diag,outliers,contiguous_scope_segments(quarter)

annual,recon,quarter,annual_diag,outliers,segments=get_data()
eligibility=evaluate_eligibility(quarter)
st.title('Program Finance Intelligence')
st.caption('LA County Measure H public expenditure research · Audited quarterly totals · Experimental analytics application')
st.warning('Independent educational tool, not an official County forecasting service. Historic reporting scopes differ; confirmed model performance is withheld.')
scope=st.selectbox('Reporting definition',['ongoing','comprehensive','unclassified'],help='Do not pool different financial scopes without an audited crosswalk.')
subset=quarter.loc[quarter.scope.eq(scope)].copy()
years=annual.loc[annual.scope.eq(scope)].copy()
if subset.empty:
    st.stop()
latest=years.iloc[-1]
c1,c2,c3,c4=st.columns(4)
c1.metric('Reports in scope',len(years))
c2.metric('Quarterly observations',len(subset))
c3.metric('Latest annual spending',f'USD {float(latest.reported_ytd_usd)/1e6:,.1f}M')
c4.metric('Latest allocation',f'USD {float(latest.allocation_usd)/1e6:,.1f}M')
overview,quality,anomalies,model_lab,scenarios,sources=st.tabs(
    ['Overview','Data quality','Anomalies and trends','Model laboratory','Scenario planner','Sources'])
with overview:
    st.subheader('Observed historical expenditures')
    subset['period']=subset.fiscal_year+' Q'+subset.quarter.astype(str)
    fig=px.line(subset,x='period',y='expenditure_usd',markers=True,title='Actuals, not predictions')
    fig.update_layout(xaxis_title='Fiscal quarter',yaxis_title='USD')
    st.plotly_chart(fig,use_container_width=True)
    st.subheader('Quarterly expenditure composition')
    st.plotly_chart(px.bar(subset,x='fiscal_year',y='expenditure_usd',
        color=subset.quarter.map(lambda x:f'Q{x}'),barmode='stack'),use_container_width=True)
    st.dataframe(annual_diag.loc[annual_diag.scope.eq(scope)],hide_index=True,use_container_width=True)
with quality:
    st.subheader('Quarterly-to-annual reconciliation')
    st.dataframe(recon.loc[recon.scope.eq(scope)],hide_index=True,use_container_width=True)
    st.info('All eight fiscal-year records reconcile within 1 USD. Comparability is a separate requirement.')
    st.subheader('Independent comparable reporting segments')
    st.dataframe(segments,hide_index=True,use_container_width=True)
with anomalies:
    st.subheader('Within-year profiles')
    st.plotly_chart(px.line(subset,x='quarter',y='expenditure_usd',color='fiscal_year',
        markers=True),use_container_width=True)
    st.subheader('Statistical anomaly register')
    st.caption('Quarter-adjusted robust MAD z-scores are only considered when at least three other reference years exist. Source values are never deleted automatically.')
    st.dataframe(outliers.loc[outliers.scope.eq(scope)],hide_index=True,use_container_width=True)
with model_lab:
    st.subheader('Candidate model readiness')
    if eligibility['status']=='blocked':
        st.error('Model comparison blocked. Fewer than 24 consecutive, comparable quarters per scope.')
    else:
        st.success('Initial history gate met; models still require rolling-origin validation.')
    st.metric('Longest comparable run',str(eligibility['maximum_contiguous_comparable_quarters'])+
        ' / '+str(eligibility['required_quarters'])+' quarters')
    for item in eligibility['models']:
        with st.expander(item['model'].replace('_',' ').title()):
            st.json(item)
    st.caption('No training or model performance has been claimed. Planned backtest: 1Q/2Q/4Q horizons, MAE, MASE, bias, calibrated interval coverage.')
with scenarios:
    st.subheader('Hypothetical financial stress test')
    st.info('Calculator built on last observed annual actual, NOT a trained prediction.')
    g=st.slider('Hypothetical spending change (%)',-30,40,5)
    a=st.slider('Hypothetical funding change (%)',-30,40,0)
    r=st.slider('Spending realization (%)',70,110,100,5)
    projected=float(latest.reported_ytd_usd)*(1+g/100)*(r/100)
    budget=float(latest.allocation_usd)*(1+a/100)
    x,y,z=st.columns(3)
    x.metric('Scenario expenditure',f'USD {projected/1e6:.2f}M')
    y.metric('Scenario funding',f'USD {budget/1e6:.2f}M')
    z.metric('Gap (+) / headroom (-)',f'USD {(projected-budget)/1e6:+.2f}M')
    scenario=pd.DataFrame([{'scope':scope,'observed_baseline_fy':latest.fiscal_year,
       'spending_change_pct':g,'funding_change_pct':a,'realization_pct':r,
       'scenario_spending_usd':projected,'scenario_funding_usd':budget,'gap_usd':projected-budget}])
    st.download_button('Export scenario',scenario.to_csv(index=False),'scenario.csv','text/csv')
with sources:
    st.subheader('Official source documents')
    st.dataframe(years[['fiscal_year','scope','source_url','verification_note']],hide_index=True,
        use_container_width=True,column_config={'source_url':st.column_config.LinkColumn('Original report')})
    st.download_button('Export audited annual totals',annual.to_csv(index=False),'annual.csv','text/csv')
    st.caption('Public report total rows were transcribed by hand; program/agency-level extraction and reconciliation are separate future milestones.')
