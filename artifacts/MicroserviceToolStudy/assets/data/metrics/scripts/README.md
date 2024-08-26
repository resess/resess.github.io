# Metrics Calculation

The entrypoint for all scripts in this directory is `main.py`. 
This `main.py` file contains a collection of boolean constants that can be set to `True` to run various portions of the scripts.
Specifically, the following constants are available:

### Setup
Clone all four case study repositories into the `casestudies` folder
```
cd casestudies 
https://github.com/SarahBornais/jpetstore-6
https://github.com/SarahBornais/spring-petclinic
https://github.com/SarahBornais/PartsUnlimitedMRP
git clone https://github.com/SarahBornais/demo
```

### Data Cleaning Scripts

Setting each of these constants to `True` will facilitate the cleaning of decompositions from different sources.
We did not receive data in the necessary format for these decompositions (cargo, ground truth, mono2micro, and mosaic),
so they must be converted to our format before we can run the rest of the scripts.

- CLEAN_CARGO
- CLEAN_GROUND_TRUTH
- CLEAN_MONO2MICRO
- CLEAN_MOSAIC

### Decomposition Transformation Scripts

- CONSTRUCT_METHOD_DECOMPOSITIONS: constructs an equivalent method-level decomposition for each of the class-level decompositions to facilitate comparison to other method-level decompositions
- FILTER_DECOMPOSITIONS: filters decompositions to only include entities that exist in the monolithic version of the application that we are considering (some decompositions also included additional files, such as test classes, in their decomposition)

### Relationship Extraction Scripts

- EXTRACT_EVOLUTIONARY_RELATIONSHIPS: extracts commit/contributor graphs for the case study applications
- EXTRACT_STRUCTURAL_RELATIONSHIPS: extracts method call/inheritance graphs for the case study applications
- EXTRACT_DATA_ACCESS_RELATIONSHIPS: extracts all database accesses in the case study applications
- EXTRACT_SEMANTIC_RELATIONSHIPS: extracts class name-similarity graphs for the case study applications
- EXTRACT_RSFS: extracts ground truth for applications

### Metrics and Visualization Scripts

- GENERATE_VISUALIZATIONS: constructs visualizations of each of the decompositions
- CALCULATE_METRICS: calculates TurboMQ-based metrics
- CALCULATE_MOJOFM: calculates similarity to ground truth metrics (MoJoFM and c2c)
- CALCULATE_ENTROPY: calculates entropy-based metrics
- CALCULATE_PARTITION_STATISTICS: calculates statistical information about the decomposition (partition size distribution and number of observed entities)