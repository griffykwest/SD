
import numpy as np
import pandas as pd

#############Reading the input file#######################
ip = pd.read_csv(r"/home/griffin-west/SD/TH/SCAinputmp.csv")  ### This changes per computer

row = ip.iloc[0]

# parameters for this run
L = row["L"]
L_e = row["L_e"]
D = row["D"]
Pitch = row["Pitch"]
T_in = row["T_in"]
mdot = row["mdot"]
P_nominal = row["P_nominal"]
qpmax = row["qpmax"]
D_ci = row["D_ci"]
D_fo = row["D_fo"]
reactor = row["reactor"]
SCB = row["SCB"]
if SCB=='on':
    SCBon=True
else:
    SCBon=False

################Setting the cell size, cel vector, and z of each iteration#############
n=400 # number of sections, could add this to inputs
dz=L/n  #size of each cell
cell=np.arange(1,n+1,1)  ## makes the Cell vector
z = np.linspace(-L/2+dz , L/2, n) #makes the z vector
###########Function That takes an input and runs it into the q equation######
def qp(z): 
    return qpmax*np.cos(np.pi*z/L_e)

#####Property table and lookup function##############
# load prop table to data fram

df = pd.read_csv(r"/home/griffin-west/SD/TH/Project_Prop.csv") ### This changes per computer
headers = df.columns.tolist()
##^^ makes a header list

data = df.to_numpy() # puts df into numpy for easier use

# create a lookup for column header
col_idx = {name: i for i, name in enumerate(headers)}

def pl(inputvar, inputvalue, outputvar):  ## Property lookup function

    # gets the column positions
    l = col_idx[inputvar]
    c = col_idx[outputvar]


    x = data[:, l]
    y = data[:, c]

    # check that inputvalue is within bounds of the entire sheet
    if inputvalue < x[0] or inputvalue > x[-1]:
        raise ValueError(f"{inputvar}={inputvalue} is out of range [{x[0]}, {x[-1]}]")
    i_high = np.searchsorted(x, inputvalue) ## position above
    i_low = i_high - 1  ## position below

    # exact match
    if x[i_high] == inputvalue:
        return y[i_high]
    
    ## for interpolation
    x1, x2 = x[i_low], x[i_high]
    y1, y2 = y[i_low], y[i_high]

    # interpolation formula
    propvalue = y1 + (y2 - y1) * (inputvalue - x1) / (x2 - x1)
    return propvalue
##^^ this function reads the csv table, the first variable string is the string in

## gets the saturation constants
h_fsat=pl('P_sat',P_nominal,'h_f')
h_gsat=pl('P_sat',P_nominal,'h_g')
T_sat=pl('P_sat',P_nominal,'T')
h_in=pl('T',T_in,'h_f') 


## making a function for CHF
def Bowring(D,G,P,x,T_m):
    p_r=0.145*P*10**(-6)
    h_fg=pl('T',T_m,'h_g')-pl('T',T_m,'h_f')
    if p_r > 1:
        F_1=p_r**(-0.368)*np.exp(0.648*(1-p_r))
        F_2=F_1*(p_r**(-0.448)*np.exp(0.245*(1-p_r)))**(-1)
        F_3=p_r**(0.219)
        F_4=F_3*p_r**1.649
    elif p_r<1:
        F_1=(1/1.917)*(p_r**18.942*np.exp(20.89*(1-p_r))+0.917)
        F_2=1.309*F_1*(p_r**(1.316)*np.exp(2.444*(1-p_r))+0.309)**(-1)
        F_3=(1/1.667)*(p_r**17.023*np.exp(16.658*(1-p_r))+0.667)
        F_4=F_3*p_r**1.649
    else:
        F_1=1
        F_2=1
        F_3=1
        F_4=1

    n=2-0.5*p_r
    A=(2.317*(h_fg*D*G/4)*F_1)/(1+0.0143*F_2*np.sqrt(D)*G)
    B=G*D/4
    C=(0.077*F_3*D*G)/(1+0.347*F_4*(G/1356)**n)
    qppchf=((A-B*h_fg*x)/C)*psi
    return qppchf

# make all vectors that will be needed and boolian flags for atleast the first half of the code
h=np.zeros(n)
T_m=np.zeros(n)
T_co=np.zeros(n)
x_e=np.zeros(n)
x=np.zeros(n)
scbstart= False
Bstart=False
DP_fric=np.zeros(n)
DP_grav=np.zeros(n) 
DP_accel=np.zeros(n)
DP=np.zeros(n)
vol_f=np.zeros(n)
rho_m=np.zeros(n)
CHFR=np.zeros(n)
CHFoccur=False

## define constants for the flow and boiling side of things
D_e=D*((4/np.pi)*(Pitch/D)**2-1) #equivilant Diameter
A=Pitch**2-np.pi*D**2/4 ## wetted area
G=mdot/(A)  #mass flux
D_h=(4*A)/(np.pi*D) #hydraulic diameter
psi=((1.826*Pitch/D)-1.0430) #weismann
z_D= None   # making a value that will be filled later for onset on SCB
Chengtedfac=0.1339+0.09059*((Pitch/D)-1)-0.09926*((Pitch/D)-1)**2 ## the long part of cheng and todreas
C=G**2*dz/(2*D_e)
cnt=0## debugging counter
g=9.81 #m/s^2


## start of the main code getting the T_m T_co, x, x_e, DP, and CHFR

for i in range(n):
    if i == 0:  ### for the first cell there is no h[i-1] so it must be treated seperatly
        h[i]=h_in+(qp(-L/2+dz/2)*dz)/(mdot)
        T_m[i]=pl('h_f',h[i],'T')
    else:  ## this branch does liquid only no scb
        qp_mid = qp(z[i] - dz/2)
        h[i] = h[i-1] + qp_mid * dz / mdot
        if h[i] > h_fsat: ## for boiling
            Bstart=True
            T_m[i]=T_sat
        else:
            T_m[i]=pl('h_f',h[i],'T') ## does temp lookup

    ## values based on T_m that are needed for T_co and other things 
    h_f=pl('T',T_m[i],'h_f') # Sub cooled 
    h_g=pl('T',T_m[i],'h_g')
    mu_f=pl('T',T_m[i],'mu_f')
    mu_g=pl('T',T_m[i],'mu_g')
    Pr=pl('T',T_m[i],'Pr_f')
    k=pl('T',T_m[i],'k_f')
    vol_f[i]=pl('T',T_m[i],'vol_f')
    vol_g=pl('T',T_m[i],'vol_g')
    Re=G*D_e/mu_f ## reynolds liquid 
    nu=(0.023*Re**0.8)*(Pr**0.333)
    htclo=(k/D_h)*nu*psi
    if Bstart==True: ## for Boiling ## something is wrong and as z grows so does the error
        x_e[i]=(h[i]-h_fsat)/(h_gsat-h_fsat) ## finds x_e for this point
        qm=qp(z[i]) ## gets q here
        if SCBon==False:  ## sets x=x_e if boiling with no subcooled boiling history
            x[i]=x_e[i]
        else:
            x[i]=x_e[i]-x_eZD*np.exp(x_e[i]/x_eZD-1)
        c1=((1-x[i])/(x[i]))**0.9 ## breaking up Xtt
        c2=(vol_f[i]/vol_g)**0.5
        c3=(mu_f/mu_g)**0.1
        Xtt= c1 * c2 * c3  ###props found at T_m 
        htc2phi=htclo*(7400*(qm/(np.pi*D)/(G*(h_g-h_f)))+1.11*Xtt**(-0.66))
        T_co[i]=T_m[i]+qm/(np.pi*D*htc2phi) 
        ##HEM pressure loss
        rho_m[i]=1/(x[i]*vol_g+(1-x[i])*vol_f[i])
        f=(Re**(-0.18))*Chengtedfac
        DP_fric[i]=f*C/rho_m[i]
        DP_grav[i]=g*dz*rho_m[i]
        DP_accel[i]=G**2*(vol_g-vol_f[i])*(x[i]-x[i-1]) 
        #CHFR
        qppchf=Bowring(D_e,G,P_nominal,x[i],T_m[i])## call CHF function
        qpchf=qppchf * np.pi * D ## put chfr into linear heat flux
        CHFR[i]=qpchf/(qm)## need to add the warning flag
        if CHFR[i]<1.3 and reactor=='PWR' and CHFoccur==False: ## Prints if CHFR has dropped below the reactor limit
            print('ALERT!!!!!! CHFR has dropped below 1.3 ')
            CHFoccur=True
        elif CHFR[i]<1.9 and reactor=='BWR' and CHFoccur== False:
            print(f'ALERT!!!!!! CHFR has dropped below 1.9 to a value of{CHFR[i]}')
            CHFoccur=True
    else: ## for not boiling 
        nu=(0.023*Re**0.8)*(Pr**0.333)
        htc=(k/D_e)*nu*psi

        qm=qp(z[i])
        T_co[i]=T_m[i]+qm/(np.pi*D*htc)
        cnt=cnt+1
        ##put single phase dp/dz, fric only
        f=(Re**(-0.18))*Chengtedfac
        DP_fric[i]=f*C*vol_f[i]
        DP_grav[i]=g*dz/vol_f[i]

        ## overwrites the non boiling if scb is happeing, many things similar to boiling
    if  scbstart==False and Bstart==False and T_m[i]<T_sat and T_co[i]>T_sat and SCBon==True: ## to start scb
        scbstart=True ## to turn of scb make this False
        z_D=z[i] # sets the right hight,
        #print(z_D)
        x_eZD=(h[i]-h_fsat)/(h_gsat-h_fsat)
    elif scbstart==True and T_m[i]<T_sat and z[i]>z_D: ## for sub cooled boiling
        ## this section is very similar to regular boiling
        qm=qp(z[i])
        x_e[i]=(h[i]-h_fsat)/(h_gsat-h_fsat)
        x[i]=x_e[i]-x_eZD*np.exp(x_e[i]/x_eZD-1)
        c1=((1-x[i])/(x[i]))**0.9
        c2=(vol_f[i]/vol_g)**0.5
        c3=(mu_f/mu_g)**0.1
        Xtt= c1 * c2 * c3  ###props found at T_m 
        htc2phi=htclo*(7400*(qm/(np.pi*D)/(G*(h_g-h_f)))+1.11*Xtt**(-0.66))
        T_co[i]=T_m[i]+qm/(np.pi*D*htc2phi)
        rho_m[i]=1/(x[i]*vol_g+(1-x[i])*vol_f[i])
        f=(Re**(-0.18))*Chengtedfac
        DP_fric[i]=f*C/rho_m[i]
        DP_grav[i]=g*dz*rho_m[i]
        DP_accel[i]=G**2*(vol_g-vol_f[i])*(x[i]-x[i-1])
        dhsub=h[i]-h_fsat
        qppchf=Bowring(D_e,G,P_nominal,x[i],T_m[i])
        qpchf=qppchf * np.pi * D
        CHFR[i]=qpchf/(qm)
        if CHFR[i]<1.3 and reactor=='PWR' and CHFoccur==False:
            print('ALERT!!!!!! CHFR has dropped below 1.3 ')
            CHFoccur=True
        elif CHFR[i]<1.9 and reactor=='BWR' and CHFoccur== False:
            print(f'ALERT!!!!!! CHFR has dropped below 1.9 to a value of{CHFR[i]}')
            CHFoccur=True


# totaling all types of pressure loss adding vectors
DP=DP_fric+DP_grav+DP_accel

    
## once inside of the fuel rod the outside phase does not matter only the temp so it can all be treated the same.

k_c=15
T_ci=np.zeros(n)
T_fo=np.zeros(n)
T_max=np.zeros(n)
D_g=(D_fo+D_ci)/2
deff=(D_ci-D_fo)/2
sbc=5.67e-8

#looping over and calculating all T_ci T_fo and T_max
for i in range(n):
    qm=qp(z[i])
    T_ci[i]=T_co[i]+(qm/(2*np.pi*k_c))*np.log((D/2)/(D_ci/2)) 
    abserr=1
    htc_g=5000
    counter=0
    T_foold= T_ci[i]+qm/(np.pi*D_g*htc_g)  ## iteration for T_co
    # finding T_fo iterative solving
    while abserr>0.001:
        k_gas=15.8*10**(-4)*((T_foold+T_ci[i])/2+273.15)**0.79
        htc_g=k_gas/deff+sbc*((T_foold+273.15)**4-(T_ci[i]+273.15)**4)/((T_foold+273.15)-(T_ci[i]+273.15))
        T_fonew=T_ci[i]+qm/(np.pi*D_g*htc_g)
        abserr=abs(T_fonew-T_foold)
        T_foold=T_fonew
        counter=counter+1
    T_fo[i]=T_foold ## files the value after convergence
    ## runs 4-7 times before converging



    ## now initializing guesses for T_max and over writing previous values
    k_guess=3 #w/mK
    ## making some constants for the integral equation for t_max
    c4=6.1256E-11
    c5=3824
    c6=402.4
    qmax=qp(z[i])
    ## get a first guess using T_guess
    T_maxnew=T_fo[i]+qmax/(4*np.pi*k_guess)
    diff=1
    cntr=0
    ##T_max iteration loop
    while diff>0.0001:
        kdT_max=c5*np.log(c6+T_fo[i])+c4/4*(T_fo[i]+273)**4+qmax/(4*np.pi)
        kdT_check=c5*np.log(c6+T_maxnew)+c4/4*(T_maxnew+273)**4
        T_maxold=T_maxnew
        T_maxnew=T_maxold+(kdT_max-kdT_check)/100
        diff=abs(kdT_max-kdT_check)
        cntr=cntr+1
    T_max[i]=T_maxnew 
    #print(cntr)
    ## runs 200-500 times before converging
    # rounding all numbers to the same length as correct values
    T_m[i]   = round(T_m[i], 5)
    T_co[i]  = round(T_co[i], 5)
    T_ci[i]  = round(T_ci[i], 5)
    T_fo[i]  = round(T_fo[i], 5)
    T_max[i] = round(T_max[i], 5)
    DP[i]    = round(DP[i],5)
    x[i]     = round(x[i],10)
    x_e[i]   = round(x_e[i],10)
    CHFR[i]  = round(CHFR[i],7)
    z[i]     = round(z[i],6)



## this makes a dataframe that can be uploaded to excel
dframe= pd.DataFrame({
    'Cell': cell,
    'z': z,
    'T_m': T_m,
    'T_co': T_co,
    'T_ci': T_ci,
    'T_fo': T_fo,
    'T_max':T_max,
    'x': x,
    'x_e': x_e,
    'CHFR':CHFR,
    'DP (this cell)':DP})
#filename based off input reactor type and scb
filename = f"{reactor}{'SCB' if SCBon else 'NSCB'}test.xlsx"
print(qpmax)
## saving output to excel
path = fr"/home/griffin-west/SD/TH/{filename}"
dframe.to_csv(path, index=False) ## user computer  specific
if Bstart==True:
    print('boiling occured')

maxtemp=max(T_max)
print(f"The max fuel temperature reached was {maxtemp:.2f} C")
# overall prints if CHFR limit is hit, if boiling occured, and what the max fuel temp was
