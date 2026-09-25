# Data

## Inputs and why they are useful

| Task | Reports | Items n | Ranked items r | Item exposure range | Observed pairs |
|---|---:|---:|---:|---:|---:|
| Beans | 842 | 10 | 3 | 234–270 | 45 / 45 |
| Sushi A | 5,000 | 10 | 10 | 5,000 | 45 / 45 |
| Sushi B | 5,000 | 100 | 10 | 50–1,546 | 4,809 / 4,950 |

All responses used here are strict, complete rankings **within the displayed
set**. None is treated as a censored top-k ranking over the whole catalog.
None supplies a true population center. Center estimation error relative to
truth is evaluated only in simulations.

### Beans

[Official documentation](https://hturner.github.io/PlackettLuce/reference/beans.html)
describes field trials of ten bean varieties in Nicaragua over five growing
seasons. Each report identifies three assigned varieties and the best and worst
of the three. We recover the middle item and form a strict three-item ranking.
The separate better/worse comparisons with a local variety are not used.

The loader validates missing fields, distinct varieties, and different valid
best/worst labels. **All 842 records pass; zero reports are excluded.** Labels
are sorted and mapped to integers. Every pair occurs 44–65 times. Season
counts are Ap15: 481, Po15: 177, Ap16: 87, Pr16: 64, and Po16: 33.
Climate and location fields are not predictors in the primary models.

This is the main small-item partial-ranking task, so the SM center can be
optimized exactly. There is no assessor ID; record-level splits cannot rule
out dependence from repeated farmers. The temporal follow-up trains on the
658 reports labeled 2015 and tests on the 184 labeled 2016.

### Sushi A and B

The [creator's 2016 archive](https://www.kamishima.net/sushi/) provides order
responses from 5,000 respondents. A ranks the same ten items; B ranks ten items
from a catalog of 100. Their respondent rows are aligned, and the experiments
use the same respondent split for both tasks. They are fitted separately.

The parser reads `sushi3a.5000.10.order` and `sushi3b.5000.10.order`, checks the
strict-order format and item ranges, and keeps the original item IDs. Display
order within a record is never shuffled. Ratings are not used. A B-only
diagnostic uses the current east/west-region field (zero-based column 9 of
`sushi3.udata`); it does not enter either primary fit.

A provides an exact-optimization control. B tests scalability and varying
display contexts. B exposure is strongly nonuniform: pair counts range from
0 to 462, and 141 possible pairs never co-occur. Uniform-design risk guarantees
are therefore not asserted for these real data. The original Sushi study's
sampling description is credited in [References](../docs/references.md).

## Access and version control

```bash
python download_data.py
python download_data.py --verify-only
```

The loader rejects byte-size or SHA256 mismatches. It never silently updates
the experiment to a new upstream version. [sources.json](sources.json) is the
pinned input manifest; `results/data_audit.json` records parsed coverage.

| File | Distribution | SHA256 |
|---|---|---|
| `raw/beans.rda` | Bundled unchanged from the pinned PlackettLuce source | `bdf799913727b3d0e75c5a4276f77fe8e0abdc9605707c7755ccb04e33ef9b6c` |
| `raw/sushi3-2016.zip` | Downloaded from the creator; ignored by Git | `4f8bbf3acd6f796cb3d0add6c73c394664982c57d3b48e75e92014e5278558a8` |

Beans is taken from PlackettLuce commit
`ea031f7b129910c518daabf7c3e769aa499ea639`, whose `DESCRIPTION` specifies GPL-3.
See [license and attribution](../THIRD_PARTY_NOTICES.md).
The Sushi creator permits research use and prohibits redistribution. Do not
commit the archive, extracted rankings, or respondent-level loss caches.

Simulated reports are generated directly by `src/models.py` using the recorded
seeds and settings; synthetic source observations are regenerated, not stored.
Aggregate simulated results are included under `results/`.

## ATP tennis extension

src/tennis.py downloads Sackmann's 2009–2019 main-tour singles files from
archive commit 83733587353df8a41f2fd4f516147d5aa83f5a8d. The first year defines
the initial prior-season catalog; evaluation covers 2010–2019. Immutable URLs,
byte counts and SHA256 hashes are recorded in data/tennis_sources.json.
Raw CSVs are excluded from Git. The source date denotes tournament starts,
not exact match times; chronological splits preserve tournaments. Invalid or
incomplete matches and out-of-catalog players are excluded and counted.

No real dataset has a supplied true center or a verified uniform display
design. Numeric lambda<1 is available from ATP and small report subsets of
Beans/Sushi B. See [the exposure report](../docs/exposure_analysis.md).
