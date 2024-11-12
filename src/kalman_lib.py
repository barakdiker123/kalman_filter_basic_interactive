#!/usr/bin/env python3

import numpy as np
import pandas as pd
import sympy as sp


def kalman_filter(x, P, phi, Q, H, R, z):  # R is the measurement noise covariance
    x_minus = phi @ x  # Estimate position
    P_minus = phi @ P @ phi.T + Q  # estimate covariance matrix
    K_k = P_minus @ H.T @ np.linalg.inv(H @ P_minus @ H.T + R)  # Kalman Gain
    innovation = z - H @ x_minus
    return x_minus + K_k @ innovation, P_minus - K_k @ H @ P_minus


def generate_phi(delta_t):
    upper = np.concatenate((np.eye(2), delta_t * np.eye(2)), axis=1)
    lower = np.concatenate((np.zeros((2, 2)), np.eye(2)), axis=1)
    phi_cv = np.concatenate((upper, lower))
    return phi_cv


def generate_Q_k(delta_t, Q):  # delta is integer for the integral !!!
    """Integrate from 0 to delta_t"""
    # np.trapz(generate_phi(delta_t) @ Q @ generate_phi(delta_t).T, axis=0)
    data = np.array(
        [
            generate_phi(delta_t) @ Q @ generate_phi(delta_t).T
            for delta_t in np.linspace(0, delta_t, 10)
        ]
    )
    integrate_data = np.trapz(data, axis=0)
    return integrate_data  # Q_k note zarchan page 135 !!!


def generate_Q_k_sym(delta_t, Q):
    t = sp.Symbol("t")
    upper = sp.Matrix([[sp.eye(2), t * sp.eye(2)]])
    lower = sp.Matrix([[sp.zeros(2), sp.eye(2)]])
    phi_cv = sp.Matrix([upper, lower])  # Constant velocity in 2d
    Q_k = phi_cv * sp.Matrix(Q) * phi_cv.T
    int_Q_k = Q_k.integrate(t).subs(t, delta_t)
    return np.array(int_Q_k, dtype=float)
