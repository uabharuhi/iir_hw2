import _pickle as  pickle # cPicle
#ir_sys = ir.IRSystem()
def init_ir_system():
    with open('./temp/ir_sys.pkl', mode='rb') as f:
        ir_sys = pickle.load(f) 
        return ir_sys
