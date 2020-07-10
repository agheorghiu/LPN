namespace lpnETCF {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Oracles;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;

    // perform CNOT between b and qs, as determined by e vector
    // (e and qs are assumed to be of the same length)
    operation controlledFlips(b: Qubit, e: Int[], qs: Qubit[]): Unit {
        let numQubits = Length(qs);
        for (i in 0 .. numQubits - 1) {
            if (e[i] > 0) {
                CNOT(b, qs[i]);
            }
        }
    }

    // create a superposition over low-weight errors
    // error probability per qubit is p
    operation createErrVector(p: Double, qs: Qubit[]): Unit {
        let numQubits = Length(qs);
        let angle = 2.0 * ArcCos(Sqrt(1. - p));
        for (i in 0 .. numQubits - 1) {
            Ry(angle, qs[i]);
        }
    }

    // maps |x>|y> to |x>|Ax + y>
    // all operations are mod 2
    // A is m x n, x is n-dimensional, y is m-dimensional
    operation matrixTimesKet(A: Int[][], x: Qubit[], y: Qubit[]): Unit {
        let m = Length(A);
        let n = Length(A[0]);
        for (i in 0 .. m - 1) {
            for (j in 0 .. n - 1) {
                if (A[i][j] > 0) {
                    CNOT(x[j], y[i]);
                }
            }
        }
    }

    // create \sum_{x, b, e} |b>|x>|Ax + b \dot (As + e') + e>
    // e vectors are not in equal superposition, but in a superposition given by the probability p for individual errors
    // A is m x n, lpnInstance (As + e') is m-dimensional
    operation clawFreeLPN(A: Int[][], lpnInstance: Int[], p: Double): Result[] {
        let m = Length(A);
        let n = Length(A[0]);
        let numQubits = m + n + 1;
        mutable res = new Result[m];

        using (qs = Qubit[numQubits]) {
            let b = qs[0];
            let x = qs[1 .. n];
            let y = qs[n + 1 .. m + n];

            // create equal superposition over b and x states
            // state becomes \sum_{b, x} |b>|x>|0>
            H(b);
            ApplyToEach(H, x);            

            // create the weighted superposition over errors in last register
            // state becomes \sum_{b, x, e} alpha_e |b>|x>|e>
            createErrVector(p, y);

            // add Ax to last register
            // state becomes \sum_{b, x, e} alpha_e |b>|x>|Ax + e>
            matrixTimesKet(A, x, y);

            // add LPN instance controlled on b
            // state becomes \sum_{b, x, e} alpha_e |b>|x>|Ax + b \dot (As + e') + e>
            controlledFlips(b, lpnInstance, y);

            // measure last register
            set res = MultiM(y);

            // print quantum state
            DumpRegister((), qs[0 .. n]);

            ResetAll(qs);
        }

        return res;
    }

}