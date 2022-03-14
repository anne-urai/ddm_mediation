# ddm_mediation
---

Simulate mediation data, and recover the mediation path parameters in a few ways.
For now, requires https://github.com/anne-urai/hddm.

## How to run
- Install `environment.yml` on [Leiden University's ALICE cluster](https://wiki.alice.universiteitleiden.nl/index.php?title=ALICE_User_Documentation_Wiki).
- `alice_job` will run `python generate_data.py`, producing the files in `data`
- `alice_job_lavaan` will run `Rscript fit_lavaan.R`
- `python plot_simfits.py` will show the correlation between ground-truth and recovered parameters

#### ToDo
- vary a-path (regression of X onto M between subj)
- stick to drift bias-only models: does lavaan find the same direct vs indirect vs. partial mediation paths?
- then see if we can distinguish z vs. v
- last: fit MEG data with HDDMnn and compare models with and without collapsing bounds

---

Anne Urai, Leiden University, 2022
