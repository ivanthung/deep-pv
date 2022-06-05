import pickle
import matplotlib.pyplot as plt

file_name = 'test_results/sample1.pkl'

with open(file_name, 'rb') as handle:
    results = pickle.load(handle)

mask = results[0][0]['masks'][:,:,0]
plt.imshow(mask)
