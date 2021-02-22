import osp.wrappers.simcmclkinetics.io_transf_util as ioutil

def getGPFFiltrationEff(P_IN, P_OUT):
    """Calculates GPF filtration efficiency in terms of particle mass or number.

    Arguments:
        P_IN    -- either inlet particle mass stream in kg/s or total particle number
                    on the filter at the beginning in # (float vector)
        P_OUT   -- either outlet particle mass stream in kg/s or total particle number
                    on the filter at the end in # (float vector)

    Returns:
        f_eff_value   -- particle mass or number filtration efficiency
        f_eff_unit    -- particle mass or number filtration efficiency unit
    """

    # set default initial values
    f_eff_value = 0.0
    f_eff_unit = '-'
    # arguments are given as vectors, always take the last values
    if P_IN[-1] > 0:
        f_eff_value = (P_IN[-1]-P_OUT[-1])/P_IN[-1]
    return f_eff_value, f_eff_unit

def getTWCCaptureEff(S_OUT, S_IN):
    """Calculates TWC capture efficiency.

    Arguments:
        S_OUT  -- outlet species concentration in mole fractions (float vector)
        S_IN   -- inlet species concentration in mole fractions (string value)

    Returns:
        f_eff_value   -- species capture efficiency
        f_eff_unit    -- species capture efficiency unit
    """

    # set default initial values
    f_eff_value = 0.0
    f_eff_unit = '-'

    S_IN = float(S_IN)
    if S_IN > 0:
        f_eff_value = (S_IN-S_OUT[-1])/S_IN
    return f_eff_value, f_eff_unit

def getPSD(dNdlogD, D, T, P):
    """Converts provided dNdlogD vs D into a vector of specific particle number densities (#/kg) that
       the GPF engine understands. The translation is case specific, e.g. it requires fixed nr of sections
       of 20, fixed O2/N2 composition and is only applicable to soot model.

    Arguments:
        dNdlogD  -- particle number densities scaled by the log of particle size in #/m^3 (string value)
        D        -- particle size in nm (string value)
        T        -- gas-phase temperature in K (string value)
        P        -- gas-phase pressure in Pa (string value)

    Returns:
        PSD_value  -- Converted particle size distribution over sections in #/kg_gas (string)
        PSD_unit   -- Converted particle size distribution unit
    """

    # string to float conversions
    dNdlogD = dNdlogD.split(',')
    dNdlogD = [float(p) for p in dNdlogD]
    D = D.split(',')
    D = [float(p) for p in D]
    T = float(T)
    P = float(P)

    # setting fixed air composition
    R_gas  = 8.31446261815324
    O2_mole_frac = 0.0077
    N2_mole_frac = 0.97665
    M_O2 = 0.015999  # [kg/mol]
    M_N2 = 0.0140067  # [kg/mol]
    Mav = M_O2 * O2_mole_frac + M_N2 * N2_mole_frac  #[kg/mol]
    rho_g = P * Mav / R_gas / T  #[kg/m3]

    # calculating sectional model parameters (20 sections)
    n_sect = 20
    d_max = D[-1]*1e-9*1.5  # [m]
    rho_s = 1800.0              # [kg/m^3]
    m_min = 6.37646944e-25      # [kg/#], depends on the precursor choice
    d_sect= []

    # transforming PSD
    SecA = ioutil.transformPSD(n_sect,d_max,rho_s,m_min,D,dNdlogD,d_sect)

    # writing the final values as strings
    PSD_unit = '#/kg'
    PSD_value = str(SecA.Sections[0].Np_log / rho_g)
    for sj in SecA.Sections[1:]:
        PSD_value = PSD_value + ' \n ' + str(sj.Np_log / rho_g)

    return PSD_value, PSD_unit