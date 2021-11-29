import numpy as np
import matplotlib.pyplot as plt
import LoadData as ld
from scipy.optimize import minimize
from scipy.integrate import quad
import itertools

plt.rcParams.update({
  "text.usetex": True,
  "font.family": "Helvetica",
  "font.size": 12
})

#loading data
data_16, data_17, data_18, array16, array17, array18 = ld.Data()
data_tot, dataTot, arrayTot = ld.TotalDataSet(data_16, data_17, data_18)
data_ta16, data_tf16, data_ta17, data_tf17, data_ta18, data_tf18 = ld.loadFill()     
FillNumber16, FillNumber17, FillNumber18 = ld.FillNumber()
data_16_sec, data_ta16_sec, data_tf16_sec, data_17_sec, data_ta17_sec,\
   data_tf17_sec, data_18_sec, data_ta18_sec, data_tf18_sec=ld.Data_sec(array16,\
      data_ta16, data_tf16, array17, data_ta17, data_tf17, array18, data_ta18, data_tf18)

#loading fit parameters and data
f=open('Data/a_16_4Par.txt',"r")
lines=f.readlines()
a_16=[]
for x in lines:
    a_16.append(float(x.split(' ')[0]))  

f.close()

f=open('Data/b_16_4Par.txt',"r")
lines=f.readlines()
b_16=[]
for x in lines:
    b_16.append(float(x.split(' ')[0]))  

f.close()

f=open('Data/c_16_4Par.txt',"r")
lines=f.readlines()
c_16=[]
for x in lines:
    c_16.append(float(x.split(' ')[0]))  

f.close()

f=open('Data/d_16_4Par.txt',"r")
lines=f.readlines()
d_16=[]
for x in lines:
    d_16.append(float(x.split(' ')[0]))  

f.close()

f=open('Data/ts_16_4Par.txt',"r")
lines=f.readlines()
ts_16=[]
for x in lines:
    ts_16.append(float(x.split(' ')[0]))  

f.close()

f=open('Data/L_int_2016_4Par.txt',"r")
lines=f.readlines()
L_int_2016=[]
for x in lines:
    L_int_2016.append(float(x.split(' ')[0]))  

f.close()


#define the fill times, the turnaround times and the model parameters
S=range(0, len(ts_16), 1)
combination_2=set(itertools.combinations(S, 2))

ts_tot_16=np.array(ts_16)
ta=np.array(data_ta16_sec)
a_tot_16=np.array(a_16)
b_tot_16=np.array(b_16)
c_tot_16=np.array(c_16)
d_tot_16=np.array(d_16)

#Total and integrated luminosity initial values
L_int_tot_2016=np.array(L_int_2016)
L_tot_tot_2016=np.sum(L_int_tot_2016)

#define total luminosity for evaluating the distribution
L_tot_test=[]

#saving optimized times
with open('Data/res_2016_4Par_2Fill.txt', 'w') as fz:
        fz.write('')
        fz.close()

for k in combination_2:
    
    #redefining the fill times, the turnaround times and the model parameters
    a_16=np.delete(a_tot_16, k)
    b_16=np.delete(b_tot_16, k)
    c_16=np.delete(c_tot_16, k)
    d_16=np.delete(d_tot_16, k)
    ts_16=np.delete(ts_tot_16, k)
    newFillNumber16=np.delete(FillNumber16, k)
    
    
    #Total and integrated luminosity
    L_int_2016=np.delete(L_int_tot_2016, k)
    L_tot_2016=np.sum(L_int_2016)
    
    #Objective Function
    def fun(t1):
        result=np.empty(len(x0))
        for i in range(len(x0)):
            lam=lambda x1: a_16[i]*np.exp(-(b_16[i]*x1))+c_16[i]*np.exp(-d_16[i]*x1)
            result[i]=-quad(lam, 0, t1[i])[0]
            
        result = np.sum(result)
        return result

    #constraint
    def cons(t1):
        res = np.sum(t1) - (tot)
        return res

    #jacobian of the objective function
    def jacb(t1):
        der=-a_16*np.exp(-(b_16*t1))-c_16*np.exp(-d_16*t1)
        #result=np.sum(der)
        return der
            
        
    #Initial guesses    
    x0=ts_16

    #constraint determination
    tot=sum(x0)+ts_tot_16[k[0]]+ta[k[0]]+ts_tot_16[k[1]]+ta[k[1]]

    #bounds
    list=[[1800,86400]]
    for li in range(1, len(a_16)):
        list=list+[[1800, 86400]]
        
    bnd=list

    #optimization
    res = minimize(fun, x0, options={'disp': False, 'maxiter':10000}, constraints={'type':'eq', 'fun': cons, 'jac': lambda x: np.ones(len(x0))}, jac=jacb, method='SLSQP', bounds=bnd)   
 
    for el in res.x:
        with open('Data/res_2016_4Par_2Fill.txt', 'a') as fz:
            fz.write(str(el))
            fz.write('\n')
 
    #Defining Integrated and total optimized Luminodity
    def fun1(t1):
        result=np.empty(len(x0))
        for i in range(len(x0)):
            lam=lambda x1: a_16[i]*np.exp(-(b_16[i]*x1))+c_16[i]*np.exp(-d_16[i]*x1)
            result[i]=quad(lam, 0, t1[i])[0]
        return result

    L_int_opt=fun1(res.x)
    L_tot_opt=np.sum(L_int_opt)

    #comparison between real and optimized times
    fig, ax1= plt.subplots()
    ax1.hist(x0/3600, facecolor='steelblue', density=True, alpha=0.4, label="Real Fill Times" )
    ax1.hist(res.x/3600, color='red', histtype='step', density=True, label="Optimized Fill Times")
    ax1.set_xlabel(r'Times [$\mathrm{h}$]')
    ax1.set_ylabel(r'Normalized Frequencies')
    ax1.set_title('2016')
    plt.legend(loc='best')
    plt.savefig('Test2_16_4Par/2016_4Par_{}.pdf'.format(k))

    #(res.x) Vs FillNumber
    fig, ax1= plt.subplots()
    ax1.axhline(1800/3600, color='r', linestyle='dashed', linewidth=1)
    ax1.axhline(24, color='r', linestyle='dashed', linewidth=1)
    ax1.plot(newFillNumber16, res.x/3600, linestyle="", marker='o')
    ax1.set_ylabel(r'Optimized Times [$\mathrm{h}$]')
    ax1.set_xlabel(r'Fill Number')
    ax1.set_title('2016')
    plt.savefig('Test2_16_4Par/2016_4Par_ratio_{}.pdf'.format(k))
    

    #comparison between real and optimized integrated luminosity
    fig, ax1= plt.subplots()
    ax1.hist(L_int_2016/1e9,  facecolor='steelblue', density=True, alpha=0.4, label="Real Integrated Luminosities" )
    ax1.hist(L_int_opt/1e9, color='red', histtype='step', density=True, label="Optimized Integrated Luminosities")
    ax1.set_xlabel(r'Integrated Luminosity [$\mathrm{fb}^{-1}$]')
    ax1.set_ylabel(r'Normalized Frequencies')
    ax1.set_title('2016')
    plt.plot([],[], "k.", label=r'Initial $L_{\mathrm{tot}}$='+'{:.2f}'.format(L_tot_2016/1e9)+r' [$\mathrm{fb}^{-1}$]')
    plt.plot([],[], "k.", label=r'Optimized $L_{\mathrm{tot}}$='+'{:.2f}'.format(L_tot_opt/1e9)+r' [$\mathrm{fb}^{-1}$]')
    plt.legend(loc='upper left')
    plt.savefig('Test2_16_4Par/2016_4Par_lumi_{}.pdf'.format(k))

    def fun2(t1):
        result=np.empty(len(x0))
        for i in range(len(x0)):
            result[i]=a_16[i]*np.exp(-(b_16[i]*t1[i]))+c_16[i]*np.exp(-d_16[i]*t1[i])
        return result

    #Istantaneous ending luminosities for optimized times
    fig, ax1= plt.subplots()
    L_ist=fun2(res.x)
    ax1.hist(L_ist,  facecolor='steelblue', density=True)
    ax1.set_xlabel(r'Istantaneous Luminosities [Hz/$\mu$b]')
    ax1.set_ylabel(r'Normalized Frequencies')
    ax1.set_title('2016')
    plt.savefig('Test2_16_4Par/2016_4Par_istLumi_{}.pdf'.format(k))
    
    L_tot_test.append(L_tot_opt)


L_tot_test=np.array(L_tot_test)
#comparison between real and optimized integrated luminosity
fig, ax1= plt.subplots()
ax1.hist(L_tot_test/1e9, facecolor='steelblue', density=True, alpha=0.4)
ax1.axvline(np.average(L_tot_test/1e9), color='r', linestyle='dashed', linewidth=1, label="Mean Value={:.2f}".format(np.average(L_tot_test/1e9))+r' [$\mathrm{fb}^{-1}$]')
ax1.axvline(np.average(L_tot_tot_2016/1e9), color='b', linestyle='dashed', linewidth=1, label="Real $L_{\mathrm{tot}}$="+"{:.2f}".format(L_tot_tot_2016/1e9)+ r' [$\mathrm{fb}^{-1}$]')
ax1.plot([],[], "k.", label="Sigma={:.2f}".format(np.std(L_tot_test/1e9))+r' [$\mathrm{fb}^{-1}$]')
ax1.set_xlabel(r'Total Luminosity [$\mathrm{fb}^{-1}$]')
ax1.set_ylabel(r'Normalized Frequencies')
ax1.set_title('Distribution of Total Luminosities 2016')
plt.legend(loc='best')
plt.savefig('Test2_16_4Par/2016_4Par_Test.pdf')


with open('Data/L_tot_2016_4Par_Measured_Real_2Fills.txt', 'w') as f:
        f.write('')
        f.close()
for el in L_tot_test:
    with open('Data/L_tot_2016_4Par_Measured_Real_2Fills.txt', 'a') as f:
        f.write(str(el))
        f.write('\n')
        
        
with open('Data/L_tot_evaluated_2016_4Par_Measured_Real_2Fill.txt', 'w') as f:
        f.write('')
        f.write(str(L_tot_tot_2016))
        f.close()
  