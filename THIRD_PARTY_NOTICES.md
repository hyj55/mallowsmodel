# Third-party data notices

## Beans

`data/raw/beans.rda` is an unchanged file from the PlackettLuce R package at
commit `ea031f7b129910c518daabf7c3e769aa499ea639`:

- [Original file](https://github.com/hturner/PlackettLuce/blob/ea031f7b129910c518daabf7c3e769aa499ea639/data/beans.rda)
- [Upstream license declaration](https://github.com/hturner/PlackettLuce/blob/ea031f7b129910c518daabf7c3e769aa499ea639/DESCRIPTION)
- [Dataset documentation](https://hturner.github.io/PlackettLuce/reference/beans.html)

That package specifies **GPL-3**. A copy is included as
[data/licenses/GPL-3.0.txt](data/licenses/GPL-3.0.txt), together with the pinned
upstream package metadata. Package authors: Heather Turner, Ioannis Kosmidis,
and David Firth; contributor: Jacob van Etten. Data are credited by the package
to van Etten et al. (2019), *Crop variety management for climate adaptation
supported by citizen science*, PNAS, DOI
[10.1073/pnas.1813720116](https://doi.org/10.1073/pnas.1813720116).

No modifications have been made to the bundled R data file. Its GPL terms apply
to that third-party material; this notice does not assign a project-wide license
to the original experiment code.

## Sushi

Sushi data are **not included**. They are downloaded directly from Toshihiro
Kamishima's website for research use. The creator's
[terms](https://www.kamishima.net/sushi/) prohibit redistribution.
Credit: Kamishima (2003), *Nantonac Collaborative Filtering: Recommendation
Based on Order Responses*, KDD. The downloaded archive includes its own README.

Git excludes the Sushi archive, processed respondent data, and private
per-report output caches. The repository contains aggregate analyses and fitted
model parameters, not copies of respondents' rankings.

## Other current sources

PrefLib Dots/Puzzle, the 2024 dots author release, gosset wheat, SP-Rank and the
tricot catalog are downloaded from pinned upstream sources; their raw files
are not redistributed here. Attribution and immutable versions appear in
[the reference list](docs/references.md) and [source manifests](data/README.md).
The tricot source declares CC BY-SA 4.0. Upstream terms continue to apply to
source-derived material. No ownership of these sources is claimed.

The additional Sounds/Beaches audit uses BayesMallows commit
`a26cf89d3142ea3499489730e7c2b3ef9a26bfb2`; PatrasIQ uses PrefLib dataset
00034 at commit `1a8e9a9d0ad02a2a2d7473e813d1ac3057264f80`. Original response
files and upstream R objects are downloaded directly, checksum-verified and
excluded from this repository. See the [extension references](docs/validation_extension.md)
for Crispino et al. (2019), Barrett and Crispino (2018), Vitelli et al. (2018)
and Caragiannis et al. (2017). The synthetic draw archive contains generated
observations only, not participant responses.

## Recovered original trial archive

The group-sensitivity experiment downloads Andrew Mao's original `voting-results.tar.gz`, linked from [his Code & Data page](https://www.andrewmao.net/code/). It retains 160 Puzzle and 160 2013-Dots trial files locally and verifies their aggregate frequencies against the pinned PrefLib sources. The original archive, raw trial rankings, Sounds records, per-report membership information and fit caches are not redistributed in this repository. Published summaries are derived aggregate analyses; no new license is assigned to the upstream material. Credit: Mao, Procaccia and Chen (AAAI 2013). The archive's URL is mutable, so its expected bytes and SHA256 are fixed in `data/group_sensitivity_sources.json`.

## Historical ATP analysis (retired)

The retired ATP pipeline credited Jeff Sackmann and retained CC BY-NC-SA 4.0
terms. That notice, mirror provenance and analysis are preserved in the
[pinned historical snapshot](docs/history.md). No current ATP results or
raw annual files are distributed on the active branch.
