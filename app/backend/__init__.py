import _pickle as  pickle # cPicle
#ir_sys = ir.IRSystem()
def init_ir_system(tokenizeType='normal'):
    with open('./temp/%s/ir_sys.pkl'%(tokenizeType), mode='rb') as f:
        ir_sys = pickle.load(f) 
        return ir_sys
