import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.integrate import quad
from RealIntegratedLuminosity import L_int_summary_16


plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Helvetica",
  "font.size": 12
})

#loading fit parameters and data
f=open('Data/a_16_2Par.txt',"r")
lines=f.readlines()
a_16=[]
for x in lines:
    a_16.append(float(x.split(' ')[0]))  

f.close()

f=open('Data/b_16_2Par.txt',"r")
lines=f.readlines()
b_16=[]
for x in lines:
    b_16.append(float(x.split(' ')[0]))  

f.close()


f=open('Data/ts_16_2Par.txt',"r")
lines=f.readlines()
ts_16=[]
for x in lines:
    ts_16.append(float(x.split(' ')[0]))  

f.close()

f=open('Data/L_int_2016_2Par.txt',"r")
lines=f.readlines()
L_int_2016=[]
for x in lines:
    L_int_2016.append(float(x.split(' ')[0]))  

f.close()


#model parameters and initial guesses
ts_16=np.array(ts_16)
a_16=np.array(a_16)
b_16=np.array(b_16)

#Total and integrated luminosity initial values
L_int_2016_2Par=np.array(L_int_2016)
L_tot_2016_2Par=np.sum(L_int_2016_2Par)

#Objective Function
def fun(t1):
    result=np.empty(len(x0))
    for i in range(len(x0)):
        lam=lambda x1: a_16[i]*np.exp(-(b_16[i]*x1))
        result[i]=-quad(lam, 0, t1[i])[0]
        
    result = np.sum(result)
    return result

#constraint
def cons(t1):
    res = np.sum(t1) - (tot)
    return res

#jacobian of the objective function
def jacb(t1):
    der=-a_16*np.exp(-(b_16*t1))
    #result=np.sum(der)
    return der

#Initial guesses    
x0=ts_16

#constraint determination
tot=sum(x0)

#bounds
list=[[1800,86400]]
for li in range(1, len(a_16)):
    list=list+[[1800, 86400]]
    
bnd=list


#optimization
res = minimize(fun, x0, options={'disp': True, 'maxiter':10000}, constraints={'type':'eq', 'fun': cons, 'jac': lambda x: np.ones(len(x0))}, jac=jacb, method='SLSQP', bounds=bnd) 

#Defining Integrated and total optimized Luminodity
def fun1(t1):
    result=np.empty(len(x0))
    for i in range(len(x0)):
        lam=lambda x1: a_16[i]*np.exp(-(b_16[i]*x1))
        result[i]=quad(lam, 0, t1[i])[0]
    return result

L_int_opt=fun1(res.x)
L_tot_opt=np.sum(L_int_opt)

#comparison between real and optimized times
fig, ax1= plt.subplots()
ax1.hist(x0/3600, facecolor='steelblue', density=True, alpha=0.4, label="Real Fill Times" )
ax1.hist(res.x/3600, color='red', histtype='step', density=True, label="Optimized Fill Times")
ax1.set_xlabel(r'Times [$\mathrm{h}$]')
ax1.set_ylabel('Normalized Frequencies')
ax1.set_title('2016')
plt.legend(loc='best')
plt.savefig('OptimizationResults/2016_2Par.pdf')
plt.show()

#comparison between real and optimized integrated luminosity
fig, ax1= plt.subplots()
ax1.hist(L_int_2016_2Par/1e9, facecolor='steelblue', density=True, alpha=0.4, label="Real Integrated Luminosities" )
ax1.hist(L_int_opt/1e9, color='red', histtype='step', density=True, label="Optimized Integrated Luminosities")
ax1.set_xlabel(r'Integrated Luminosity [$\mathrm{fb}^{-1}$]')
ax1.set_ylabel('Normalized Frequencies')
ax1.set_title('2016')
ax1.plot([],[], "k.", label=r'Initial $L_{\mathrm{tot}}$='+'{:.2f}'.format(L_tot_2016_2Par/1e9)+r' [$\mathrm{fb}^{-1}$]')
ax1.plot([],[], "k.", label=r'Optimized $L_{\mathrm{tot}}$='+'{:.2f}'.format(L_tot_opt/1e9)+r' [$\mathrm{fb}^{-1}$]')
plt.legend(loc='upper left')
plt.savefig('OptimizationResults/2016_2Par_lumi.pdf')
plt.show()


def fun2(t1):
    result=np.empty(len(x0))
    for i in range(len(x0)):
        result[i]=a_16[i]*np.exp(-(b_16[i]*t1[i]))
    return result

#Istantaneous ending luminosities for optimized times
fig, ax1= plt.subplots()
L_ist=fun2(res.x)
ax1.hist(L_ist,  facecolor='steelblue', density=True)
ax1.set_xlabel(r'Istantaneous Luminosities [Hz/$\mu$b]')
ax1.set_ylabel('Normalized Frequencies')
ax1.set_title('2016')
plt.savefig('OptimizationResults/2016_2Par_istLumi.pdf')
plt.show()


#comparison between real and optimized integrated luminosity
fig, ax1= plt.subplots()
ax1.hist(L_int_2016_2Par/1e9,  facecolor="green", alpha=0.3, density=True, label="Real Integrated Luminosities" )
ax1.hist(L_int_summary_16/1e9, histtype='step', density=True, label="Measured Integrated Luminosity")
ax1.set_xlabel(r'Integrated Luminosity [$\mathrm{fb}^{-1}$]')
ax1.set_ylabel('Normalized Frequencies')
ax1.set_title('2016')
plt.legend(loc='upper left')
plt.savefig('OptimizationResults/2016_2Par_Real_Measured_Lumi.pdf')
plt.show()

with open('Data/L_tot_2016_2Par.txt', 'w') as f:
        f.write('')
        f.write(str(L_tot_opt))
        f.close()