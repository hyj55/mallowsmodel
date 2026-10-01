# Dots 2013 and Puzzle: objective ordering and repeated trials

[Data catalogue](README.md) · [Prediction](../docs/repeated_holdout.md) · [Group analysis](../docs/group_sensitivity.md)

## Sources and task meaning

Mao, Procaccia and Chen's [2013 study](https://ojs.aaai.org/index.php/AAAI/article/view/8460) collected noisy orders of four dot images or four sliding puzzles. Participants order dot images by their number of dots and puzzles by difficulty associated with solution length. PrefLib provides the [Dots collection 00024](https://preflib.github.io/PrefLib-Jekyll/dataset/00024) and [Puzzle collection 00025](https://preflib.github.io/PrefLib-Jekyll/dataset/00025). Eight `.soc` files are pinned to PrefLib commit `1a8e9a9d0ad02a2a2d7473e813d1ac3057264f80` in [the source manifest](strict_feature_sources.json).

| Task ID | Four category labels | Reports | Group-analysis name |
|---|---|---:|---|
| `00024-00000001` | 200, 203, 206, 209 dots | 795 | `dots-3` |
| `00024-00000002` | 200, 205, 210, 215 dots | 794 | `dots-5` |
| `00024-00000003` | 200, 207, 214, 221 dots | 800 | `dots-7` |
| `00024-00000004` | 200, 209, 218, 227 dots | 794 | `dots-9` |
| `00025-00000001` | 11, 14, 17, 20 solution steps | 793 | `puzzle-11` |
| `00025-00000002` | 5, 8, 11, 14 solution steps | 795 | `puzzle-5` |
| `00025-00000003` | 7, 10, 13, 16 solution steps | 795 | `puzzle-7` |
| `00025-00000004` | 9, 12, 15, 18 solution steps | 797 | `puzzle-9` |

A **condition** fixes these four category values. A **trial** is one source stimulus set within that condition. The source archive contains 40 trials per condition, each with repeated rankings (typically near 20); 40 is a feature of that collection, not a number derived from the four items, a train/test split, or a model assumption.

## Variables and reconstruction

The PrefLib header supplies task title, alternative names, catalogue size, total reports and unique ranking count. Each data line stores a multiplicity and a strict order of four IDs. Expansion preserves every count and maps IDs 1–4 to 0–3. It yields 3,183 Dots and 3,180 Puzzle reports, all with n=r=4 and all six pairs observed. The one coded display per condition identifies difficulty categories, not one physical board set.

Andrew Mao's [Code & Data page](https://www.andrewmao.net/code/) links the [original voting archive](https://dl.dropboxusercontent.com/s/mf0mm153pe3f12w/voting-results.tar.gz). Its checksum and folder mapping are in [group_sensitivity_sources.json](group_sensitivity_sources.json). Each of the eight folders has 40 uniquely named trial files. Each line is an original four-category ranking; the filename supplies its trial identity. The loader verifies that the complete frequency distribution over all 24 orders exactly matches the corresponding PrefLib file.

| Information | Available? | Consequence |
|---|---|---|
| Difficulty/dot-count category | Yes | Consistent categorical coding within each condition |
| Original trial filename and membership | Yes, from the archive | Within-trial fitting and whole-trial holdout |
| Actual puzzle board or dot-image layout | Not recovered in these ranking files | Cannot model visual identity or verify cross-trial stimulus reuse |
| Globally unique physical-board ID | No | A category label is not such an ID |
| Cross-trial respondent ID or demographics | No | Cannot establish participant-disjoint trial holdout or respondent-bootstrap inference |
| Year/season/location per response | No usable fields in these ranking exports | No such stratification |

Different puzzles requiring the same number of solution steps can differ in human difficulty. A pooled fit treats category labels as common items; a local fit uses the fixed four stimuli of one trial. G1 evaluates this representational issue rather than assuming a common latent center across all boards. The external increasing-category order is an objective reference, not a known population SM center.

## Uses and coverage

P1/P2 expand the anonymous PrefLib frequencies and split reports; no trial stratification is used there. Their exact N values are listed in [task sizes](../docs/repeated_holdout.md#task-sizes). Since r=n=4, $`\lambda=\mu=N`$ and item/pair exposure is complete in every nonempty training subset. Fixed full displays permit shell diagnostics but no within-pair changing-display gap contrast.

G1 uses the original trial files, not a guessed assignment of anonymous expanded rows. It splits within all 40 trials or holds out entire trials and compares local, pooled and matched-budget fitting. Trial metadata route the local model; they are not fitted covariates. All four conditions remain separate. Repeated trial partitions do not supply the missing worker identities, so G1's empirical split ranges are descriptive.
