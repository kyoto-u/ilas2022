import pickle
 
with open('datas.pickle', mode='rb') as f:
    datas = pickle.load(f)
    print(datas)