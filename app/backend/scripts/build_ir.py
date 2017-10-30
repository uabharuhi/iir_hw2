import pickle
from  backend.ir import  IRSystem



ir_sys = IRSystem()


with open("./temp/ir_sys.pkl", mode='wb') as f:
   pickle.dump(ir_sys,f)