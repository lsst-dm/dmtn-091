..

:tocdepth: 1

.. Please do not modify tocdepth; will be fixed when a new Sphinx theme is shipped.

.. sectnum::

.. TODO: Delete the note below before merging new content to the master branch.

   **This technote is not yet published.**

   Planning out datatests for regular monitoring of the LSST DM Science Pipelines from continuous integration testing and regression monitoring through to large-scale performance reports.

.. Add content here.
.. Do not include the document title (it's automatically added from metadata.yaml).

========
Abstract
========

This document serves to define dataset types and sizes for semi-automated monitoring of scientific performance of the LSST DRP and AP pipelines. It does not cover datasets for testing the full DM system such as data acquisition, data transport, data loading, or the LSST Science Platform.

We start with a summary recommendation for a minimal set of datasets that would be suitable for performance monitoring, regression testing, and estimation of Key Performance Metrics (KPMs) for the LSST DM Science Pipelines.
We next define and provide guidelines for the processing workflow and cadence, and monitoring and assessment of test datasets divided into groups.  We refer to these groups as CI, SMALL, MEDIUM, and LARGE datasets.
We finally present more detailed discussion of the existing and near-future planned datasets for DRP and AP Science Performance monitoring.

We provide some approximate sizes of datasets here, however the singular reference for all sizing is the Data Management Sizing Model, `DMTN-135 <https://dmtn-135.lsst.io/>`_. Table 32 in `DMTN-135 <https://dmtn-135.lsst.io/>`_ provides current values for dataset sizes.


=================
Executive Summary
=================

1. DRP Scientific Performance Monitoring can be primarily accomplished through monthly processing of the HSC RC2 dataset from the SSP survey and the DESC DC2 simulated dataset, supplemented by less frequent processing of the much larger HSC PDR2. This needs to be supplemented by HSC observations in crowded fields.
2. AP Scientific Performance Monitoring can be accomplished through analysis of the DECam HiTS survey, HSC SSP PRD2-PDR1, *plus* an additional high-cadence multi-band survey.
3. Datasets for Continuous Integration (CI)-level tests and regression monitoring can be constructed out of subsets from the full DRP and AP dastasets identified above.  Several such datasets currently exist and are being regularly tested through USDF and Jenkins and are being monitored in SQuaSH.


=======================
Dataset Types and Goals
=======================

We identify 4 scales of datasets: CI, SMALL, MEDIUM, and LARGE.  These are meant to span a range of computational requirements, response time, and fidelity of performance measurements.

CI
--

  - Goals

    - Test that key initial processing steps execute
    - Allow checks for reasonable ranges of, for example,

      - Numbers of stars
      - Photometric zeropoints

  - Requirements

    - Runs less than 15 minutes wall time on 16 cores
    - Good data that is expected to be successfully processed.
    - Can be run by developer on an individual machine

  - Steps

    - Instrument-Signature Removal
    - Single-Frame Processing


SMALL
-----

  - Goals

    - Fuller integrated testing
    - Verify that DIA works
    - Monitor quantities to 25%:

      - Numbers of stars
      - zeropoints
      - KPMs
      - Numbers of detected DIA sources

  - Requirements

    - Less than 8 hours on 16-32 cores
    - Coadd at least 5 detectors
    - Run image-image DIA

  - Steps

    - Instrument-Signature Removal
    - Single-Frame Processing
    - Coadd
    - Difference Image Analysis
    - Forced Photometry


MEDIUM
------

  - Goals

    - Monitor quantities to 10%, both static sky and DIA
    - Include known edge cases
    - Suitable for daily tracking of regression both in metrics and robustness
    - Generate DRP/DPDD by running SDM Standardization.

  - Requirements

    - 24 hours on 64-128 cores
    - At least 2 filters
    - Coadd at least 5 full focal-plane images per filter
    - Run image-template DIA

  - Steps

    - Instrument-Signature Removal
    - Single-Frame Processing
    - Coadd
    - Multiband detection, merging, and measurement
    - Difference Image Analysis
    - Forced Photometry


LARGE
-----

  - Requirements

    - 168 hours on 512 cores
    - At least 3 filters
    - Coadd at least 10 full focal-plane images/filter
    - Run image-template DIA for 5 epochs of same field

  - Goals

    - Peformance Report for static sky and DIA.  Monitor numbers to 5%.
    - KPMs numbers should be suitable to predict full survey performance to ~50%
    - Generate DRP/DPDD
    - Allow testing of loading of data into DAX.

  - Steps

    - Instrument-Signature Removal
    - Single-Frame Processing
    - Coadd
    - Multiband detection, merging, and measurement
    - Difference Image Analysis
    - Forced Photometry
    - Ingest of DRP data into database/DPDD structure

The SDM Standardization process to generate the DPDD should always be run for at least MEDIUM and LARGE datasets. However, if the process is fast enough, it should be run following the processing of all datasets.

=================
DRP Test Datasets
=================

The DRP team semi-regularly processes many of the following datasets at different scales.

CI
--

`testdata_ci_hsc`
^^^^^^^^^^^^^^^^^

The `testdata_ci_hsc` package (https://github.com/lsst/testdata_ci_hsc) includes just enough data to exercise the main steps of the current pipeline: single-frame processing, coaddition, and coadd processing.  The input data comprises 33 CCD images from 12 HSC visits in r and i band, pre-made master darks, dome flats, sky flats, biases and detector defect files for these, and the necessary subset of the PS1-PV3 reference catalog.  These data total 8.3 GB.  The `ci_hsc` package is run to process the `testdata_ci_hsc` data automatically on a nightly basis by the CI system and can be explicitly included in developer-initiated CI runs on development branches.  The package also includes some simple tests to make sure that the expected outputs exist, but practically no tests of algorithmic or scientific correctness.  Both by name and content, this is a CI-level dataset as defined above.


`testdata_ci_imsim`
^^^^^^^^^^^^^^^^^^^

The `testdata_ci_imsim` package (https://github.com/lsst/testdata_ci_imsim) is intended to be similar to `testdata_ci_hsc`, but with simulated data from DESC Data Challenge 2 (DC2; see the `DC2 simulations overview paper <https://ui.adsabs.harvard.edu/abs/2021ApJS..253...31L/abstract>`_ and the `DESC DC2 Data Release Note <https://arxiv.org/abs/2101.04855>`_) instead of HSC data. The input data consists of 6 CCD images in each of the `ugrizy` bands, plus pre-generated calibrations (darks, flats, biases, detector defect files, and reference catalogs). These data total 5.5 GB. The `ci_imsim` package is run to process the `testdata_ci_imsim` data in developer-initiated CI runs on development branches. Typically both `ci_hsc` and `ci_imsim` are run in CI to confirm that the ticket being checked does not cause any issues in pipeline execution. Both by name and content, this is a CI-level dataset as defined above.

.. See https://jira.lsstcorp.org/browse/DM-26083


SMALL
-----

rc2_subset
^^^^^^^^^^

The `rc2_subset <https://github.com/lsst/rc2_subset>`_ dataset is a subset of the larger "HSC RC2" dataset that contains sufficient data to enable full, end-to-end processing with the Science Pipelines in a reasonable (few hours) time.
This dataset is processed through the entire Data Release Production (DRP) pipelines nightly for CI and data quality metrics monitoring purposes.
It is also used as a standalone dataset for tutorials and examples for using the data butler and the Science Pipelines.
Because it was intended to be small, `rc2_subset` should not be treated as a dataset intended for passing milestones or testing normative requirements.

The dataset consists of 5 central detectors plus one additional detector separated from the others (see figure below), for 8 randomly chosen visits in each of five HSC broadband filters -- HSC-G, HSC-R, HSC-I, HSC-Z, and HSC-Y.
These were specifically chosen from the COSMOS field (tract 9813 in the "hsc_rings_v1" skymap), so that translational dithers are minimal and the individual chips overlap each other.

.. figure:: /_static/rc2_subset_detectors.png
    :name: fig-rc2_subset_detectors

    Map of the HSC detectors in the focal plane, showing the 6 detectors (outlined in blue) included in the rc2_subset dataset. Note that the separation of one detector from the five centrally-located ones was an error that occurred during creation of the dataset. Because this dataset was in use for a long time before noticing this issue, we have retained it in this state for consistency with previous results based on rc2_subset.

These data are regularly run through all steps of the DRP pipeline, from single-frame through coaddition. Some custom configuration is necessary, however, for FGCM. The pipeline definition YAML file containing this custom configuration can be found in $DRP_PIPE_DIR/pipelines/HSC/DRP-RC2_subset.yaml (where $DRP_PIPE_DIR gives the local path to the set-up version of `the drp_pipe package <https://github.com/lsst/drp_pipe/tree/main>`_).


MEDIUM
------

DC2-test-med-1
^^^^^^^^^^^^^^

The `DC2-test-med-1` dataset is made up of two tracts from the DESC Data Challenge 2 (DC2; see the `DC2 simulations overview paper <https://ui.adsabs.harvard.edu/abs/2021ApJS..253...31L/abstract>`_ and the `DESC DC2 Data Release Note <https://arxiv.org/abs/2101.04855>`_). Tract 3828 contains a total of 288 visits over the six `ugrizy` bands, and tract 3829 has 227 contributing visits.

This DC2 dataset is reprocessed monthly at the USDF using the full DRP pipeline, which includes standard single-frame processing and onward through coaddition, as well as difference imaging. Data quality plots are generated by `analysis_tools` tasks, and their associated data quality metrics are dispatched to the `Sasquatch <https://sasquatch.lsst.io/>`_ database and displayed on chronograf dashboards for monitoring.

The `DC2-test-med-1` data are currently available in a shared Butler repository at the USDF as `/repo/dc2`. The `DC2-test-med-1` dataset was defined on Jira tickets `DM-22954 <https://jira.lsstcorp.org/browse/DM-22954>`_ and `DM-22816 <https://jira.lsstcorp.org/browse/DM-22816>`_.

The coadds reach average 5-sigma point-source depths (averaged over all patches in both tracts) of (25.9, 26.3, 25.9, 25.4, 24.0, 23.4) mag in (`u`, `g`, `r`, `i`, `z`, `y`) bands, equivalent to roughly the expected depth of five years of the LSST survey.

+-------+-------+-----------+----------------------------+
| Tract | Band  | NumVisits | VisitList                  |
+=======+=======+===========+============================+
| 3828  | u     | 22        | 2336, 2337, 179999, 180000,|
|       |       |           | 180001, 200936, 218326,    |
|       |       |           | 219143, 235057, 235058,    |
|       |       |           | 235149, 277060, 277061,    |
|       |       |           | 277093, 431192, 431193,    |
|       |       |           | 431405, 433038, 466711,    |
|       |       |           | 466712, 466756, 466758     |
+-------+-------+-----------+----------------------------+
| 3828  | g     | 28        | 159471, 159491, 183772,    |
|       |       |           | 183773, 183818, 183912,    |
|       |       |           | 193780, 193781, 193827,    |
|       |       |           | 221574, 221575, 221614,    |
|       |       |           | 221616, 254358, 254359,    |
|       |       |           | 254379, 254380, 254381,    |
|       |       |           | 254407, 400440, 419000,    |
|       |       |           | 419806, 430094, 466279,    |
|       |       |           | 479264, 480908, 484236,    |
|       |       |           | 484266                     |
+-------+-------+-----------+----------------------------+
| 3828  | r     | 64        | 162699, 181901, 193111,    |
|       |       |           | 193144, 193147, 193189,    |
|       |       |           | 193232, 193233, 193235,    |
|       |       |           | 193848, 193888, 199651,    |
|       |       |           | 202587, 202590, 202617,    |
|       |       |           | 202618, 202627, 202628,    |
|       |       |           | 212071, 212085, 212118,    |
|       |       |           | 212119, 212127, 212704,    |
|       |       |           | 212739, 212805, 212806,    |
|       |       |           | 213513, 213514, 213545,    |
|       |       |           | 219950, 236788, 236833,    |
|       |       |           | 242597, 252377, 252422,    |
|       |       |           | 252424, 257768, 257797,    |
|       |       |           | 271328, 271331, 300250,    |
|       |       |           | 300252, 398407, 398413,    |
|       |       |           | 401616, 401660, 414873,    |
|       |       |           | 415029, 416955, 436491,    |
|       |       |           | 436492, 436538, 440938,    |
|       |       |           | 448317, 451452, 451489,    |
|       |       |           | 451502, 452556, 452557,    |
|       |       |           | 456690, 456716, 467701,    |
|       |       |           | 479434                     |
+-------+-------+-----------+----------------------------+
| 3828  | i     |  78       | 174534, 177481, 192355,    |
|       |       |           | 204706, 204708, 211099,    |
|       |       |           | 211100, 211132, 211140,    |
|       |       |           | 211141, 211198, 211228,    |
|       |       |           | 211477, 211478, 211483,    |
|       |       |           | 211484, 211490, 211527,    |
|       |       |           | 211530, 211531, 211533,    |
|       |       |           | 211545, 214433, 214434,    |
|       |       |           | 214464, 214465, 214467,    |
|       |       |           | 227950, 227951, 227976,    |
|       |       |           | 227984, 228020, 228092,    |
|       |       |           | 230740, 230775, 244004,    |
|       |       |           | 244005, 244028, 244029,    |
|       |       |           | 244068, 248966, 248970,    |
|       |       |           | 256383, 263452, 263453,    |
|       |       |           | 263455, 263501, 263502,    |
|       |       |           | 263511, 280217, 280271,    |
|       |       |           | 397278, 397279, 397322,    |
|       |       |           | 397330, 397331, 410996,    |
|       |       |           | 421682, 421725, 427674,    |
|       |       |           | 428492, 428525, 433960,    |
|       |       |           | 433962, 433992, 433993,    |
|       |       |           | 457681, 457721, 457723,    |
|       |       |           | 457749, 471963, 471987,    |
|       |       |           | 472179, 479620, 491550,    |
|       |       |           | 496959, 496960, 496989     |
+-------+-------+-----------+----------------------------+
| 3828  | z     | 38        | 7997, 7998, 8003, 8029,    |
|       |       |           | 13288, 32680, 187502,      |
|       |       |           | 187533, 187556, 209015,    |
|       |       |           | 209018, 209031, 209032,    |
|       |       |           | 209061, 209062, 209063,    |
|       |       |           | 209068, 209843, 226983,    |
|       |       |           | 227030, 240852, 243019,    |
|       |       |           | 243021, 265317, 303559,    |
|       |       |           | 408907, 408941, 426672,    |
|       |       |           | 426969, 427030, 427069,    |
|       |       |           | 460088, 460130, 460131,    |
|       |       |           | 462543, 462714, 474849,    |
|       |       |           | 474890                     |
+-------+-------+-----------+----------------------------+
| 3828  | y     | 58        | 5884, 5886, 5891, 12454,   |
|       |       |           | 12466, 12471, 12481, 37656,|
|       |       |           | 37657, 37658, 167863,      |
|       |       |           | 167864, 169763, 169812,    |
|       |       |           | 169838, 169839, 189315,    |
|       |       |           | 189317, 189318, 189382,    |
|       |       |           | 190282, 190503, 191217,    |
|       |       |           | 206021, 206031, 206033,    |
|       |       |           | 206039, 206050, 206073,    |
|       |       |           | 206120, 207784, 207791,    |
|       |       |           | 266115, 266117, 266118,    |
|       |       |           | 266127, 282444, 282445,    |
|       |       |           | 282446, 306181, 306182,    |
|       |       |           | 306188, 390558, 406992,    |
|       |       |           | 406996, 407919, 407950,    |
|       |       |           | 407951, 425484, 443127,    |
|       |       |           | 444706, 444725, 456651,    |
|       |       |           | 458252, 458253, 458254,    |
|       |       |           | 458255, 492028             |
+-------+-------+-----------+----------------------------+
| 3829  | u     | 19        | 2334, 2336, 2337, 2339,    |
|       |       |           | 179999, 180000, 180001,    |
|       |       |           | 200750, 200813, 218326,    |
|       |       |           | 219143, 219917, 235058,    |
|       |       |           | 277060, 277061, 431405,    |
|       |       |           | 433038, 466756, 466758     |
+-------+-------+-----------+----------------------------+
| 3829  | g     | 22        | 159471, 159507, 183772,    |
|       |       |           | 183818, 193827, 194862,    |
|       |       |           | 221574, 221575, 221577,    |
|       |       |           | 221614, 221615, 221616,    |
|       |       |           | 254358, 254359, 254379,    |
|       |       |           | 254380, 254381, 254407,    |
|       |       |           | 271920, 419000, 484236,    |
|       |       |           | 484266                     |
+-------+-------+-----------+----------------------------+
| 3829  | r     | 51        | 40327, 162699, 193111,     |
|       |       |           | 193144, 193147, 193187,    |
|       |       |           | 193189, 193232, 193233,    |
|       |       |           | 193235, 193848, 193880,    |
|       |       |           | 193888, 202590, 202591,    |
|       |       |           | 202617, 202618, 212071,    |
|       |       |           | 212072, 212116, 212118,    |
|       |       |           | 212127, 212739, 212805,    |
|       |       |           | 212806, 213513, 213514,    |
|       |       |           | 213545, 213560, 219950,    |
|       |       |           | 219959, 236788, 236833,    |
|       |       |           | 242468, 242505, 242563,    |
|       |       |           | 242597, 252422, 257766,    |
|       |       |           | 271331, 300250, 300252,    |
|       |       |           | 398407, 401660, 414873,    |
|       |       |           | 436538, 440938, 448317,    |
|       |       |           | 452557, 456716, 467701     |
+-------+-------+-----------+----------------------------+
| 3829  | i     | 56        | 174534, 192355, 204706,    |
|       |       |           | 204708, 211099, 211100,    |
|       |       |           | 211132, 211141, 211198,    |
|       |       |           | 211228, 211478, 211484,    |
|       |       |           | 211490, 211527, 211531,    |
|       |       |           | 211533, 211540, 211544,    |
|       |       |           | 211545, 214433, 214434,    |
|       |       |           | 214464, 214465, 214467,    |
|       |       |           | 214468, 214558, 227882,    |
|       |       |           | 227883, 227917, 227950,    |
|       |       |           | 227951, 227976, 227984,    |
|       |       |           | 228020, 228092, 230740,    |
|       |       |           | 230774, 230776, 244029,    |
|       |       |           | 248970, 256353, 256383,    |
|       |       |           | 263502, 263511, 280216,    |
|       |       |           | 280217, 280271, 410996,    |
|       |       |           | 433960, 433992, 457681,    |
|       |       |           | 457723, 457749, 479620,    |
|       |       |           | 496960, 496989             |
+-------+-------+-----------+----------------------------+
| 3829  | z     | 26        | 7997, 7999, 8003, 8029,    |
|       |       |           | 8030, 8045, 13287, 13332,  |
|       |       |           | 32682, 209010, 209015,     |
|       |       |           | 209018, 209031, 209032,    |
|       |       |           | 209061, 209063, 209068,    |
|       |       |           | 209080, 226983, 240852,    |
|       |       |           | 240854, 243019, 303559,    |
|       |       |           | 426672, 460130, 462714     |
+-------+-------+-----------+----------------------------+
| 3829  | y     | 53        | 5882, 5884, 5886, 12453,   |
|       |       |           | 12454, 12466, 12471, 12481,|
|       |       |           | 37656, 37657, 37658,       |
|       |       |           | 167862, 167863, 167864,    |
|       |       |           | 167877, 169763, 169764,    |
|       |       |           | 169765, 169811, 169812,    |
|       |       |           | 169838, 169839, 189315,    |
|       |       |           | 189317, 189318, 189382,    |
|       |       |           | 190282, 206031, 206032,    |
|       |       |           | 206033, 206039, 206073,    |
|       |       |           | 207791, 207792, 246649,    |
|       |       |           | 266115, 266117, 266167,    |
|       |       |           | 266168, 267504, 282398,    |
|       |       |           | 282445, 284048, 306181,    |
|       |       |           | 306182, 306188, 406992,    |
|       |       |           | 407919, 425484, 443127,    |
|       |       |           | 444725, 456651, 458253     |
+-------+-------+-----------+----------------------------+



HSC RC2
^^^^^^^

The "RC2" dataset consists of two complete HSC SSP-Wide tracts and a single HSC SSP-UltraDeep tract (in the COSMOS field).  This dataset is processed monthly using the weekly releases of the DM stack.  The processing includes the entire current DM pipeline (including tasks that are not included in `ci_hsc`) as well as `analysis_tools` tasks, which generate a large suite of validation plots and associated metrics that are uploaded to the `Sasquatch <https://sasquatch.lsst.io/>`_ database and monitored on chronograf dashboards.  Processing currently requires some manual supervision, but we expect processing of this scale to eventually be fully automated.  See also https://confluence.lsstcorp.org/display/DM/Reprocessing+of+the+HSC+RC2+dataset.

The HSC RC2 data is presently (2024-02-21) available at the USDF in a shared Butler repository at `/repo/main/hsc`.  The HSC dataset was defined in a JIRA ticket: `Redefine HSC "RC" dataset for bi-weeklies processing <https://jira.lsstcorp.org/browse/DM-11345>`_

Particular attention was paid in defining this dataset for it to consist of mostly good data plus some specific cases known to be more challenging (see above JIRA issue for details).  Explicitly increasing the proportion of more challenging cases increases the efficiency of identifying problems for a fixed amount of compute resources at the expense of making the total scientific performance numbers less representative of the average quality for a full-survey-sized set of data.  This is a good tradeoff to make, but also an important point to keep in mind when using the processing results of such datasets to make predictions of performance of the LSST Science Pipelines on LSST data.

.. The monthly processing of this dataset is tracked at: `Reprocessing of the HSC RC2 dataset <https://confluence.lsstcorp.org/display/DM/Reprocessing+of+the+HSC+RC2+dataset#/>`_.

.. The DM Tech Note `DMTN-088 <https://dmtn-088.lsst.io/>`_ provides a brief introduction to the processing of this dataset at the LSST Data Facility (LDF).  There are some updates in the un-merged branch `DMTN-088 (DM-15546) <https://dmtn-088.lsst.io/v/DM-15546/index.html>`_

The fields are defined in the JIRA issue at `https://jira.lsstcorp.org/browse/DM-11345 <https://jira.lsstcorp.org/browse/DM-11345?focusedCommentId=90372&page=com.atlassian.jira.plugin.system.issuetabpanels:comment-tabpanel#comment-90372>`_ to be:

+-----------+-------+----------+-----------+----------------------------+
| Field     | Tract | Filter   | NumVisits | VisitList                  |
+===========+=======+==========+===========+============================+
| WIDE_VVDS | 9697  | HSC_G    | 22        | 6320,34338,34342,34362,    |
|           |       |          |           | 34366,34382,34384,34400,   |
|           |       |          |           | 34402,34412,34414,34422,   |
|           |       |          |           | 34424,34448,34450,34464,   |
|           |       |          |           | 34468,34478,34480,34482,   |
|           |       |          |           | 34484,34486                |
+-----------+-------+----------+-----------+----------------------------+
| WIDE_VVDS | 9697  | HSC-R    | 22        | 7138,34640,34644,34648,    |
|           |       |          |           | 34652,34664,34670,34672,   |
|           |       |          |           | 34674,34676,34686,34688,   |
|           |       |          |           | 34690,34698,34706,34708,   |
|           |       |          |           | 34712,34714,34734,34758,   |
|           |       |          |           | 34760,34772                |
+-----------+-------+----------+-----------+----------------------------+
| WIDE_VVDS | 9697  | HSC-I    | 33        | 35870,35890,35892,35906,   |
|           |       |          |           | 35936,35950,35974,36114,   |
|           |       |          |           | 36118,36140,36144,36148,   |
|           |       |          |           | 36158,36160,36170,36172,   |
|           |       |          |           | 36180,36182,36190,36192,   |
|           |       |          |           | 36202,36204,36212,36214,   |
|           |       |          |           | 36216,36218,36234,36236,   |
|           |       |          |           | 36238,36240,36258,36260,   |
|           |       |          |           | 36262                      |
+-----------+-------+----------+-----------+----------------------------+
| WIDE_VVDS | 9697  | HSC-Z    | 33        | 36404,36408,36412,36416,   |
|           |       |          |           | 36424,36426,36428,36430,   |
|           |       |          |           | 36432,36434,36438,36442,   |
|           |       |          |           | 36444,36446,36448,36456,   |
|           |       |          |           | 36458,36460,36466,36474,   |
|           |       |          |           | 36476,36480,36488,36490,   |
|           |       |          |           | 36492,36494,36498,36504,   |
|           |       |          |           | 36506,36508,38938,38944,   |
|           |       |          |           | 38950                      |
+-----------+-------+----------+-----------+----------------------------+
| WIDE_VVDS | 9697  | HSC-Y    | 33        | 34874,34942,34944,34946,   |
|           |       |          |           | 36726,36730,36738,36750,   |
|           |       |          |           | 36754,36756,36758,36762,   |
|           |       |          |           | 36768,36772,36774,36776,   |
|           |       |          |           | 36778,36788,36790,36792,   |
|           |       |          |           | 36794,36800,36802,36808,   |
|           |       |          |           | 36810,36812,36818,36820,   |
|           |       |          |           | 36828,36830,36834,36836,   |
|           |       |          |           | 36838                      |
+-----------+-------+----------+-----------+----------------------------+
| WIDE_VVDS | 9697  | TOTAL    | 143       | Size: 1.7 TB               |
+-----------+-------+----------+-----------+----------------------------+

+--------------+-------+--------+-----------+----------------------------+
| Field        | Tract | Filter | NumVisits | VisitList                  |
+==============+=======+========+===========+============================+
| WIDE_GAMA15H | 9615  | HSC_G  | 17        | 26024,26028,26032,26036,   |
|              |       |        |           | 26044,26046,26048,26050,   |
|              |       |        |           | 26058,26060,26062,26070,   |
|              |       |        |           | 26072,26074,26080,26084,   |
|              |       |        |           | 26094                      |
+--------------+-------+--------+-----------+----------------------------+
| WIDE_GAMA15H | 9615  | HSC-R  | 17        | 23864,23868,23872,23876,   |
|              |       |        |           | 23884,23886,23888,23890,   |
|              |       |        |           | 23898,23900,23902,23910,   |
|              |       |        |           | 23912,23914,23920,23924,   |
|              |       |        |           | 28976                      |
+--------------+-------+--------+-----------+----------------------------+
| WIDE_GAMA15H | 9615  | HSC-I  | 26        | 1258,1262,1270,1274,       |
|              |       |        |           | 1278,1280,1282,1286,       |
|              |       |        |           | 1288,1290,1294,1300,       |
|              |       |        |           | 1302,1306,1308,1310,       |
|              |       |        |           | 1314,1316,1324,1326,       |
|              |       |        |           | 1330,24494,24504,24522,    |
|              |       |        |           | 24536,24538                |
+--------------+-------+--------+-----------+----------------------------+
| WIDE_GAMA15H | 9615  | HSC-Z  | 26        | 23212,23216,23224,23226,   |
|              |       |        |           | 23228,23232,23234,23242,   |
|              |       |        |           | 23250,23256,23258,27090,   |
|              |       |        |           | 27094,27106,27108,27116,   |
|              |       |        |           | 27118,27120,27126,27128,   |
|              |       |        |           | 27130,27134,27136,27146,   |
|              |       |        |           | 27148,27156                |
+--------------+-------+--------+-----------+----------------------------+
| WIDE_GAMA15H | 9615  | HSC-Y  | 26        | 380,384,388,404,           |
|              |       |        |           | 408,424,426,436,           |
|              |       |        |           | 440,442,446,452,           |
|              |       |        |           | 456,458,462,464,           |
|              |       |        |           | 468,470,472,474,           |
|              |       |        |           | 478,27032,27034,27042,     |
|              |       |        |           | 27066,27068                |
+--------------+-------+--------+-----------+----------------------------+
| WIDE_GAMA15H | 9615  | TOTAL  | 112       | Size: 1.4 TB               |
+--------------+-------+--------+-----------+----------------------------+

+-----------+-------+--------+-----------+----------------------------+
| Field     | Tract | Filter | NumVisits | VisitList                  |
+===========+=======+========+===========+============================+
| UD_COSMOS | 9813  | HSC_G  | 17        | 11690,11692,11694,11696,   |
|           |       |        |           | 11698,11700,11702,11704,   |
|           |       |        |           | 11706,11708,11710,11712,   |
|           |       |        |           | 29324,29326,29336,29340,   |
|           |       |        |           | 29350                      |
+-----------+-------+--------+-----------+----------------------------+
| UD_COSMOS | 9813  | HSC-R  | 16        | 1202,1204,1206,1208,       |
|           |       |        |           | 1210,1212,1214,1216,       |
|           |       |        |           | 1218,1220,23692,23694,     |
|           |       |        |           | 23704,23706,23716,23718    |
+-----------+-------+--------+-----------+----------------------------+
| UD_COSMOS | 9813  | HSC-I  | 33        | 1228,1230,1232,1238,       |
|           |       |        |           | 1240,1242,1244,1246,       |
|           |       |        |           | 1248,19658,19660,19662,    |
|           |       |        |           | 19680,19682,19684,19694,   |
|           |       |        |           | 19696,19698,19708,19710,   |
|           |       |        |           | 19712,30482,30484,30486,   |
|           |       |        |           | 30488,30490,30492,30494,   |
|           |       |        |           | 30496,30498,30500,30502,   |
|           |       |        |           | 30504                      |
+-----------+-------+--------+-----------+----------------------------+
| UD_COSMOS | 9813  | HSC-Z  | 31        | 1166,1168,1170,1172,       |
|           |       |        |           | 1174,1176,1178,1180,       |
|           |       |        |           | 1182,1184,1186,1188,       |
|           |       |        |           | 1190,1192,1194,17900,      |
|           |       |        |           | 17902,17904,17906,17908,   |
|           |       |        |           | 17926,17928,17930,17932,   |
|           |       |        |           | 17934,17944,17946,17948,   |
|           |       |        |           | 17950,17952,17962          |
+-----------+-------+--------+-----------+----------------------------+
| UD_COSMOS | 9813  | HSC-Y  | 52        | 318,322,324,326,           |
|           |       |        |           | 328,330,332,344,           |
|           |       |        |           | 346,348,350,352,           |
|           |       |        |           | 354,356,358,360,           |
|           |       |        |           | 362,1868,1870,1872,        |
|           |       |        |           | 1874,1876,1880,1882,       |
|           |       |        |           | 11718,11720,11722,11724,   |
|           |       |        |           | 11726,11728,11730,11732,   |
|           |       |        |           | 11734,11736,11738,11740,   |
|           |       |        |           | 22602,22604,22606,22608,   |
|           |       |        |           | 22626,22628,22630,22632,   |
|           |       |        |           | 22642,22644,22646,22648,   |
|           |       |        |           | 22658,22660,22662,22664    |
+-----------+-------+--------+-----------+----------------------------+
| UD_COSMOS | 9813  | NB0921 | 28        | 23038,23040,23042,23044,   |
|           |       |        |           | 23046,23048,23050,23052,   |
|           |       |        |           | 23054,23056,23594,23596,   |
|           |       |        |           | 23598,23600,23602,23604,   |
|           |       |        |           | 23606,24298,24300,24302,   |
|           |       |        |           | 24304,24306,24308,24310,   |
|           |       |        |           | 25810,25812,25814,25816    |
+-----------+-------+--------+-----------+----------------------------+
| UD_COSMOS | 9813  | TOTAL  | 177       | Size: 3.2 TB               |
+-----------+-------+--------+-----------+----------------------------+

This dataset satisfies the definition above for a MEDIUM dataset.

LARGE
-----


HSC RC3 (proposed)
^^^^^^^^^^^^^^^^^^

As survey operations approaches and our ability to process and analyze larger datasets increases, there is a need for a dataset that is more substantial than RC2, allowing us to identify and test the handling of more "edge cases" by the science pipelines. We thus propose the creation of an HSC "RC3" dataset that has the following characteristics:

  - Covers a contiguous area that spans more than a tract in size
  - Contains data taken with multiple physical filters that map to the same "effective" filter (e.g., both HSC-I and HSC-I2, which map to "i")
  - Is sufficient for creating templates for AP difference imaging in the COSMOS field
  - Provides a long time baseline sufficient to measure proper motions and parallaxes
  - Includes data with rotational dithers
  - Includes "all" HSC visits in the COSMOS field for "full-depth" testing of pipelines
  - Samples fields at both high and low Galactic latitudes

**Proposal:**

We will retain all data that are currently part of RC2, which were selected to represent some edge cases. All data proposed below will be in addition to the existing RC2 data. Because the COSMOS field lies within a larger WIDE region of the HSC-SSP, we propose to include *all* COSMOS data in RC3, plus adjacent tracts from the WIDE footprint that create a contiguous field extending to the "edge" of the survey footprint. (Suggestion: include tracts 9812-9814, 9569-9572, and 9326-9329; see the figure below for a map of HSC tracts.) This enables all of the following:

  - Full survey depth coadds in the COSMOS field.
  - COSMOS "truth" table of deep HST galaxy, star, and transient/variable measurements for comparison.
  - COSMOS provides a long time baseline over which to validate parallax/proper motion algorithms (though the lack of dithering may be an issue; including dithered WIDE data may alleviate this).
  - COSMOS has data from both HSC-I/HSC-I2 and also HSC-R/HSC-R2. We can thus test processing on, e.g., only HSC-I, only HSC-I2, or the combination of them both.
  - The large number of visits in COSMOS means we can create independent coadds consisting of separate sets of visits.
  - Extending over a large area provides a dataset to use in developing QA tools (e.g., survey property maps).
  - Extends to the edge of the survey footprint to explore issues near survey boundaries.
  - Can use WIDE data when proper dithering is required, but COSMOS data when depth is more important.

**Additional considerations:**

  - COSMOS and the current RC2 dataset provide little variation in declination or Galactic latitude. We may need to include some Subaru+HSC PI data to get higher source densities.
  - We could consider cherry-picking some region(s) of the sky with, e.g., a known rich galaxy cluster (e.g., RC2's tract 9615 was selected for this reason + a big galaxy), Galactic cirrus, a nearby globular cluster or dwarf galaxy, or other features to enable exercising/testing specific algorithms and capabilities.
  - It is vital to inject synthetic sources into data for validation purposes. However, the details of what types of sources to inject, how many tracts to inject them into, and others can be decided after the RC3 dataset has been created.

.. figure:: /_static/tracts_patches_W_w03_HSC-I_trimmed.png
    :name: fig-HSC_fields

    Map of the HSC-SSP tracts in the region near the COSMOS field (centered on tract 9813). The proposed RC3 dataset would contain tracts 9812-9814, 9569-9572, and 9326-9329, including *all* data from the DEEP/ULTRADEEP layers in the COSMOS field.

This section is a condensed encapsulation of discussion that took place on `this Confluence page <https://confluence.lsstcorp.org/x/vY1cC>`_; for more details about the considerations that were discussed, please consult that page.


HSC SSP PDR1 and PDR2
^^^^^^^^^^^^^^^^^^^^^

The full HSC SSP Public Data Release 1 (PDR1) dataset has been processed by LSST DM twice.  This is a LARGE dataset.  The timescale for these runs is essentially as-needed.  The processing of these large datasets could be increased as the workflow and orchestration tooling for automated execution improves.  We expect this scale of processing to always require some manual supervision (but significantly less than it does today).  As more data becomes available with future SSP public releases, we expect this dataset to grow to include them.

See reports at:

  - `Cycle S17 HSC PDR1 Processing <https://confluence.lsstcorp.org/display/DM/S17B+HSC+PDR1+reprocessing>`_
  - `Cycle S18 HSC PDR1 Processing <https://confluence.lsstcorp.org/display/DM/S18+HSC+PDR1+reprocessing/>`_

The HSC Public Data Release 2 (PDR2) dataset was released by HSC in the Summer of 2019.  This dataset is being copied to NCSA and will be available at `/datasets/hsc/raw/ssp_pdr2`.  PDR2

  - Contains 5654 visits in 7 bands (grizy plus two narrow-band filters)
  - Covers 119 tracts
  - Data from 3 survey tiers: WIDE, DEEP, UDEEP
  - Is 13 times larger than RC2
  - Takes 80,000 core hours.  80% of this is spent in the full multiband processing

It is appropriate for DRP and for AP testing and performance monitoring.  As with PDR1, PDR2 is similarly a LARGE dataset.


DESIRED DATASETS
----------------

In the future, there are at least two additional dataset needs:

Less Large LARGE
^^^^^^^^^^^^^^^^

Some important features of data are sufficiently rare that it's hard to include all of them simultaneously in just the three tracts of the RC dataset.  A dataset between the RC and PDR1/2 scales, run perhaps on monthly timescales (especially if RC processing can be done weekly as automation improves), would be useful to ensure coverage of those features.  10-15 tracts is probably the right scale.

Missing Features
^^^^^^^^^^^^^^^^

Three important data features are missed in all of the datasets described above, as they are generically missing all datasets that are subsets of HSC SSP PDR1/2 and RC2:

  - Differential chromatic refraction (HSC has an atmospheric dispersion corrector)

  - LSST-like wavefront sensors (HSC's are too close to focus to be useful for learning much about the state of the optical system)

  - Crowded stellar fields

A (not yet identified) DECam dataset could potentially address all of these issues, but characterizing the properties of DECam at the level already done for HSC may be difficult, and would probably be necessary to fully test the DM algorithms for which DCR and wavefront sensors are relevant (e.g., physically-motivated PSF modeling).  Many non-PDR1/2+RC2 HSC datasets do include more interesting variability or crowded fields, so it *might* be most efficient to just add one of these to our test data suite, and defer some testing of DCR or wavefront-sensor algorithms until data from ComCam or even the full LSST camera are available.

DRP Summary
-----------

CI, SMALL, MEDIUM, and LARGE datasets exist suitable for significant amount of Science Pipelines performance monitoring.  The addition of a dataset on a crowded field would help exercise a key portion of the Science Pipelines that currently is uncertain.  Technical investigations of (1) using wavefront-sensor data and (2) a system without an ADC may wait until commissioning data is available from ComCam or the full LSSTCam.

=================
AP Test Datasets
=================

Summary recommendations:

1. Use a subset of HiTS for quick turnaround processing, smoke tests, etc.  DONE.
2. Use the DECam Bulge survey for crowded field tests.  IN PROGRESS.
3. Select a subset of HSC SSP PDR1 vs PDR2.  TICKET OPEN.
4. Use a DES Deep SN field for large-scale processing.

Desiderata for AP testing:

  - Tens of epochs per filter per tract in order to construct templates for image differencing and to characterize variability
  - The ability to exercise as many aspects of LSST pipelines and data products as possible
  - Public availability (so that we can feely recruit various LSST stakeholders)
  - Potential for enabling journal publications (both technical and scientific) so that various stakeholders beyond LSST DM may have direct interest in contributing tools and analysis
  - Datasets from at least two different cameras, so that we can isolate effects of LSST pipeline performance from camera-specific details (e.g., ISR, PSF variations) that impact the false-positive rate
  - At least one dataset should be from HSC, to take advantage of Princeton's work on DRP processing
  - At least one dataset should be in multiple filters from a camera without an ADC to test DCR
  - Probably only two cameras should be used for regular detailed processing, to avoid spending undue DM time characterizing non-LSST cameras.  HSC and DECam are the clear choices for this
  - Datasets should include regions of both high and low stellar densities, to understand the impact of crowding on image differencing
  - Ideally, data will be taken over multiple seasons to enable clear separation of templates from the science images
  - Datasets sampling a range of timescales (hours, days, ... years) provide the most complete look at the real transient and variable population
  - Substantial dithering or field overlaps will allow us to test our ability to piece together templates from multiple images (some transient surveys, such as HiTS, PTF, and ZTF, use a strict field grid)
  - There is a balance to be struck between using datasets that have been extensively mined scientifically by the survey teams as opposed to datasets that have not been exploited completely.  If published catalogs of variables, transients, and/or asteroids exist, they will aid in false-positive discrimination and speed QA work.  On the other hand, well-mined datasets may be less motivating to work on, particularly for those outside LSST DM.
  - LSST-like cadences to test Solar System Orbit algorithms

CI
--

DECam HiTS
^^^^^^^^^^

  - A subset of data intended for CI AP testing (with Blind15A_40 and Blind15A_42) is in https://github.com/lsst/ap_verify_ci_hits2015

This subset is only 3 visits and 2 CCDs per visit.

SMALL
-----

DECam HiTS
^^^^^^^^^^

  - Available on lsst-dev in `/datasets/decam/_internal/raw/hits`
  - Total of 2269 visits available
  - up to 14 DECam fields taken over two seasons, and a larger number (40-50) of fields observed only during a single season ; 4-5 epochs per night in one band (g) over a week
  - Essentially only g-band, as there are only a few r-band visits available.  This would not then actually satisfy the 2-band MEDIUM color requirement outlined above.
  - Blind15A_26, Blind15A_40, and Blind15A_42 have been selected for AP testing in https://github.com/lsst/ap_verify_hits2015

MEDIUM
------

HSC SSP PDR1+PDR2
^^^^^^^^^^^^^^^^^

  - Planned work to build templates from PDR1 and then run subtractions from the new data in PDR2 from later years.

    - https://jira.lsstcorp.org/browse/DM-20559
    - https://jira.lsstcorp.org/browse/DM-20560

It's less clear that it's feasible to do active regular testing of DIA on LARGE datasets.  MEDIUM should be sufficient to characterize the key science performance goals.


AP Candidate Additional Datasets
--------------------------------

DECam DES SN fields
^^^^^^^^^^^^^^^^^^^

  - 8 shallow SN fields, 2 deep SN fields
  - griz observation sequences obtained ~ weekly
  - Deep fields have multiple exposures in one field in the same filter each night, with other filters other nights; shallow fields have a single griz sequence in one night.  Former is more LSST-like.
  - Raw data are public
  - 10 fields from 2014 (DES Y2) in field SN-X3.
  - g (no particular reason for this choice)
  - Visits = [371412, 371413, 376667, 376668, 379288, 379289, 379290, 381528, 381529]
  - Available on lsst-dev in `/datasets/des_sn/repo_Y2`

HSC New Horizons
^^^^^^^^^^^^^^^^

  - Crowded stellar field (Galactic Bulge)
  - Available to us (not fully public?); unclear details of numbers of epochs, etc.
  - Scientifically untapped
  - Available on lsst-dev at `/datasets/hsc/raw/newhorizons/`

DECam Bulge survey
^^^^^^^^^^^^^^^^^^

  - Crowded stellar field
  - Propoasal ID 2013A-0719 (PI Saha)
  - Limited publications to date: 2017AJ....154...85V; total boundaries of survey unclear.
  - Published example shows that globular cluster M5 field has 50+ observations over 2+ seasons in each of ugriz

DECam NEO survey
^^^^^^^^^^^^^^^^

  - PI L. Allen
  - 320 square degrees; 5 epochs a night in a single filter with 5 minute cadence, repeating for three nights
  - 3 seasons of data

HSC SSP Deep or Ultra-Deep
^^^^^^^^^^^^^^^^^^^^^^^^^^

  - grizy; exposure times 3-5 minutes; tens of epochs available
  - Two UD fields and 15 deep fields
  - Open Time observations from Yoshida
  - Tens of epochs over a couple of nights for a range of fields
  - GAMA09 and VVDS overlap SSP wide (only) but Yoshida reports the seeing was bad (~1")

Deep DECam Outer Solar System Survey (DDOSSS)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  - P.I. D. Trilling.
  - 13 total nights across 2019A, B semesters.
  - VR=27 mag.  Observations are in several bands.
  - Goal is 5,000 KBOs.
  - https://www.noao.edu/noaoprop/abstract.mpl?2019A-0337
  - Provides a deep dataset and a good source of comparison for deep Solar System object recovery, which is a key interesting science case.

====================================
Datasets considered but not selected
====================================

- CFHT-SNLS

  - Suitable for some AP performance.  But no obvious reason to select CFHT over DECam.

- CFHTLS-Deep

  - Suitable, but no obvious reason to select CFHT over DECam

- PTF

  - Tens to thousands of epochs of public images available in two filters (g & R), but camera characteristics are markedly different–2"+ seeing, 1" pixels, and much shallower.

- ZTF

  - Same sampling issues as PTF.  `obs_ztf` exists, but has not been thoroughly tested.  Not all desired calibration products are presently (2019-10-07) publicly available.

- DLS

  - MOSAIC data.  Was processed through the DM Science Pipelines once (https://dmtn-063.lsst.io/), but there is no supported LSST Science Pipelines module for the camera, so there is no possibility of ongoing analysis.

===========================================
Timescale for preserving processed datasets
===========================================

Preserved outputs are very useful for people testing downstream components without needing to regenerate them as needed. With regular reprocessing of datasets, the volume of data on disk will grow rapidly. It is neither necessary nor feasible to preserve all processed datasets in perpetuity. The following gives the required timescales for retaining processed test datasets:

  - LARGE: A minimum of two datasets should always be preserved as well as two sets of corresponding master calibraions to be used for subsequent processing campaigns. The reason is to be able to compare the results of each subsequent processing campaign. One of the two may be deleted prior to processing the next one if space is needed.
  - MEDIUM: A minimum of 12 months.
  - SMALL: 1 month at the most. Datasets in this category should be managed so that there is always at least one available and so that the likelihood of a dataset being deleted while in use is mitigated. The output from each successive run in this category should be preserved at least until 72 hours after the output of the next run is available.
  - CI: There is no need to preserve any CI datasets.

============
Related Work
============

There is a detailed table of datasets and the elements of https://ls.st/LSE-61 tested by each on the LSST Project Confluence.  The table there aims to cover all aspects of the DM system, not just the Science Pipelines focus on this present tech note:
`Data sets used for DM Verification and Validation <https://confluence.lsstcorp.org/x/nYn4BQ>`_

And here are some thoughts from the perspective of the Commissioning team:
`Design Requirements for Science Verification Analysis Framework <https://confluence.lsstcorp.org/pages/viewpage.action?spaceKey=LSSTCOM&title=Design+Requirements+for+Science+Verification+Analysis+Framework>`_

===============
Practical Notes
===============

Calibration
-----------

Master calibration images will be required prior to processing.  We will not be testing the generation of these master calibration images as part of the processing of these datasets for CI, SMALL, and MEDIUM datasets.  Such generation is suitable for processing with LARGE datasets, but full testing of calibration should be the subject of a separate effort and planning and additional supporting documentation.

Astrometric and photometric reference catalogs will be required for each dataset.

Jenkins vs. NCSA
----------------

The above goals and dataset definitions are written with the NCSA Verification Cluster in mind.
The current Jenkins AWS solution has a much smaller number of available cores than the NCSA Verification Cluster.  These limitations mean that the CI and SMALL datasets are suited to Jenkins.  It would be _possible_ to do occasional MEDIUM runs through Jenkins, but it's likely more efficient to run them at NCSA.

The CI scale of data should also be possible for a developer to manually run on an individual machine, whether that's at their desktop or NCSA.

October, 2019: Jenkins is now running at the LDF in the same configuration of a Kubernetes cluster at the LDF.  Those pods created could have access to the shared datasystem on the LDF.

===========
Future Work
===========

- Specify as-realized datasets on disk based on these recommendations.


.. .. rubric:: References

.. Make in-text citations with: :cite:`bibkey`.

.. .. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
..    :encoding: latex+latin
..    :style: lsst_aa
