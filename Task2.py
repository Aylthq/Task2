from urllib.request import urlopen
import scipy.special as sps
import matplotlib.pyplot as pp
import numpy as np
import re

class RCS:
    
 def __init__(self, D, f):
     r = D/2
     l = 3e10/f
     k = 2*np.pi/l
     res = 0
     for n in range(1,10):
         res+= (-1)**n*(n+0.5)*(self.b(n, k*r)-self.a(n,k*r))
     self.res = np.abs(res)**2*l**2/np.pi
    
 def h(self, n, x):
     return sps.spherical_jn(n, x)+1j*sps.spherical_yn(n, x)
   
 def a(self, n, x):
     return sps.spherical_jn(n, x)/self.h(n, x)

 def b(self, n, x):
     return (x*sps.spherical_jn(n-1, x)-n*sps.spherical_jn(n, x))/(x*self.h(n-1,x)-n*self.h(n,x))

class Result:
    
    def __init__(self, D, fmin, fmax):
        self.fmin = fmin
        self.fmax = fmax
        self.f = np.linspace(fmin,fmax,101)
        self.res = RCS(D, self.f).res
        fig, ax = pp.subplots()
        ax.set_xlim(fmin,fmax)
        ax.set_xlabel("f, Гц")
        ax.set_ylabel("σ, м^2")
        ax.plot(self.f, self.res)
        pp.show()
        
    def output(self):
        f = open("Task2_res.txt", "x")
        for i in range(len(self.f)):
         f.write("{x}    {f}\n".format(x=self.f[i],f=self.res[i]))
        f.close()
                    
                        
s = str(urlopen("https://jenyay.net/uploads/Student/Modelling/task_rcs.xml").read())
n = s.find('number="2"')
s = s[n:s.find('/', n)]
D = float(re.search('(?<=D=")\d+\.?\d*e?-?\d?(?=")', s).group())
fmin = float(re.search('(?<=fmin=")\d+\.?\d*e?-?\d?(?=")', s).group())
fmax = float(re.search('(?<=fmax=")\d+\.?\d*e?-?\d?(?=")', s).group())
res = Result(D, fmin, fmax)
res.output()
        
    
     
