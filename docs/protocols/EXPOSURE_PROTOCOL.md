# Exposure-regime extension protocol

Date: 2026-09-25; seed 20260925. This recovered copy records the settings used
in the completed local experiment. The original pre-fit protocol hash was
9d86cde0996f2a5b48d25feb38da20c7a1606c02d6738c11356e7d614de274a2.
This is a reconstruction from the recorded run, not the original byte-for-byte
protocol file or a retroactive registration.

## Models, algorithms, and target

Use the manuscript's direct selective Mallows model. Sample subsets first,
then rank directly within each subset. Do not delete items from a latent full
Mallows ranking. Conditional whole-ranking NLL is the predictive criterion.
Joint probabilities are excluded. Center accuracy uses Kendall distance only
when the generating order is known.

Algorithm 2.1 uses proof constants, fresh pilot batches, one independent
uniform pair extraction per report/block without using orientations in pair
selection, and the exact greedy maximal permutation sieve of Lemma 2.11.
Its radius is m*choose(m,2)/k; separation is strictly greater than the radius.
Enumerate labels lexicographically. Limit exact blocks to eight items;
larger exact sieves are unavailable, not substituted by MLE.

Algorithm 3.1 uses proof constants A=256 and the supplied beta0=.8, deterministic
candidate/batch schedules, accumulated offsets, and terminal block scores.
Record actual depth/fallback. For lambda>1, cap starting resolution at 1 as an
empirical extension without a theorem claim. Exact DP is the center MLE at n=8
and for Beans n=10. Large real catalogs use insertion from the score order,
with a pairwise lower bound and no unearned global certificate.

Profile beta over [0,10], retaining cap-hit flags. Raw and shrunk predictions
are separate. N>=5: first floor(.8*N) training reports fit inner models; the
remainder selects beta multiplier in [0,.25,.5,.75,1] and PL ridge in [.1,1,10].
Then refit on all N. N<5: multiplier .5 and ridge 1 fixed without validation.
These defaults are sensitivities, not optimally established tiny-sample rules.

## Uniform simulations

Small grid n=8:
- r=2, N=[2,4,8,16,28,56,112].
- r=4, N=[1,2,4,8,16,64].
- r=8, N=[1,2,8,32], shown as a separate full-ranking endpoint.

Coverage grid n=64: r=[2,8,32], target lambda=[.03,.3,1,3];
N=max(1,round(lambda*n*(n-1)/(r*(r-1)))). Record actual exposure. Rounding
duplicates at r=32,N=1 are pooled as independent replicates of the same actual
design, not misrepresented as distinct exposures.

Two DGPs: SM beta=.8, and equally spaced PL log worths scaled to match the
SM expected inversion count for each n,r. Randomize true centers. Thirty
independent datasets per target design/DGP; tests contain 2000 reports at n=8,
1000 at n=64. Seed=data base+cell*1000+DGP*100+rep, with a 100000 offset for
coverage. Estimator seed is independently derived by
SeedSequence([data_seed,73471]); no tie-breaking stream reveals the truth.

Report lambda=N*r*(r-1)/(n*(n-1)), mu=N*r/n, -N*log(1-r/n), unseen items/pairs,
Kendall distance and its fraction of choose(n,2), runtime, actual depth,
sieve cardinality and NLL. The reference min(choose(n,2),n/lambda) is a
rate shape, not a numerical lower bound. C0 in the sufficient coverage
condition is unspecified. No finite test certifies worst-case minimax risk.

Use paired t intervals across independent datasets. Data-generated PL is
outside the SM model regardless of its numeric exposure. Do not compare
raw NLL magnitudes across report lengths.

## Real data

Use the original 20% outer test sets. Five seeded training permutations.
Beans budgets [2,5,10,14,30,100]; Sushi B [5,10,25,50,100,300].
Shuffle whole reports, never ranking positions. No constructed pairwise
pseudo-reports. Exact sharp sieve is unavailable for these catalog sizes.
Average training repetitions before the paired test-report bootstrap
(2000 resamples), conditional on fitted models.

ATP: pin archive commit 83733587353df8a41f2fd4f516147d5aa83f5a8d.
Download annual main-tour singles 2009–2019 plus original documentation/license.
The recovered downloader records SHA256 on first download from these immutable
URLs and verifies it on subsequent uses; it does not fetch a moving branch.

For each year 2010–2019, define the player catalog from retained previous-year
matches. Filter missing/self matches, walkovers, retirements, defaults,
abandoned and unfinished scores. Keep current-year matches inside the catalog;
count all exclusions. Train on tournament starts before July 1, test thereafter.
Inner training precedes April 1; April–June validates. No chronological shuffle.

Primary test: both players seen in full training. Secondary: all in-catalog
test matches with ordinary fitted-model predictions, explicitly counting cold
starts. Compare Section 3, insertion SM, and regularized BT/PL. Log loss is
primary, with Brier and calibration secondary. Bootstrap test tournaments
within years; aggregate annual differences by a t interval across ten years.
These intervals condition on fits and do not eliminate serial/player dependence.
There is no known real central ranking and no verified uniform matchup design.
