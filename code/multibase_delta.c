/*
 * multibase_delta.c — consecutive-prime Artin correlation for MANY bases in ONE pass.
 *
 * For each prime p we factor p-1 ONCE, then test primitive-root status for every
 * base in BASES.  We accumulate, per base:
 *   - global 2x2 joint counts (artin_n, artin_{n+1})
 *   - per-gap 2x2 joint counts (gaps up to GAP_MAX)
 * No CSV is written (disk is tight); results go to JSON at the end.
 *
 * Compile:
 *   gcc -O3 -o multibase_delta multibase_delta.c -lm
 *
 * Usage: ./multibase_delta <limit> <outfile.json>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define SEG_SIZE   (1 << 22)
#define SMALL_LIM  100000
#define GAP_MAX    300

static const int BASES[] = {2, 3, 5, 6, 7, 10, 11, 13, 17, 21, 29};
#define NB (int)(sizeof(BASES)/sizeof(BASES[0]))

static char  small_composite[SMALL_LIM + 1];
static long  small_primes[10000];
static int   n_small = 0;

static void build_small(void) {
    for (long i = 2; i <= SMALL_LIM; i++)
        if (!small_composite[i]) {
            small_primes[n_small++] = i;
            for (long j = i * i; j <= SMALL_LIM; j += i) small_composite[j] = 1;
        }
}

/* modular exponentiation with __int128 to avoid overflow */
static long powmod(long b, long e, long m) {
    long r = 1; b %= m; if (b < 0) b += m;
    while (e > 0) {
        if (e & 1) r = (long)(((__int128)r * b) % m);
        b = (long)(((__int128)b * b) % m);
        e >>= 1;
    }
    return r;
}

/* accumulators */
static long joint[NB][2][2];
static long gapjoint[NB][GAP_MAX + 1][2][2];
static long n_pairs = 0;

int main(int argc, char **argv) {
    long LIMIT = (argc > 1) ? atol(argv[1]) : 1000000000L;
    const char *out = (argc > 2) ? argv[2] : "multibase_results.json";

    build_small();
    memset(joint, 0, sizeof joint);
    memset(gapjoint, 0, sizeof gapjoint);

    char *seg = malloc(SEG_SIZE);
    if (!seg) { fprintf(stderr, "oom\n"); return 1; }

    long prev_p = 0;
    int  prev_art[NB];
    memset(prev_art, 0, sizeof prev_art);
    long count = 0;

    for (long lo = 2; lo <= LIMIT; lo += SEG_SIZE) {
        long hi = lo + SEG_SIZE - 1;
        if (hi > LIMIT) hi = LIMIT;
        memset(seg, 0, SEG_SIZE);
        for (int i = 0; i < n_small; i++) {
            long q = small_primes[i];
            if (q * q > hi) break;
            long start = (lo + q - 1) / q * q;
            if (start < q * q) start = q * q;
            for (long j = start; j <= hi; j += q) seg[j - lo] = 1;
        }
        for (long n = lo; n <= hi; n++) {
            if (seg[n - lo]) continue;
            long p = n;
            if (p < 5) continue;

            /* factor p-1 once */
            long pm1 = p - 1, tmp = pm1, fac[64]; int nf = 0;
            for (int i = 0; i < n_small; i++) {
                long d = small_primes[i];
                if (d * d > tmp) break;
                if (tmp % d == 0) { fac[nf++] = d; while (tmp % d == 0) tmp /= d; }
            }
            if (tmp > 1) fac[nf++] = tmp;

            int art[NB];
            for (int b = 0; b < NB; b++) {
                long a = BASES[b];
                if (a % p == 0) { art[b] = 0; continue; }
                int ok = 1;
                for (int i = 0; i < nf && ok; i++)
                    if (powmod(a, pm1 / fac[i], p) == 1) ok = 0;
                art[b] = ok;
            }

            if (prev_p) {
                long g = p - prev_p;
                n_pairs++;
                for (int b = 0; b < NB; b++) {
                    joint[b][prev_art[b]][art[b]]++;
                    if (g <= GAP_MAX) gapjoint[b][g][prev_art[b]][art[b]]++;
                }
            }
            prev_p = p;
            memcpy(prev_art, art, sizeof art);

            if (++count % 2000000 == 0) {
                fprintf(stderr, "  p=%ld  primes=%ld  pairs=%ld\n", p, count, n_pairs);
                fflush(stderr);
            }
        }
    }

    FILE *f = fopen(out, "w");
    fprintf(f, "{\n  \"limit\": %ld,\n  \"n_pairs\": %ld,\n  \"bases\": {\n", LIMIT, n_pairs);
    for (int b = 0; b < NB; b++) {
        fprintf(f, "    \"%d\": {\n", BASES[b]);
        fprintf(f, "      \"joint\": [[%ld,%ld],[%ld,%ld]],\n",
                joint[b][0][0], joint[b][0][1], joint[b][1][0], joint[b][1][1]);
        fprintf(f, "      \"gap\": {");
        int first = 1;
        for (int g = 2; g <= GAP_MAX; g++) {
            long t = gapjoint[b][g][0][0] + gapjoint[b][g][0][1]
                   + gapjoint[b][g][1][0] + gapjoint[b][g][1][1];
            if (!t) continue;
            if (!first) fprintf(f, ",");
            fprintf(f, "\n        \"%d\": [[%ld,%ld],[%ld,%ld]]", g,
                    gapjoint[b][g][0][0], gapjoint[b][g][0][1],
                    gapjoint[b][g][1][0], gapjoint[b][g][1][1]);
            first = 0;
        }
        fprintf(f, "\n      }\n    }%s\n", (b == NB - 1) ? "" : ",");
    }
    fprintf(f, "  }\n}\n");
    fclose(f);
    fprintf(stderr, "DONE primes=%ld pairs=%ld -> %s\n", count, n_pairs, out);
    return 0;
}
