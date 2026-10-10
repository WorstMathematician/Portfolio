"""Quarterly program-level public finance exploration, no predictive model yet."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
import plotly.express as px
import pandas as pd
import streamlit as st
from src.program_panel import load_panel, quarterly_panel, panel_diagnostics

ROOT=Path(__file__).resolve().parents[2]
st.set_page_config(page_title='Program Expenditure Explorer',page_icon='📊',layout='wide')
st.title('Program-level expenditure explorer')
st.caption('Public Measure H ongoing program and agency allocations · FY 2023–24 and FY 2024–25')
st.warning('These are published historical expenditures, not predicted program outcomes. Only eight fiscal quarters are available in the comparable panel.')

@st.cache_data
def data():
    return load_panel(ROOT/'data'/'ongoing_program_agency_2023_2025.csv',ROOT/'data'/'annual_quarterly_totals.csv')
panel,report=data()
summary=panel_diagnostics(panel)
a,b,c,d=st.columns(4)
a.metric('Program-agency years',summary['program_agency_year_rows'])
b.metric('Quarterly observations',summary['quarterly_observations'])
c.metric('Distinct programs',summary['distinct_programs'])
d.metric('Both-year program-agency pairs',summary['pairs_present_both_years'])
with st.expander('Financial source reconciliation',expanded=False):
    st.dataframe(report,use_container_width=True,hide_index=True)
    st.caption('Printed dashes in County tables are represented as numeric zero. Original pages are linked per row. Differences of at most USD 1 are permitted for published rounding.')
programs=st.multiselect('Program',sorted(panel.program.unique()),default=[])
agencies=st.multiselect('Agency',sorted(panel.agency.unique()),default=[])
filtered=panel.copy()
if programs: filtered=filtered.loc[filtered.program.isin(programs)]
if agencies: filtered=filtered.loc[filtered.agency.isin(agencies)]
if filtered.empty:
    st.info('No records match the chosen filters.');st.stop()
long=quarterly_panel(filtered)
long['label']=long.fiscal_year+' Q'+long.quarter.astype(str)
st.subheader('Quarterly expenditure actuals')
long['series']=long.program+' · '+long.agency
fig=px.line(long,x='label',y='expenditure_usd',color='series',markers=True)
fig.update_layout(xaxis_title='Fiscal quarter',yaxis_title='USD',hovermode='x unified',legend_title_text='Program · Agency')
st.plotly_chart(fig,use_container_width=True)
st.subheader('Year-over-year program allocations and expenditure')
comparison=filtered[['program','agency','fiscal_year','allocation_usd','reported_ytd_usd']].copy()
comparison['program_agency']=comparison.program+' · '+comparison.agency
melt=comparison.melt(id_vars=['program_agency','fiscal_year'],value_vars=['allocation_usd','reported_ytd_usd'],var_name='measure',value_name='usd')
st.plotly_chart(px.bar(melt,x='program_agency',y='usd',color='fiscal_year',facet_row='measure',barmode='group',height=650),use_container_width=True)
st.subheader('Reported program records')
st.dataframe(filtered,hide_index=True,use_container_width=True,column_config={'source_url':st.column_config.LinkColumn('Official report')})
st.download_button('Export selection (source records)',filtered.to_csv(index=False),'selected_program_records.csv','text/csv')
st.download_button('Export quarterly panel',long.to_csv(index=False),'program_quarterly_panel.csv','text/csv')