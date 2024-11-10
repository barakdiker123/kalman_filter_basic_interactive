import numpy as np
from kalman_lib import *


def main_run(time_dur=400, time_jumps=3, Q_0_0=0.05, Q_1_1=0.05):
    rng = np.random.default_rng(12345)
    rfloat = rng.random()

    # fig1, ax = plt.subplots(1,1,figsize=(5, 2.7), layout='constrained')
    # fig2, ax_standard = plt.subplots(4, 1, figsize=(13, 40))

    # plt.close()
    P_0 = np.array([[100, 0, 0, 0], [0, 100, 0, 0],
                   [0, 0, 100, 0], [0, 0, 0, 10]])

    z = np.array([0, 1]).reshape(2, 1)
    R = np.array([[4, 0], [0, 4]])

    pos = np.array([0, -10]).reshape(2, 1)
    v = np.array([5, 5]).reshape(2, 1)
    x_0 = np.concatenate((pos, v), axis=0)

    Q = np.zeros((4, 4))
    Q[0, 0] = Q_0_0  # 0.05  # q_k^y
    Q[1, 1] = Q_1_1  # 0.05  # q_k^x
    Q[2, 2] = 0.0  # q_k^x
    Q[3, 3] = 0.0  # q_k^y
    Q

    H_CV = np.concatenate((np.eye(2), np.zeros((2, 2))), axis=1)
    H_CV

    delta_t = time_jumps  # 3
    phi_cv = generate_phi(delta_t)
    # upper = np.concatenate((np.eye(2),delta_t*np.eye(2)),axis=1)
    # lower = np.concatenate((np.zeros((2,2)),np.eye(2)),axis=1)
    # phi_cv = np.concatenate((upper,lower))

    Q_k = generate_Q_k(delta_t, Q)

    x_n_minus_one = x_0
    P_n_minus_one = P_0
    location_arr = []
    location_uncertainty = []
    # time_dur = 400
    time_jumps = delta_t

    location_x = []
    location_x_uncertainty = []
    location_y = []
    location_y_uncertainty = []
    velocity_x = []
    velocity_x_uncertainty = []
    velocity_y = []
    velocity_y_uncertainty = []
    sample_size = np.arange(0, time_dur, time_jumps).shape[0] * 2
    for t in np.arange(0, time_dur, time_jumps):
        # +np.array([20*(rng.random()-0.5),10*(rng.random()-0.5)]).reshape(2,1)
        z = v * t + x_0[:2] + 4 * np.random.randn(2, 1)
        x_n, P_n = kalman_filter(
            x_n_minus_one, P_n_minus_one, phi_cv, Q_k, H_CV, R, z)
        # x_n,P_n = x_n_minus_one,P_n_minus_one
        x_n_minus_one, P_n_minus_one = x_n, P_n
        location_arr.append(x_n_minus_one[:2])
        location_arr.append(x_n_minus_one[:2])
        eigen_value, eigen_vector = np.linalg.eig(P_n_minus_one[:2, :2])
        location_uncertainty.append(eigen_vector[:, 0] * eigen_value[0])
        location_uncertainty.append(eigen_vector[:, 1] * eigen_value[1])
        location_x.append(x_n_minus_one[0])  # x location !
        location_x_uncertainty.append(P_n_minus_one[0, 0])  # x uncertainty !
        location_y.append(x_n_minus_one[1])  # y location !
        location_y_uncertainty.append(P_n_minus_one[1, 1])  # x uncertainty !
        velocity_x.append(x_n_minus_one[2])  # y location !
        velocity_x_uncertainty.append(P_n_minus_one[2, 2])  # x uncertainty !
        velocity_y.append(x_n_minus_one[3])  # y location !
        velocity_y_uncertainty.append(P_n_minus_one[3, 3])  # x uncertainty !

    GT_x = [v * t + x_0[:2] for t in np.arange(0, time_dur, time_jumps)]
    time = [t for t in np.arange(0, time_dur, time_jumps)]
    error_x = np.array(location_x) - np.array(GT_x)[:, 0]
    data_pos_x = error_x[
        (error_x.ravel() < np.array(location_x_uncertainty))
        & (error_x.ravel() > -np.array(location_x_uncertainty))
    ]
    leng_pos_x_in = str(len(data_pos_x))
    leng_pos_x_total = str(len(error_x))
    # ax_standard[0].plot(time, error_x, "+", label="estimated x position")
    # ax_standard[0].plot(
    #    time, np.array(location_x_uncertainty), label="estimated error x position-"
    # )
    # ax_standard[0].plot(
    #    time, -np.array(location_x_uncertainty), label="estimated error x position+"
    # )
    # ax_standard[0].set_title(
    #    "X positioning" + " " + leng_pos_x_in + "/" + leng_pos_x_total
    # )
    # ax_standard[0].set_xlabel("Time[s]")
    # ax_standard[0].set_ylabel("Error x[m]")

    GT_y = [v * t + x_0[:2] for t in np.arange(0, time_dur, time_jumps)]
    time = [t for t in np.arange(0, time_dur, time_jumps)]
    error_y = np.array(location_y) - np.array(GT_y)[:, 1]
    data_pos_y = error_y[
        (error_y.ravel() < np.array(location_y_uncertainty))
        & (error_y.ravel() > -np.array(location_y_uncertainty))
    ]
    leng_pos_y_in = str(len(data_pos_y))
    leng_pos_y_total = str(len(error_y))
    # ax_standard[1].plot(time, error_y, "+", label="estimated y position")
    # ax_standard[1].plot(
    #    time, np.array(location_y_uncertainty), label="estimated error y position-"
    # )
    # ax_standard[1].plot(
    #    time, -np.array(location_y_uncertainty), label="estimated error y position+"
    # )
    # ax_standard[1].set_title(
    #    "Y positioning" + " " + leng_pos_y_in + "/" + leng_pos_y_total
    # )
    # ax_standard[1].set_xlabel("Time[s]")
    # ax_standard[1].set_ylabel("Error y[m]")

    GT_velo_x = [v[0] for t in np.arange(0, time_dur, time_jumps)]
    time = [t for t in np.arange(0, time_dur, time_jumps)]
    error_velo_x = np.array(velocity_x) - np.array(GT_velo_x)
    # ax_standard[2].plot(time, error_velo_x, "+", label="estimated x velocity")
    # ax_standard[2].plot(
    #    time, np.array(velocity_x_uncertainty), label="estimated error x velocity-"
    # )
    # ax_standard[2].plot(
    #    time, -np.array(velocity_x_uncertainty), label="estimated error x velocity+"
    # )
    # ax_standard[2].set_title("X Velocity")
    # ax_standard[2].set_xlabel("Time[s]")
    # ax_standard[2].set_ylabel("Error x[m/s]")

    GT_velo_y = [v[1] for t in np.arange(0, time_dur, time_jumps)]
    time = [t for t in np.arange(0, time_dur, time_jumps)]
    error_velo_y = np.array(velocity_y) - np.array(GT_velo_y)
    # ax_standard[3].plot(time, error_velo_y, "+", label="estimated y position")
    # ax_standard[3].plot(
    #    time, np.array(velocity_y_uncertainty), label="estimated error y velocity-"
    # )
    # ax_standard[3].plot(
    #    time, -np.array(velocity_y_uncertainty), label="estimated error y velocity+"
    # )
    # ax_standard[3].set_title("Y Velocity")
    # ax_standard[3].set_xlabel("Time[s]")
    # ax_standard[3].set_ylabel("Error y[m/s]")

    return (
        time,
        error_x,
        np.array(location_x_uncertainty),
        error_y,
        np.array(location_y_uncertainty),
        leng_pos_x_in,
        leng_pos_x_total,
        leng_pos_y_in,
        leng_pos_y_total,
    )
