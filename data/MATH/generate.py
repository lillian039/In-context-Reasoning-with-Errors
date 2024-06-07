from get_random_train_example import get_sample_examples,load_math_data
import os
import json

if not os.path.exists('algebra'):
    os.mkdir('algebra')
if not os.path.exists('counting_and_probability'):
    os.mkdir('counting_and_probability')
if not os.path.exists('geometry'):
    os.mkdir('geometry')
if not os.path.exists('intermediate_algebra'):
    os.mkdir('intermediate_algebra')
if not os.path.exists('number_theory'):
    os.mkdir('number_theory')
if not os.path.exists('prealgebra'):
    os.mkdir('prealgebra')
if not os.path.exists('precalculus'):
    os.mkdir('precalculus')


for i in range(7):
    for j in range(6):
        load_math_data(math_type=i, difficulty=j)
    get_sample_examples(math_type=i)
