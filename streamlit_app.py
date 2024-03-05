import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
latext=r'''
$$
\begin{array}{rl} x-1  ~~~~~~~\quad\quad\quad \\   x^2 +2x -1 ~\enclose{longdiv}{~ x^3+\phantom{5} x^2 -5x +4} &  \\      \underline{~~  x^3+2x^2 - \phantom{5} x  ~ \phantom{000} }& \\   -x^2 - 4x +4   \\      \underline{~~~~~~~ -x^2-2x+1  }& \\   -2x+3&  \\ \end{array}
$$
'''
# latext = r'''
# ## Latex example
# ### full equation 
# $$ 
# \Delta G = \Delta\sigma \frac{a}{b} 
# $$ 
# ### inline
# Assume $\frac{a}{b}=1$ and $\sigma=0$...  
# '''
st.write(latext)

num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

indices = np.linspace(0, 1, num_points)
theta = 2 * np.pi * num_turns * indices
radius = indices

x = radius * np.cos(theta)
y = radius * np.sin(theta)

df = pd.DataFrame({
    "x": x,
    "y": y,
    "idx": indices,
    "rand": np.random.randn(num_points),
})

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))
