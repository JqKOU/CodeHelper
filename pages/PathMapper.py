import sys 
sys.dont_write_bytecode = True
import streamlit as st
import re

st.set_page_config(
    page_title="PathMapper",
    page_icon="🚩",
    layout="wide"
)
def _max_width_():
    max_width_str = f"max-width: 1400px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    ) 
_max_width_()

backslash = "\\"

st.markdown("#### ➰ K Drive Path Converter for SAS EG and R Usage")
Kloc = st.text_input('Windows explorer path', value=r"K:\xover\cibmtr\biostats\projects")
if re.search('[a-zA-Z]', Kloc):
    Rloc = Kloc.replace(backslash , "/")
    EGloc = Rloc.replace('K:/xover/', "/netware/grpshare/")

st.markdown('SAS EG')
st.code(f'''{EGloc}''')
st.markdown('R')      
st.code(f'''{Rloc}''')


