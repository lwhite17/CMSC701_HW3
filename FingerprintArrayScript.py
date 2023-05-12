import BBHash
import Utils
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import FingerprintArray as FA
sns.set_style('darkgrid')
import matplotlib
matplotlib.rcParams.update({'font.size': 16})


def plot(res):
    sizes, times_o0, times_o1, times_o2, times_o5 = res[:5]
    false_pos_o0, false_pos_o1, false_pos_o2, false_pos_o5 = res[5:]

    # Plot size
    Ns = [10000, 30000, 60000]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(Ns, sizes[0, :], label="$b=7$")
    ax.plot(Ns, sizes[1, :], label="$b=8$")
    ax.plot(Ns, sizes[2, :], label="$b=10$")
    ax.set_xlabel("Number of keys")
    ax.set_ylabel("Size of MPH + fingerprint array (bytes)")
    ax.set_title("Size of MPH + fingerprint array vs number of keys")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("FPA_size.png")
    plt.clf()

    # Plot time
    times_o0 *= 1e-6
    times_o1 *= 1e-6
    times_o2 *= 1e-6
    times_o5 *= 1e-6

    fig, ax = plt.subplots(figsize=(10, 6))
    # gamma_strs = ["$\gamma=2^{-7}$", "$\gamma=2^{-8}$", "$\gamma=2^{-10}$"]
    gamma_strs = ["$b=7$", "$b=8$", "$b=10$"]
    overlap_strs = ["overlap 0%", "overlap 10%", "overlap 25%", "overlap 50%"]
    linestyles = ["-", "--", ":", "-."]
    for ind, gamma_str in enumerate(gamma_strs):
        ax.plot(Ns, times_o0[ind, :],
                label=gamma_str + ", " + overlap_strs[0],
                linestyle=linestyles[ind])
        ax.plot(Ns, times_o1[ind, :],
                label=gamma_str + ", " + overlap_strs[1],
                linestyle=linestyles[ind])
        ax.plot(Ns, times_o2[ind, :],
                label=gamma_str + ", " + overlap_strs[2],
                linestyle=linestyles[ind])
        ax.plot(Ns, times_o5[ind, :],
                label=gamma_str + ", " + overlap_strs[3],
                linestyle=linestyles[ind])

    ax.set(xscale='log')
    ax.set_xlabel("Number of keys")
    ax.set_ylabel("Total query time of MPH + fingerprint array (ms)")
    ax.set_title("Total query time vs number of keys")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("FPA_times.png")
    plt.clf()

    avg_times_o0 = times_o0 * 1e6
    avg_times_o1 = times_o1 * 1e6
    avg_times_o2 = times_o2 * 1e6
    avg_times_o5 = times_o5 * 1e6
    for j in range(3):
        avg_times_o0[:, j] /= Ns[j]
        avg_times_o1[:, j] /= Ns[j]
        avg_times_o2[:, j] /= Ns[j]
        avg_times_o5[:, j] /= Ns[j]

    # Plot avg times
    fig, ax = plt.subplots(figsize=(10, 6))
    # gamma_strs = ["$\gamma=2^{-7}$", "$\gamma=2^{-8}$", "$\gamma=2^{-10}$"]
    gamma_strs = ["$b=7$", "$b=8$", "$b=10$"]
    overlap_strs = ["overlap 0%", "overlap 10%", "overlap 25%", "overlap 50%"]
    linestyles = ["-", "--", ":", "-."]
    for ind, gamma_str in enumerate(gamma_strs):
        ax.plot(Ns, avg_times_o0[ind, :],
                label=gamma_str + ", " + overlap_strs[0],
                linestyle=linestyles[ind])
        ax.plot(Ns, avg_times_o1[ind, :],
                label=gamma_str + ", " + overlap_strs[1],
                linestyle=linestyles[ind])
        ax.plot(Ns, avg_times_o2[ind, :],
                label=gamma_str + ", " + overlap_strs[2],
                linestyle=linestyles[ind])
        ax.plot(Ns, avg_times_o5[ind, :],
                label=gamma_str + ", " + overlap_strs[3],
                linestyle=linestyles[ind])

    ax.set(xscale='log')
    ax.set_xlabel("Number of keys")
    ax.set_ylabel("Average query time of MPH + fingerprint array (ns)")
    ax.set_title("Average query time vs number of keys")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("FPA_avgtimes.png")
    plt.clf()

    # Plot false pos
    Ns = [10000, 30000, 60000]

    fig, ax1 = plt.subplots(figsize=(10, 6))
    # gamma_strs = ["$\gamma=2^{-7}$", "$\gamma=2^{-8}$", "$\gamma=2^{-10}$"]
    overlap_strs = ["overlap 0%", "overlap 10%", "overlap 25%", "overlap 50%"]
    linestyles = ["-", "--", ":", "-."]
    for ind, gamma_str in enumerate(gamma_strs):
        ax1.plot(Ns, false_pos_o0[ind, :],
                 label=gamma_str + ", " + overlap_strs[0],
                 linestyle=linestyles[ind])
        ax1.plot(Ns, false_pos_o1[ind, :],
                 label=gamma_str + ", " + overlap_strs[1],
                 linestyle=linestyles[ind])
        ax1.plot(Ns, false_pos_o2[ind, :],
                 label=gamma_str + ", " + overlap_strs[2],
                 linestyle=linestyles[ind])
        ax1.plot(Ns, false_pos_o5[ind, :],
                 label=gamma_str + ", " + overlap_strs[3],
                 linestyle=linestyles[ind])

    ax1.set(xscale='log')
    ax1.set_xlabel("Number of keys")
    ax1.set_ylabel("False positive count of ")
    ax1.set_title("MPH + fingerprint array false positive count vs number of keys")
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("FPA_falsepos_count.png")
    plt.clf()

    for ind, N in enumerate(Ns):
        false_pos_o0[:, ind] /= N
        false_pos_o1[:, ind] /= N
        false_pos_o2[:, ind] /= N
        false_pos_o5[:, ind] /= N
    fig, ax = plt.subplots(figsize=(10, 6))
    for ind, gamma_str in enumerate(gamma_strs):
        ax.plot(Ns, false_pos_o0[ind, :],
                label=gamma_str + ", " + overlap_strs[0],
                linestyle=linestyles[ind])
        ax.plot(Ns, false_pos_o1[ind, :],
                label=gamma_str + ", " + overlap_strs[1],
                linestyle=linestyles[ind])
        ax.plot(Ns, false_pos_o2[ind, :],
                label=gamma_str + ", " + overlap_strs[2],
                linestyle=linestyles[ind])
        ax.plot(Ns, false_pos_o5[ind, :],
                label=gamma_str + ", " + overlap_strs[3],
                linestyle=linestyles[ind])

    ax.set(xscale='log')
    ax.set_xlabel("Number of keys")
    ax.set_ylabel("False positive rate ")
    ax.set_title("MPH + fingerprint array false positive rate vs number of keys")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig("FPA_falsepos_rate.png")
    plt.clf()


def main():
    Ns = [10000, 30000, 60000]

    # Gammas by Ns
    times_o0 = np.zeros((3, 3))
    times_o1 = np.zeros((3, 3))
    times_o2 = np.zeros((3, 3))
    times_o5 = np.zeros((3, 3))

    sizes = np.zeros((3, 3))

    # Gammas by ns
    false_pos_o0 = np.zeros((3, 3))
    false_pos_o1 = np.zeros((3, 3))
    false_pos_o2 = np.zeros((3, 3))
    false_pos_o5 = np.zeros((3, 3))

    for i, N in enumerate(Ns):
        print(f"N={N}")

        keys = Utils.read_file(f"Data/K_{N}.txt")
        test_keys_p0 = Utils.read_file(f"Data/Kp_{N}_0.txt")
        test_keys_p10 = Utils.read_file(f"Data/Kp_{N}_10.txt")
        test_keys_p25 = Utils.read_file(f"Data/Kp_{N}_25.txt")
        test_keys_p50 = Utils.read_file(f"Data/Kp_{N}_50.txt")

        gammas = [1. / (2 ** 7), 1. / (2 ** 8), 1 / (2. ** 10)]
        b = [7, 8, 10]

        hashfn = Utils.hash_keys

        for j, gamma in enumerate(gammas):
            print(f"    gamma={gamma}")
            mph = BBHash.build_bbhash(keys=keys, hashfn=hashfn, N=N)
            fpa = FA.FingerprintArray(b=b[j], N=N)
            fpa.populate(mph=mph, keys=keys, hashfn=Utils.hash_keys)

            sizes[j, i] = mph.__sizeof__() + fpa.get_size()
            # sizes[j, i] = mph.backend.num_bits

            start = time.time_ns()
            query_p0 = fpa.query(keys=test_keys_p0, mph=mph, hashfn=hashfn)
            end = time.time_ns()
            times_o0[j, i] = end - start
            truth = Utils.true_is_in(test_keys=test_keys_p0, keys=keys)
            comb = [truth[i] == query_p0[i] for i in range(len(truth))]
            false_pos_o0[j, i] = N - sum(bool(x) for x in comb)
            Utils.check_false_neg(truth=truth, query=query_p0)

            start = time.time_ns()
            query_p1 = fpa.query(keys=test_keys_p10, mph=mph, hashfn=hashfn)
            end = time.time_ns()
            times_o1[j, i] = end - start
            truth = Utils.true_is_in(test_keys=test_keys_p0, keys=keys)
            comb = [truth[i] == query_p1[i] for i in range(len(truth))]
            false_pos_o1[j, i] = N - sum(bool(x) for x in comb)
            Utils.check_false_neg(truth=truth, query=query_p1)

            start = time.time_ns()
            query_p2 = fpa.query(keys=test_keys_p25, mph=mph, hashfn=hashfn)
            end = time.time_ns()
            times_o2[j, i] = end - start
            truth = Utils.true_is_in(test_keys=test_keys_p0, keys=keys)
            comb = [truth[i] == query_p2[i] for i in range(len(truth))]
            false_pos_o2[j, i] = N - sum(bool(x) for x in comb)
            Utils.check_false_neg(truth=truth, query=query_p2)

            start = time.time_ns()
            query_p5 = fpa.query( keys=test_keys_p50, mph=mph, hashfn=hashfn)
            end = time.time_ns()
            times_o5[j, i] = end - start
            truth = Utils.true_is_in(test_keys=test_keys_p0, keys=keys)
            comb = [truth[i] == query_p5[i] for i in range(len(truth))]
            false_pos_o5[j, i] = N - sum(bool(x) for x in comb)
            Utils.check_false_neg(truth=truth, query=query_p5)

    return sizes, times_o0, times_o1, times_o2, times_o5, false_pos_o0, \
           false_pos_o1, false_pos_o2, false_pos_o5


if __name__ == '__main__':
    res = main()
    plot(res)
