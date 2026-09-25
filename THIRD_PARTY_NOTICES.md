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

## ATP tennis

Data author: **Jeff Sackmann**, ATP Tennis Rankings, Results, and Stats,
https://github.com/JeffSackmann/tennis_atp. Data retain CC BY-NC-SA 4.0 terms.
The original endpoint was unavailable; source files are retrieved from
https://github.com/Aneeshers/tennis-sackmann-archive at commit
83733587353df8a41f2fd4f516147d5aa83f5a8d. Its original attribution and license
are preserved by the downloader. No source data ownership is claimed.

Raw annual CSVs and the per-match prediction cache are excluded from Git.
The repository distributes aggregate analyses and fitted parameters; any
source-derived material subject to the upstream license retains those terms.
Filtering and chronological splits are our analysis choices, not the source
paper's exact preprocessing. See data/tennis_sources.json and the original
license saved as data/licenses/ATP-CC-BY-NC-SA-4.0.txt after download.
