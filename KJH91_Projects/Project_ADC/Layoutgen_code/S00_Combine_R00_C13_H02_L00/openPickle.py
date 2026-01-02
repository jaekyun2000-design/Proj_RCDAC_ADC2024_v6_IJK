import dill as pickle

with open('LayoutObj_version7.pkl', 'rb') as f:
    data_loaded = pickle.load(f)

print(data_loaded)