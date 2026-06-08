"""
Hodgkin-Huxley neuron model.

Implements the 1952 HH conductance-based neural model. 
Voltage and time are in mV and ms respectively. Current density
in uA/cm2 and conductance density in mS/cm2.

Reference: Hodgkin & Huxley (1952) J. Physiol. 117, 500-544.
"""

import numpy as np
from scipy.integrate import solve_ivp

# ---------------------------------------------------------------------------
# Default biophysical parameters
# ---------------------------------------------------------------------------

DEFAULT_PARAMS = {
    "C_m":  1.0,       # membrane capacitance  (uF/cm2)
    "g_Na": 120.0,     # max Na conductance   (mS/cm2)
    "g_K":  36.0,      # max K conductance    (mS/cm2)
    "g_L":  0.3,       # leak conductance      (mS/cm2)
    "E_Na":  50.0,     # Na reversal          (mV)
    "E_K":  -77.0,     # K reversal           (mV)
    "E_L":  -54.387,   # leak reversal         (mV)
}

DEFAULT_V_REST = -65.0   # resting potential used for initial conditions (mV)
DEFAULT_I_APP  = 10.0    # applied current density for regular spiking   (µA/cm²)

# ---------------------------------------------------------------------------
# Voltage-dependent rate functions (α / β)
# ---------------------------------------------------------------------------

def alpha_m(V):
    """Opening rate for Na activation gate m (1/ms)."""
    dv = V + 40.0
    # L'Hôpital limit at V = -40 mV avoids 0/0
    return np.where(np.abs(dv) < 1e-7,
                    1.0,
                    0.1 * dv / (1.0 - np.exp(-dv / 10.0)))


def beta_m(V):
    """Closing rate for Na activation gate m (1/ms)."""
    return 4.0 * np.exp(-(V + 65.0) / 18.0)


def alpha_h(V):
    """Opening rate for Na inactivation gate h (1/ms)."""
    return 0.07 * np.exp(-(V + 65.0) / 20.0)


def beta_h(V):
    """Closing rate for Na inactivation gate h (1/ms)."""
    return 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))


def alpha_n(V):
    """Opening rate for K activation gate n (ms⁻¹)."""
    dv = V + 55.0
    # L'Hôpital limit at V = -55 mV
    return np.where(np.abs(dv) < 1e-7,
                    0.1,
                    0.01 * dv / (1.0 - np.exp(-dv / 10.0)))


def beta_n(V):
    """Closing rate for K activation gate n (1/ms)."""
    return 0.125 * np.exp(-(V + 65.0) / 80.0)

# ---------------------------------------------------------------------------
# Steady-state gating variables
# ---------------------------------------------------------------------------

def steady_state_gates(V):
    """Return (minf, hinf, ninf) at voltage V (mV)."""
    am, bm = alpha_m(V), beta_m(V)
    ah, bh = alpha_h(V), beta_h(V)
    an, bn = alpha_n(V), beta_n(V)
    return am / (am + bm), ah / (ah + bh), an / (an + bn)


def gate_time_constants(V):
    """Return (tau_m, tau_h, tau_n) in ms at voltage V."""
    tau_m = 1.0 / (alpha_m(V) + beta_m(V))
    tau_h = 1.0 / (alpha_h(V) + beta_h(V))
    tau_n = 1.0 / (alpha_n(V) + beta_n(V))
    return tau_m, tau_h, tau_n

# ---------------------------------------------------------------------------
# Ionic currents
# ---------------------------------------------------------------------------

def ionic_currents(V, m, h, n, params):
    """Return (I_Na, I_K, I_L) in uA/cm2."""
    I_Na = params["g_Na"] * m**3 * h * (V - params["E_Na"])
    I_K  = params["g_K"]  * n**4     * (V - params["E_K"])
    I_L  = params["g_L"]             * (V - params["E_L"])
    return I_Na, I_K, I_L

# ---------------------------------------------------------------------------
# ODE right-hand side
# ---------------------------------------------------------------------------

def hh_rhs(t, y, params, I_app):
    """Right-hand side of the Hodgkin-Huxley ODE system.

    State vector: y = [V (mV), m, h, n]

    Parameters
    ----------
    t      : float  - current time (ms)
    y      : array  - state [V, m, h, n]
    params : dict   - biophysical parameters (see DEFAULT_PARAMS)
    I_app  : float  - applied current density (uA/cm2)
    """
    V, m, h, n = y

    I_Na, I_K, I_L = ionic_currents(V, m, h, n, params)

    dV = (I_app - I_Na - I_K - I_L) / params["C_m"]
    dm = alpha_m(V) * (1.0 - m) - beta_m(V) * m
    dh = alpha_h(V) * (1.0 - h) - beta_h(V) * h
    dn = alpha_n(V) * (1.0 - n) - beta_n(V) * n

    return [dV, dm, dh, dn]

# ---------------------------------------------------------------------------
# Simulation entry point
# ---------------------------------------------------------------------------

def simulate(t_span=(0.0, 100.0), I_app=DEFAULT_I_APP,
             params=None, V0=DEFAULT_V_REST, dt=0.025):
    """Integrate the HH model and return an OdeSolution object.

    Parameters
    ----------
    t_span : (float, float)  - (t_start, t_end) in ms
    I_app  : float           - applied current density in uA/cm2
    params : dict or None    - model parameters; None uses DEFAULT_PARAMS
    V0     : float           - initial membrane potential in mV
    dt     : float           - output time step in ms (max integration step)

    Returns
    -------
    sol : scipy.integrate.OdeResult
        sol.t  - time array (ms)
        sol.y  - state matrix [V, m, h, n] x time
    """
    if params is None:
        params = DEFAULT_PARAMS.copy()

    m0, h0, n0 = steady_state_gates(V0)
    y0 = [V0, m0, h0, n0]

    t_eval = np.arange(t_span[0], t_span[1] + dt, dt)

    sol = solve_ivp(
        fun=lambda t, y: hh_rhs(t, y, params, I_app),
        t_span=t_span,
        y0=y0,
        method="RK45",
        t_eval=t_eval,
        max_step=dt,
        rtol=1e-6,
        atol=1e-8,
    )

    if not sol.success:
        raise RuntimeError(f"ODE integration failed: {sol.message}")

    return sol


def get_default_params():
    """Return a copy of the default HH parameter dictionary."""
    return DEFAULT_PARAMS.copy()
