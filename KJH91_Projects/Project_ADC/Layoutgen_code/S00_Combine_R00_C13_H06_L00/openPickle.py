import dill as pickle

with open('LayoutObj.pkl', 'rb') as f:
    data_loaded = pickle.load(f)

print(data_loaded)