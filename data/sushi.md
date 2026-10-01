# Sushi A and B: respondent preference orders

[Data catalogue](README.md) · [Prediction](../docs/repeated_holdout.md) · [Learning curves](../docs/learning_curves.md) · [Structural controls](../docs/structural_controls.md)

## Source and files

Toshihiro Kamishima's [SUSHI data page](https://www.kamishima.net/sushi/) provides the [2016 archive](https://www.kamishima.net/asset/sushi3-2016.zip). Its exact bytes are recorded in [sources.json](sources.json). The archive URL is mutable; SHA256 identifies the used version. The source's terms prohibit redistribution without permission.

| File | Contents | Use |
|---|---|---|
| `sushi3a.5000.10.order` | 5,000 complete orders of the same ten items | Sushi A fit and test |
| `sushi3b.5000.10.order` | 5,000 complete orders of ten displayed items from a 100-item catalogue | Sushi B fit and test |
| `sushi3b.5000.10.score` | Five-point item ratings, with −1 for unobserved ratings | Not used |
| `sushi3.udata` | Respondent ID and ten user attributes/codes | Row correspondence; region used only in an identified diagnostic |
| `sushi3.idata` | Item ID, name, style/category and aggregate item attributes | Source interpretation; not model covariates |
| Archive README files | Format, identity correspondence, elicitation and terms | Provenance |

The user fields are ID, sex, age category, response time, childhood prefecture/region/east–west code, current prefecture/region/east–west code, and a childhood/current prefecture difference indicator. Item fields are ID, name, roll/other style, seafood/other category, detailed food category, oiliness, eating frequency, normalized price and availability. The ranking models use none of these attributes. The numerical scores are not sorted to manufacture ranking reports.

## Reading an order file

An `.order` file is plain text. Its first line gives the catalogue size and a format marker. Every following row has the form:

```text
0 10 item_1 item_2 ... item_10
```

The leading zero is a format field, not a participant ID; `10` is the ranking length. The remaining ten labels are in most-preferred-first order. One row corresponds to the same row of `sushi3.udata`. A and B use separate item-ID catalogues, so a numeric ID should not be matched between them without the source dictionary.

The loader reads the declared full catalogue, checks the prefix and ten distinct in-range labels, and retains every row. **Sushi B is a complete ranking of its ten-item display, not the top ten favorites selected from an observed ranking of all 100.** Neither task supplies a true population preference order.

## Sizes, coverage and dependence

A has n=r=10, one display and full pair exposure. B has n=100, r=10 and 4,983 distinct displays among 5,000 reports. Its full source observes 4,809 of 4,950 possible pairs; item frequencies range 50–1,546. B's display design is strongly nonuniform. Keeping the full catalogue preserves the intended task but does not ensure a unique finite PL fit at small budgets.

The same 5,000 respondents supplied A and B. Within each task there is one ranking per respondent. Experimental split keys align A/B membership so the same person occupies the same split in both tasks. Demographic balance is not enforced. A/B results are separate prediction tasks from a shared sample, not independent replications of a population claim.

P1/P2 use N=3,000, discovery=1,000, confirmation=1,000. For A, λ=μ=3,000; for B, λ=27.2727 and μ=300. L1 instead uses a 4,000-person outer development pool, nested budgets, and a fixed 1,000-person test. L2 uses B's small budgets. C1 uses saved fits for pair/shell/context and common-order or optimization controls. The Sushi B region adjustment uses the released current east/west code in diagnostic cells only.
