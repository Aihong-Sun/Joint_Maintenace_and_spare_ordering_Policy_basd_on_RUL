'''
START DATE: 2021/9/28 10:56
use for implement discrete event simulation algorithm from :
张新辉,王雷震,赵斐.基于剩余寿命预测的维修与备件订购联合策略优化[J].工业工程,2020,23(4):106-113.
'''

from Params import args
import numpy as np
import sympy
import random
import matplotlib.pyplot as plt
# random.seed(64)

class DES:

    def __init__(self,args):
        self.args=args

    def B(self,t_k):
        sig=t_k
        return np.exp(-t_k ** 2 / (2 * sig ** 2)) / (np.sqrt(2 * np.pi) * sig)

    #计算累计退化量
    def X_t(self,t_k,l_k=None,x_k=None):
        B = self.B(t_k)
        if l_k!=None:
            B_tl=self.B(t_k+l_k)
            return x_k+self.args.u*l_k+self.args.sigma*(B_tl-B)
        else:
            return 75+self.args.u*t_k+self.args.sigma*B

    def chs_lk(self,xk,tk):
        lk=sympy.symbols("lk")
        f=xk+self.args.u*lk+self.args.sigma*(self.B(tk+lk)-self.B(tk))
        print(solve(f>0))
        return lk

    #剩余使用寿命：
    def l_t(self,x_t):
        return (self.args.L_c-x_t)/self.args.u

    def even1(self,TC,TL,t):
        TCi=TC+self.args.C_i+self.args.C_e0+self.args.C_R
        TL+=t
        return TCi,TL

    def even2(self,TC,TL,t,t0):
        TCi=TC+self.args.C_i+self.args.C_0+self.args.C_R+(t0+self.args.L-t)*self.args.C_s
        TL=Tl+t0+L
        return TCi,TL

    def even3(self,TC,TL,t,t0):
        TCi = TC + self.args.C_i + self.args.C_0 + self.args.C_R + (t - self.args.L - t0) * self.args.C_h
        TL = Tl + t
        return TCi, TL

    def even4(self,TC,TL,t):
        TCi = TC + self.args.C_i + self.args.C_e0 + self.args.C_F+self.args.C_R
        TL += t
        return TCi, TL

    def even5(self,TC,TL,t,t0):
        TCi = TC + self.args.C_i + self.args.C_0 + self.args.C_F + self.args.C_R + (
                    t0 + self.args.L - t) * self.args.C_s
        TL =TL+t0+L
        return TCi,TL

    def even6(self,TC,TL,t,t0):
        TCi = TC + self.args.C_i + self.args.C_0 + self.args.C_F + self.args.C_R + (
                t- self.args.L- t0) * self.args.C_h
        TL = TL + t
        return TCi, TL

    def main(self):
        q,LP=0,0, #总期望成本、总期望时长、订货阈值、预防性更换阈值
        EC_TOTAL=[]
        EC_set=[]
        TC_set=[]
        TL_set=[]


        for i in range(20):
            LP+=1
            EC = 9999
            for i in range(1000):
                q+=1
                TC, TL=0,0
                X_t=0
                t0=0
                T=0
                tk=random.randint(10,100)
                T+=tk
                TL+=tk
                xk=self.X_t(tk)     #随机产生一个退化量，根据式（2）
                # print(xk)
                lk=self.l_t(xk)     #根据式（6）
                X_t+=xk
                lk_set=[]
                # lk_set.append(lk)
                for i in range(self.args.N_max):
                    if lk-self.args.L<=q:
                        if t0==0:    #未订货
                            t0=T     #进行订货，此为订货时刻
                    if X_t<=LP:
                        pass
                    else:
                        if LP<=X_t and self.args.L_c>=X_t:  #预防性更换
                            if t0==0:            #未订购备件，事件1发生
                                TC,TL=self.even1(TC,TL,T)
                            elif t0<T<t0+L:    #配件已订购但未到货,事件2发生
                                TC, TL = self.even2(TC, TL, T,t0)
                            elif t0+L<=T:      #已到货，事件3发生
                                TC,TL=self.even3(TC,TL,T,t0)
                        elif X_t>=self.args.L_c:     #故障更换
                            if t0==0:  # 未订购备件，事件4发生
                                TC, TL = self.even4(TC, TL, T)
                            elif t0 < T < t0 + self.args.L:  # 配件已订购但未到货,事件5发生
                                TC,TL=self.even5(TC,TL,T,t0)
                            elif t0 + self.args.L <= T:  # 已到货，事件6发生
                                TC, TL = self.even6(TC, TL, T,t0)
                    T += self.args.T
                    xk = self.X_t(T)  # 随机产生一个退化量，根据式（2）
                    lk = self.l_t(xk)  # 根据式（6）
                    X_t+=xk
                    lk_set.append(lk)
                ECi=TC/TL
                print(ECi)
                if  ECi<EC:
                    EC=ECi
                else:
                    print("this is break point q",q)
                    break
            # print(TC)
            EC_set.append(EC)
            TC_set.append(TC)
            TL_set.append(TL_set)
        x=[i for i in range(20)]
        plt.plot(x,EC_set)
        plt.xlabel("LP")
        plt.ylabel("TC")
        plt.show()

        return EC,q,LP

d=DES(args)
EC,Q,LP=d.main()
print(EC,Q,LP)









