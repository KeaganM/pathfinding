from hypothesis import given,strategies
import hypothesis.strategies as st
from hypothesis.extra.numpy import arrays as hypo_array
import numpy as np

# test = hypo_array(dtype=np.int,shape=(5,5),elements=st.integers(0,1))

@strategies.extend(Test)
def test_strategy():

