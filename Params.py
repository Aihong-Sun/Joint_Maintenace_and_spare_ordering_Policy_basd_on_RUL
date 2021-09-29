'''
START DATE:2021/9/28  10:25
BASED ON THESIS:张新辉,王雷震,赵斐.基于剩余寿命预测的维修与备件订购联合策略优化[J].工业工程,2020,23(4):106-113.
'''

import random
import argparse

#Parameters Initialization
parser=argparse.ArgumentParser()

#cost parameters
parser.add_argument("--C_i",type=float,default=500,help="Cost parameter Ci")
parser.add_argument("--C_0",type=float,default=100,help="Cost parameter C0")
parser.add_argument("--C_e0",type=float,default=4000,help="Cost parameter C_e0")
parser.add_argument("--C_R",type=float,default=1200,help="Cost parameter C_R")
parser.add_argument("--C_F",type=float,default=50000,help="Cost parameter C_F")
parser.add_argument("--C_s",type=float,default=250,help="Cost parameter C_s")
parser.add_argument("--C_h",type=float,default=50,help="Cost parameter C_h")

# Degradation Parameters
parser.add_argument("--u",type=float,default=-0.01478)
parser.add_argument("--sigma",type=float,default=0.39997)
parser.add_argument("--L_p",type=float,default=0)       #预防性更换
parser.add_argument("--L_c",type=float,default=0,help="Fault threshold")    #故障更换
parser.add_argument("--N_max",type=float,default=100)       #迭代次数
parser.add_argument("--T",type=int,default=100)   #按论文还可修改为：50，100，150，200，250，300，350
parser.add_argument("--L",type=int,default=100)     #按论文还可修改为：300，500，1000，1500，2000，2500，3000

args=parser.parse_args()
# print(args.C_i)



