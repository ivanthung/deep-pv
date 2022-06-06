import pickle
import matplotlib.pyplot as plt

def test_results():
    file_name = 'test_results/sample1.pkl'
    with open(file_name, 'rb') as handle:
        results = pickle.load(handle)

    return results
