import numpy as np


def calc_glucosa_canal(x,y, promCanal):
    n = len(x)
    x = np.array(x)
    y = np.array(y)
    sumx = sum(x)
    sumy = sum(y)
    sumx2 = sum(x*x)
    sumy2  = sum(y*y)
    sumxy = sum(x*y)
    promx = sumx/n
    promy = sumy/n

    m  = (sumx*sumy - n*sumxy)/(sumx**2 - n*sumx2)
    b = promy - m*promx

    sigmax = np.sqrt(sumx2/n - promx**2)
    sigmay = np.sqrt(sumy2/n - promy**2)
    sigmaxy = sumxy/n - promx*promy
    R2= (sigmaxy/(sigmax*sigmay))**2
    R= (sigmaxy/(sigmax*sigmay))

    valorGlucosa  = (promCanal - b)/m

    valores = {
        "m" : m,
        "b" : b,
        "valorGlucosa" : valorGlucosa,
        "sigmax": sigmax,
        "sigmay": sigmay,
        "sigmaxy": sigmaxy,
        "R2": R2,
        "R": R
    }
    return valores

# x = [85, 96, 99, 99, 104, 108, 112, 120, 133, 176, 178, 232, 259, 264, 272, 272, 313, 340]
# yr = [2022.78000, 1920.66832, 2078.43013, 2055.86000, 2102.65423, 2619.65462, 2013.92241, 1903.74000, 2099.17020, 1731.57000, 2490.49000, 2221.63000, 2294.15000, 2647.94000, 2423.32288, 1530.64000, 2578.86000, 2728.69000]
# ys = [654.42413, 614.61275, 654.29890, 644.35920, 670.49985, 826.42413, 705.31118, 675.95000, 684.81683, 585.76000, 842.59433, 715.55837, 717.77216, 857.20200, 785.38696, 553.64957, 802.11000, 862.36193]
# yt = [157.42217, 145.96809, 154.61032, 155.47235, 162.18383, 196.84441, 172.03994, 162.61, 167.23723, 144.54, 199.42682, 171.35384, 176.71511, 202.17123, 187.17229, 135.5842, 192.74, 207.31699]
# yu = [76.44825,  71.36185, 76.45268, 75.58916, 79.57455, 97.79102, 82.8957, 77.53, 81.35374, 71.67024, 97.26675, 83.51248, 88.67449, 99.54885, 91.89046, 65.02795, 96.03319, 104.05137]
# yv = [111.45944, 105.00594, 115.10267, 103.05131, 117.81616, 147.25443, 111.56882, 104.77, 116.54957, 101.9589, 137.7031, 122.29208, 133.02436, 148.71936, 134.33377, 84.9387, 147.02004, 156.62996]
# yw = [75.52525, 70.6481, 77.01144, 73.38042, 78.61585, 97.05947, 76.4505, 73.08, 78.09713, 67.51167, 93.38723, 82.09608, 86.97564, 99.11121, 89.46669, 58.34967, 95.66114, 102.16923]

x = [85, 96, 99, 99, 104, 108, 112, 120, 133, 178, 232, 259, 264, 272, 313, 340]
yr = [2022.78000, 1920.66832, 2078.43013, 2055.86000, 2102.65423, 2619.65462, 2013.92241, 1903.74000, 2099.17020, 2490.49000, 2221.63000, 2294.15000, 2647.94000, 2423.32288, 2578.86000, 2728.69000]
ys = [654.42413, 614.61275, 654.29890, 644.35920, 670.49985, 826.42413, 705.31118, 675.95000, 684.81683, 842.59433, 715.55837, 717.77216, 857.20200, 785.38696, 802.11000, 862.36193]
yt = [157.42217, 145.96809, 154.61032, 155.47235, 162.18383, 196.84441, 172.03994, 162.61, 167.23723, 199.42682, 171.35384, 176.71511, 202.17123, 187.17229, 192.74, 207.31699]
yv = [111.45944, 105.00594, 115.10267, 103.05131, 117.81616, 147.25443, 111.56882, 104.77, 116.54957, 137.7031, 122.29208, 133.02436, 148.71936, 134.33377, 147.02004, 156.62996]
yu = [76.44825, 71.36185, 76.45268, 75.58916, 79.57455, 97.79102, 82.8957, 77.53, 81.35374, 97.26675, 83.51248, 88.67449, 99.54885, 91.89046, 96.03319, 104.05137]
yw = [75.52525, 70.6481, 77.01144, 73.38042, 78.61585, 97.05947, 76.4505, 73.08, 78.09713, 93.38723, 82.09608, 86.97564, 99.11121, 89.46669, 95.66114, 102.16923]

promedios = {
  "promR": 2226.050714285714,
  "promS": 770.6460571428572,
  "promT": 182.0456,
  "promU": 85.7329,
  "promV": 115.67061428571431,
  "promW": 80.13580857142857
}

glucoseR = round(calc_glucosa_canal(x,yr,round(promedios["promR"], 2))["valorGlucosa"],2)
glucoseS = round(calc_glucosa_canal(x,ys,round(promedios["promS"], 2))["valorGlucosa"],2)
glucoseT = round(calc_glucosa_canal(x,yt,round(promedios["promT"], 2))["valorGlucosa"],2)
glucoseU = round(calc_glucosa_canal(x,yu,round(promedios["promU"], 2))["valorGlucosa"],2)
glucoseV = round(calc_glucosa_canal(x,yv,round(promedios["promV"], 2))["valorGlucosa"],2)
glucoseW = round(calc_glucosa_canal(x,yw,round(promedios["promW"], 2))["valorGlucosa"],2)

print("Glucosa canal R", glucoseR)
print("Glucosa canal S", glucoseS)
print("Glucosa canal T", glucoseT)
print("Glucosa canal U", glucoseU)
print("Glucosa canal V", glucoseV)
print("Glucosa canal W", glucoseW)

glucosetotal = (glucoseR + glucoseS + glucoseT + glucoseU + glucoseV + glucoseW) / 6
print("Glucosa total", round(glucosetotal,2))

coefR = calc_glucosa_canal(x,yr,round(promedios["promR"], 2))["R"] 
coefS = calc_glucosa_canal(x,ys,round(promedios["promS"], 2))["R"] 
coefT = calc_glucosa_canal(x,yt,round(promedios["promT"], 2))["R"] 
coefU = calc_glucosa_canal(x,yu,round(promedios["promU"], 2))["R"] 
coefV = calc_glucosa_canal(x,yv,round(promedios["promV"], 2))["R"] 
coefW = calc_glucosa_canal(x,yw,round(promedios["promW"], 2))["R"] 

PromedioPond = (glucoseR * coefR + glucoseS * coefS + glucoseT * coefT + glucoseU * coefU + glucoseV * coefV + glucoseW * coefW) / (coefR + coefS + coefT +coefU + coefV + coefW)

print("Promedio ponderado: ", PromedioPond)

print(calc_glucosa_canal(x,yr,round(promedios["promR"], 2)))
print(calc_glucosa_canal(x,ys,round(promedios["promS"], 2)))
print(calc_glucosa_canal(x,yt,round(promedios["promT"], 2)))
print(calc_glucosa_canal(x,yu,round(promedios["promU"], 2)))
print(calc_glucosa_canal(x,yv,round(promedios["promV"], 2)))
print(calc_glucosa_canal(x,yw,round(promedios["promW"], 2)))


