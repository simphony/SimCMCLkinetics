import numpy as np

EPS = 1E-12
LogBase = np.e

class Secs:
    #--------------------------------------------------
    #            Container that stores all sections
    #--------------------------------------------------
    def __init__(self,aName="",aNsect=0,aDmin=0.0,aDmax=0.0,aSections=[]):
        self.Name = aName           # Some name
        self.Nsect = aNsect         # Nr of sections
        self.Dmin = aDmin           # Part diameter in the first section [nm]
        self.Dmax = aDmax           # Part diameter in the last section [nm]
        self.Sections = aSections   # Array of sections of type Seci
        self.Npt_lin = 0.0          # Total nr of density of particles (in all sections)
                                    # obtained by integration in dD
        self.Npt_log = 0.0          # Total nr of density particles (in all sections)
                                    # obtained by integration in dlogD
        self.mpt_lin = 0.0          # Total mass density of particles (in all sections)
                                    # obtained by integration in dD
        self.mpt_log = 0.0          # Total mass density of particles (in all sections)
                                    # obtained by integration in dlogD
        self.Vpt_lin = 0.0          # Total volume density of particles (in all sections)
                                    # obtained by integration in dD
        self.Vpt_log = 0.0          # Total volume density of particles (in all sections)
                                    # obtained by integration in dlogD
        self.FDS = -1               # Index of the first section with some
                                    # experimental data in it
        self.LDS = -1               # Index of the last section with some
                                    # experimental data in it
class Seci:
    #--------------------------------------------------
    #   Container that stores data for a single section
    #--------------------------------------------------
    def __init__(self,aName="",aId=0,aD=0.0,
                 aFirst=False,aLast=False, arho_s=1800):
        self.Name = aName              # Some name
        self.Id = aId                  # Section index (0-based, but doesnt really matter)
        self.D = aD                    # Section diameter [nm]
        self.logD = np.log(aD)/np.log(LogBase) # Natural log (default) of Section's diameter (lnD)
        self.LB = 0.0                  # Section lower bound [nm]
        self.UB = 0.0                  # Section upper bound [nm]
        self.logLB = 0.0               # Ln of LB
        self.logUB = 0.0               # Ln of UB
        self.Vp_one = np.pi*(aD*1e-9)**3.0/6.0            # Volume of a single particle of size aD [m^3]
        self.mp_one = np.pi*(aD*1e-9)**3.0/6.0 * arho_s   # Mass of a single particle of size aD [kg]
        self.First = aFirst        # True if the section is the first section (e.g. section 0)
        self.Last = aLast          # True if the section is the last section
        self.ExpIds = []           # Indices of experimental data points that fall into this
        self.DataPointsN = []      # All integrable N points = experimental points + interpolated points
        self.DataPointsD = []      # All integrable D points = experimental points + interpolated points



        self.Np_lin = 0.0          # Total nr density of particles in this section obtained via integration in dD
        self.Np_log = 0.0          # Total nr density of particles in this section obtained via integration in dlogD
        self.mp_lin = 0.0          # Total mass density of particles in this section:   mp_one x Np_lin
        self.mp_log = 0.0          # Total mass density of particles in this section:   mp_one x Np_log
        self.Vp_lin = 0.0          # Total volume density of particles in this section: Vp_one x Np_lin
        self.Vp_log = 0.0          # Total volume density of particles in this section: Vp_one x Np_log

def setSectDiams(n_sect,d_max,rho_s,m_min,d_sect):
    if not d_sect:
        # This calculates sections diameters, creates sections containers Seci,
        # puts them into an array Sec = [ Seci1, Seci2, ..., SeciN]
        # and crates global sections container SecA, that holds Sec array
        # dmax [m]
        # rho_s [kg/m^3]
        # m_min [lg/#]
        d_sect = [0]*n_sect
        m_max = rho_s * np.pi / 6. * d_max**3 #m_max [kg/#]
        FS = (np.log(m_max)/np.log(LogBase)-np.log(m_min)/np.log(LogBase))/(n_sect-1)
        XS = [0]*n_sect
        XS[0] = np.log(m_min)/np.log(LogBase)
        for i in range(1,n_sect):
            XS[i] = XS[i-1] + FS
        # calculate section diameter
        d_sect = [0]*n_sect
        Sec = [0]*n_sect
        for i in range (n_sect):
           d_sect[i]=(np.power(LogBase,XS[i])/rho_s / np.pi * 6.0)**(1.0/3.0)*1e9 # d_sect[i] in [nm]
           Sec[i] = Seci(aName="Section "+str(i),aId=i,aD=d_sect[i],aFirst=(i==0),aLast=(i==n_sect-1),arho_s=rho_s)
    else:
        Sec = [0]*n_sect
        for i in range (n_sect):
           Sec[i] = Seci(aName="Section "+str(i),aId=i,aD=d_sect[i],aFirst=(i==0),aLast=(i==n_sect-1),arho_s=rho_s)
    # output sections
    SecA = Secs(aName='All Sections',aNsect=n_sect,aDmin=d_sect[0],aDmax=d_sect[-1],aSections=Sec)
    return SecA

def setSectBounds(SecA):
    # This sets sections LB/UB - these are set in lin scale
    for n in range(SecA.Nsect):
        sj = SecA.Sections[n]

        # First section
        if n == 0:
            sk = SecA.Sections[n+1]
            # initial LB assigned to be symmetrical with UB,
            # however, LB may later change if there is exp
            # data point that is smaller than the current LB
            sj.LB = sj.D - (sk.D-sj.D)/2.0  # [nm]
            sj.UB = sj.D + (sk.D-sj.D)/2.0  # [nm]
            sj.logLB = np.log(sj.LB) / np.log(LogBase)
            sj.logUB = np.log(sj.UB) / np.log(LogBase)

        # Last section
        elif n == SecA.Nsect-1:
            si = SecA.Sections[n-1]
            # intial UB assigned to be symmetrical with LB,
            # however, UB may later change if there is exp
            # data point that is greater than the current UB
            sj.LB = si.UB  # [nm]
            sj.UB = sj.D + (sj.D-si.D)/2.0  # [nm]
            sj.logLB = np.log(sj.LB) / np.log(LogBase)
            sj.logUB = np.log(sj.UB) / np.log(LogBase)

        # in between sections
        else:
            si = SecA.Sections[n-1]
            sk = SecA.Sections[n+1]

            sj.LB = si.UB  # [nm]
            sj.UB = sj.D + (sk.D-sj.D)/2.0  # [nm]
            sj.logLB = np.log(sj.LB) / np.log(LogBase)
            sj.logUB = np.log(sj.UB) / np.log(LogBase)

    return SecA

def expPointsToSect(SecA,d_exp,y_exp):
    def doInterp(xp,xv,yv):
        yint = np.interp(xp,xv,yv)
        xint = xp
        return xint, yint

    FSD_found = False
    for j in range(SecA.Nsect):
        sj = SecA.Sections[j]

        # first section
        if j == 0:
            exp_ind_list = list(filter(lambda x: d_exp[x] < sj.UB, range(len(d_exp))))
            if exp_ind_list:
                FSD_found = True

                d_exps = [d_exp[i] for i in exp_ind_list]
                y_exps = [y_exp[i] for i in exp_ind_list]

                sj.ExpIds.extend(exp_ind_list)
                sj.DataPointsN.extend(y_exps)
                sj.DataPointsD.extend(d_exps)

                # If it happens that some points are
                # lower than section LB, move LB
                if (d_exps[0] < sj.LB):
                    sj.LB = d_exps[0]
                    sj.logLB = np.log(sj.LB)/np.log(LogBase)

                # add interpolated UB point in case there are exp points after this section
                iL = exp_ind_list[-1]
                if iL < len(d_exp)-1:
                    xend, yend = doInterp(sj.UB,d_exp,y_exp)
                    sj.DataPointsN.append(yend)
                    sj.DataPointsD.append(xend)

        # last section
        elif j == SecA.Nsect-1:
            exp_ind_list = list(filter(lambda x: d_exp[x] >= sj.LB, range(len(d_exp))))
            if exp_ind_list:

                d_exps = [d_exp[i] for i in exp_ind_list]
                y_exps = [y_exp[i] for i in exp_ind_list]

                # add interpolated LB point in case there were exp points before this section
                if FSD_found:
                    xf, yf = doInterp(sj.LB,d_exp,y_exp)
                    sj.DataPointsN.append(yf)
                    sj.DataPointsD.append(xf)

                # If it happens that some points are
                # larger than sections UB, move UB
                if (d_exps[-1] > sj.UB):
                    sj.UB = d_exps[-1]
                    sj.logUB = np.log(sj.UB)/np.log(LogBase)

                sj.ExpIds.extend(exp_ind_list)
                sj.DataPointsN.extend(y_exps)
                sj.DataPointsD.extend(d_exps)
        else:
            # Assign all exp points that
            # are within section's LB - UB
            exp_ind_list = list(filter(lambda x: d_exp[x] >= sj.LB and d_exp[x] < sj.UB, range(len(d_exp))))

            if exp_ind_list:

                d_exps = [d_exp[i] for i in exp_ind_list]
                y_exps = [y_exp[i] for i in exp_ind_list]

                # add interpolated LB point in case there were exp points before this section
                if FSD_found:
                    xf, yf = doInterp(sj.LB,d_exp,y_exp)
                    sj.DataPointsN.append(yf)
                    sj.DataPointsD.append(xf)

                # add sections exp points to the list
                sj.ExpIds.extend(exp_ind_list)
                sj.DataPointsN.extend(y_exps)
                sj.DataPointsD.extend(d_exps)

                # add interpolated UB point in case there are exp points after this section
                iL = exp_ind_list[-1]
                if iL < len(d_exp)-1 and any(d >= sj.UB for d in d_exp):
                    xend, yend = doInterp(sj.UB,d_exp,y_exp)
                    sj.DataPointsN.append(yend)
                    sj.DataPointsD.append(xend)
                FSD_found = True
            else:
                # section with no exp points that is after a section with exp points
                # only consider this section if there were exp points prior to it and
                # if there are exp points after it
                if FSD_found and any(d >= sj.UB for d in d_exp):
                    # add interpolated LB point
                    xf, yf = doInterp(sj.LB,d_exp,y_exp)
                    sj.DataPointsN.append(yf)
                    sj.DataPointsD.append(xf)

                    # add interpolated UB point
                    xend, yend = doInterp(sj.UB,d_exp,y_exp)
                    sj.DataPointsN.append(yend)
                    sj.DataPointsD.append(xend)

    # Once the exp points are assigned,
    # find an index of the first section
    # that has some points
    for j in range(SecA.Nsect):
        if SecA.Sections[j].ExpIds:
            SecA.FDS = j
            break
    # Find an index of the last section
    # that has some points
    for j in range(SecA.Nsect-1,-1,-1):
        if SecA.Sections[j].ExpIds:
            SecA.LDS = j
            break

    # For each section, calculate how many
    # exp points it has
    for j in range(SecA.FDS,SecA.LDS+1):
        SecA.Sections[j].Nexps = len(SecA.Sections[j].ExpIds)
    return SecA


def int_dNdlogD(SecA,d_exp,y_exp):
    # Calculates number of particles in each section
    # via integration in dD and dlogD
    for j in range(SecA.FDS,SecA.LDS+1):
        sj = SecA.Sections[j]
        if j >= SecA.FDS:
            sj = interpOneBit_logd(sj,d_exp,y_exp,j,SecA.FDS,SecA.LDS)
            sj = interpOneBit_d(sj,d_exp,y_exp,j,SecA.FDS,SecA.LDS)

            # Accumulate total densities for number of particles, mass and volume
            # across all sections
            SecA.Npt_lin = SecA.Npt_lin + sj.Np_lin
            SecA.Npt_log = SecA.Npt_log + sj.Np_log
            SecA.mpt_lin = SecA.mpt_lin + sj.mp_lin
            SecA.mpt_log = SecA.mpt_log + sj.mp_log
            SecA.Vpt_lin = SecA.mpt_lin + sj.Vp_lin
            SecA.Vpt_log = SecA.mpt_log + sj.Vp_log
    return SecA

def interpOneBit_logd(sj,d_exp,y_exp,j,FDS,LDS):
    # integrates in dlogD
    logd = [np.log(d)/np.log(LogBase) for d in sj.DataPointsD]
    sj.Np_log = np.trapz(sj.DataPointsN,logd)
    # Calculate mass and volume densities of all particles in this section
    # we assume that particles are of the same size D
    sj.mp_log = sj.mp_one * sj.Np_log
    sj.Vp_log = sj.Vp_one * sj.Np_log
    return sj

def interpOneBit_d(sj,d_exp,y_exp,j,FDS,LDS):
    # integrates in dD

    y_use = [y/x for y, x in zip(sj.DataPointsN, sj.DataPointsD)]

    sj.Np_lin = np.trapz(y_use,sj.DataPointsD)

    # Calculate mass and volume densities of all particles in this section
    # we assume that particles are of the same size D
    sj.mp_lin = sj.mp_one * sj.Np_lin
    sj.Vp_lin = sj.Vp_one * sj.Np_lin
    return sj


def transformPSD(n_sect,d_max,rho_s,m_min,d_exp,y_exp,d_sect):
    SecA = setSectDiams(n_sect,d_max,rho_s,m_min,d_sect)
    SecA = setSectBounds(SecA)
    SecA = expPointsToSect(SecA,d_exp,y_exp)
    SecA = int_dNdlogD(SecA,d_exp,y_exp)
    return SecA