# ATP tennis: chronological pair prediction

[Data catalogue](README.md) · [Temporal experiment](../docs/temporal_prediction.md)

## Source and task

Match records originate from [Jeff Sackmann's tennis_atp repository](https://github.com/JeffSackmann/tennis_atp). The recorded acquisition uses the [archival mirror at 8373358](https://github.com/Aneeshers/tennis-sackmann-archive/tree/83733587353df8a41f2fd4f516147d5aa83f5a8d/atp), with annual 2009–2019 files, source attribution, dictionary and licence recorded in [the file manifest](https://github.com/hyj55/mallowsmodel/blob/89b21645d5f7eb463cc90c4e982c3a66ce805b41/data/tennis_sources.json). The 2009 file defines the first prior-season catalogue; predictions cover 2010–2019. This matches the period discussed by [Cantwell and Moore](https://arxiv.org/abs/2110.00513), but is not asserted to recover their exact source snapshot or marginal-likelihood analysis.

A completed match becomes the direct pair `[winner_id, loser_id]`, r=2. Players are the ranked items, not independent assessors. Repeated player identities across matches and years can induce dependence.

## Released variable groups

The mirror's [data dictionary](https://github.com/Aneeshers/tennis-sackmann-archive/blob/83733587353df8a41f2fd4f516147d5aa83f5a8d/atp/matches_data_dictionary.txt) describes:

| Fields | Meaning | Use in this experiment |
|---|---|---|
| `tourney_id`, `tourney_name`, `surface`, `draw_size`, `tourney_level`, `tourney_date`, `match_num` | Tournament identity/design/date and match index | IDs for grouping, date for allocation, stable ordering; surface retained for descriptive records |
| `winner_id`, `loser_id` | Stable player identifiers | Item catalogue and pair outcome |
| Winner/loser `name`, `seed`, `entry`, `hand`, `ht`, `ioc`, `age` | Player identity and characteristics | Not fitted covariates |
| `score`, `best_of`, `round`, `minutes` | Match outcome/format/duration | Score determines completed-match eligibility; other fields not fitted |
| Winner/loser `rank`, `rank_points` | Published ranking information | Not supplied to either model |
| `w_`/`l_` fields `ace`, `df`, `svpt`, `1stIn`, `1stWon`, `2ndWon`, `SvGms`, `bpSaved`, `bpFaced` | Match serving statistics | Not fitted covariates |

No human rating or top-k list is constructed from these fields.

## Explicit eligibility and coverage

Discard rows missing winner, loser, tournament date or score; self-matches; and scores containing walkover, retirement, default, abandonment or unfinished markers (`W/O`, `RET`, `DEF`, `ABD`, `ABN`, `UNF`). Within each prediction year, fix the catalogue to players in eligible matches in the **previous season**, before inspecting that year's test outcomes. Matches containing out-of-catalogue players are excluded and counted. These rules define a completed-match, prior-catalogue target rather than all professional tennis outcomes.

The ten catalogues have 418–469 players. January–June has 1,444–1,636 training matches; training λ≈0.0144–0.0177 and μ≈6.64–7.46. Exposure is highly nonuniform: some catalogue players have no training matches. The main evaluation has 9,495 July–December matches with both players seen in training; the separate all-catalogue target includes 10,082, of which 587 contain a training-unseen player. These are distinct evaluation denominators.

Tournament start date controls the split, so complete tournaments remain on one side. January–March / April–June supplies inner tuning; January–June / July–December supplies final train/test. No outer temporal shuffle is performed. Surface, age and country are not balanced across periods or modeled. Tournament bootstrap intervals preserve dependence within a tournament but cannot remove dependence from players recurring across tournaments or serially across years.
