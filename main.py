
#This is where wind loading calcs go
import scipy.interpolate

def Wind(importance_level,design_life,region,height_z,Terrain_categories):
    Vr = 37
    Mc = 1
    A0 = {'N':0.9,'NE':0.85,'E':0.85,'SE':0.9,'S':0.9,'SW':0.95,'W':1,'NW':0.95}#Done
    A1 = {'N': 0.9, 'NE': 0.85, 'E': 0.85, 'SE': 0.8, 'S': 0.8, 'SW': 0.95, 'W': 1, 'NW': 0.95}#Done
    A2 = {'N': 0.85, 'NE': 0.75, 'E': 0.85, 'SE': 0.95, 'S': 0.95, 'SW': 0.95, 'W': 1, 'NW': 0.95}#Done
    A3 = {'N': 0.9, 'NE': 0.85, 'E': 0.85, 'SE': 0.9, 'S': 0.9, 'SW': 0.95, 'W': 1, 'NW': 0.95}
    A4 = {'N': 0.9, 'NE': 0.85, 'E': 0.85, 'SE': 0.9, 'S': 0.9, 'SW': 0.95, 'W': 1, 'NW': 0.95}
    A5 = {'N': 0.9, 'NE': 0.85, 'E': 0.85, 'SE': 0.9, 'S': 0.9, 'SW': 0.95, 'W': 1, 'NW': 0.95}
    B1 = {'N': 0.9, 'NE': 0.85, 'E': 0.85, 'SE': 0.9, 'S': 0.9, 'SW': 0.95, 'W': 1, 'NW': 0.95}
    B2 = {'N': 0.9, 'NE': 0.85, 'E': 0.85, 'SE': 0.9, 'S': 0.9, 'SW': 0.95, 'W': 1, 'NW': 0.95}
    T3_2_A = {'A0':A0,'A1':A1,'A2':A2,'A3':A3,'A4':A4,'A5':A5,'B1':B1,'B2':B2,'C':B2,'D':B2}
    Md = T3_2_A[region]
    Mz_cat = select_Mz_cat(height_z,Terrain_categories)
    Ms = 1
    Mt = 1
    Vsit_beta = {}
    p_sls = {}
    p_uls = {}
    for i in Terrain_categories:
        Vsit_beta[i] = Vr*Mc*Md[i]*Mz_cat[i]*Ms*Mt
        p_sls[i] = round(0.6*Vsit_beta[i]**2/1000,2)
        p_uls[i] = round(p_sls[i]*(45/Vr)**2,2)
    print(p_sls,'sls')
    print(p_uls,'uls')
    return p_sls, p_uls, Mz_cat, Md, Vr

importance_level = 2
design_life = 50
region = 'A2'
height_z = 8
#Couldnt put Terrain category 2.5 so went straight to 3, i.e. Terrain cat 3 is now = 4, etc.
Terrain_categories = {'N':3,'NE':3,'E':4,'SE':4,'S':4,'SW':4,'W':4,'NW':2}

#Takes nearest values, Does not interpolate!!!
def select_Mz_cat(z,Terrain_categories):

    Mz_cat = {}

    col_A = [3,5,10,15,20,30,40,50,75,100,150,200]
    col_1 = [0.97,1.01,1.08,1.12,1.14,1.18,1.21,1.23,1.27,1.31,1.36,1.39]
    col_2 = [0.91,0.91,1,1.05,1.08,1.12,1.16,1.18,1.22,1.24,1.27,1.29]
    col_2_5 = [0.87,0.87,0.92,0.97,1.01,1.06,1.1,1.13,1.17,1.2,1.24,1.27]
    col_3 = [0.83,0.83,0.83,0.89,0.94,1,1.04,1.07,1.12,1.16,1.21,1.24]
    col_4 = [0.75,0.75,0.75,0.75,0.75,0.8,0.85,0.9,0.98,1.03,1.11,1.16]
    cols = [col_A,col_1,col_2,col_2_5,col_3,col_4]

    if z <= 3:
        for j in Terrain_categories:
            Mz_cat[j] = cols[Terrain_categories[j]][0]
    else:
        x = min(col_A, key=lambda x: abs(x - z))
        if x > z:
            check = -1
        else:
            check = +1
        count =0
        for j in col_A:
            if x == j:
                break
            count += 1
        for i in Terrain_categories:
            x1 = cols[Terrain_categories[i]][count]
            x2 = cols[Terrain_categories[i]][count + check]
            y1 = col_A[count]
            y2 = col_A[count + check]
            Mz_cat[i] = x2 - (x2-x1)/(y2-y1)*(y2-z)
        #for i in Terrain_categories:
            #Mz_cat[i] = cols[Terrain_categories[i]][count]

    return Mz_cat

x = Wind(importance_level,design_life,region,height_z,Terrain_categories)
with open('Wind pressures.txt','w') as f:
    f.write('p SLS ' + str(x[0]))
    f.write('\n')
    f.write('\n')
    f.write('p SLS max: ' + str(max(x[0].values())) + ' KPa\n\n')
    f.write('p ULS ' + str(x[1]))
    f.write('\n')
    f.write('\n')
    f.write('p ULS max: ' + str(max(x[1].values())) + ' KPa\n\n')
    f.write('Terrain categories are integers only, so category 2.5 = 3, 3 = 4, and 4 = 5\n')
    f.write('Terrain categories ' + str(Terrain_categories))
    f.write('\n')
    f.write('\n')
    f.write('Mz_cat ' + str(x[2]))
    f.write('\n')
    f.write('\n')
    f.write('Md ' + str(x[3]))
    f.write('\n')
    f.write('\n')
    f.write('Vr sls ' + str(x[4]))
    f.write(' m/s\n')
    f.write('\n')
    f.write('Height, z ' + str(height_z))
    f.write(' m\n')
    f.write('\n')
    f.write('Region ' + region)
