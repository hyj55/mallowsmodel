# References and provenance

The supplied unpublished manuscript, *Selective Mallows Estimation from Uniform
Partial Rankings: Minimax Kendall Risk, Efficient Algorithms, and Likelihood
Comparisons*, is the specification: §1.1 model, §2.5 sharp estimator,
§3 efficient hierarchy, §4.1 likelihood fitting, §4.3 beans protocol.
It is not included in the distributable repository.

1. Fotakis, D., Kalavasis, A., & Stavropoulos, K. (2021).
   **Aggregating Incomplete and Noisy Rankings.** AISTATS, PMLR 130, 2278–2286.
   [Paper and supplement](https://proceedings.mlr.press/v130/fotakis21a.html).
   Used for the selective model, literal PosEst, and localization-based MLE discussion.
2. Raman, K., & Joachims, T. (2014).
   **Methods for Ordinal Peer Grading.** KDD.
   [Author PDF](https://www.cs.cornell.edu/people/tj/publications/raman_joachims_14a.pdf).
   Used for the strict-subset, equal-reliability specialization of greedy MAL and the applied comparison precedent.
3. Conitzer, V., Davenport, A., & Kalagnanam, J. (2006).
   **Improved Bounds for Computing Kemeny Rankings.** AAAI.
   [AAAI PDF](https://cdn.aaai.org/AAAI/2006/AAAI06-099.pdf).
   Used for generic Kemeny optimization and lower-bound methodology; our implementation uses SciPy/HiGHS.
4. PlackettLuce package maintainers. **Preferred Bean Varieties in Nicaragua.**
   [Official dataset documentation](https://hturner.github.io/PlackettLuce/reference/beans.html).
   [Pinned data source](https://raw.githubusercontent.com/hturner/PlackettLuce/ea031f7b129910c518daabf7c3e769aa499ea639/data/beans.rda).
   Used for the 842-record dataset, assigned triples, response decoding, and season fields.
5. van Etten, J., et al. (2019).
   **Crop variety management for climate adaptation supported by citizen science.**
   PNAS, 116(10), 4194–4199.
   [Original study](https://www.pnas.org/doi/10.1073/pnas.1813720116).
   Original study credited by the beans documentation.
6. Kamishima, T. **SUSHI Preference Data Sets.**
   [Creator's data and license page](https://www.kamishima.net/sushi/).
   [Original 2016 archive](https://www.kamishima.net/asset/sushi3-2016.zip).
   Used for original order files and the prohibition on redistributing source data.
   File format is additionally documented in the README inside the downloaded archive.
7. Kamishima, T. (2003).
   **Nantonac Collaborative Filtering: Recommendation Based on Order Responses.** KDD.
   [Author PDF](https://www.kamishima.net/archive/2003-p-kdd.pdf).
   Acknowledgment of the Sushi data's originating research; this project is not collaborative filtering.
8. Mao, C., Weed, J., & Rigollet, P. (2018).
   **Minimax Rates and Efficient Algorithms for Noisy Sorting.** ALT, PMLR 83, 821–847.
   [Paper](https://proceedings.mlr.press/v83/mao18a.html).
   Background for independent-pair minimax and sieve methods; not used to pretend report pairs are independent.
9. SciPy developers. **`scipy.optimize.milp`.**
   [Official documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html).
   Solver status, time limits, and dual-bound semantics. Runtime used SciPy 1.17.0.
10. Turner, H. L., van Etten, J., Firth, D., & Kosmidis, I. (2020).
    **Modelling rankings in R: the PlackettLuce package.** Computational Statistics, 35, 1027–1057.
    [Paper](https://link.springer.com/article/10.1007/s00180-020-00959-3).
    [Official overview](https://hturner.github.io/PlackettLuce/articles/Overview.html).
    Used for direct subset PL modeling and finite regularized estimates. Our Python fit uses the manuscript's ridge objective, not the R package's default pseudo-rankings.

Data bytes, source URLs, seeds and software versions are recorded under `results/`.

11. Cantwell, G. T., & Moore, C. (2022). **Belief propagation for permutations,
    rankings, and partial orders.** Physical Review E 105, L052303.
    [Paper](https://arxiv.org/abs/2110.00513),
    [DOI](https://doi.org/10.1103/PhysRevE.105.L052303),
    [code](https://github.com/gcant/pairwise-comparison-BP).
    Page 5 and reference 27 identify ATP 2010–2019 and Sackmann's source.
12. Sackmann, J. **ATP Tennis Rankings, Results, and Stats.**
    [Original repository](https://github.com/JeffSackmann/tennis_atp).
    Original README and data dictionary define annual files and tournament dates.
    License: CC BY-NC-SA 4.0.
13. Aneeshers. **Tennis Sackmann archive.**
    [Pinned mirror](https://github.com/Aneeshers/tennis-sackmann-archive/tree/83733587353df8a41f2fd4f516147d5aa83f5a8d).
    Used because the original endpoint returned 404; original authorship stays
    with Jeff Sackmann. Accessed 2026-09-25.
