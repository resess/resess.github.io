from access.application import Application
from access.applications import ApplicationRepository
from access.data_repository import DataRepository
from access.decompositions import DecompositionRepository
from access.manifest import Manifest
from calculator.data_access import DataAccess
from calculator.dependency_graph import DependencyGraph
from calculator.entropy import EntropyCalculator
from calculator.evolutionary import EvolutionaryRelationshipExtrator
from calculator.evaluate import Evaluator
from calculator.mojofm import MojofmCalculator
from calculator.semantic import SemanticExtractor
from calculator.visualization import VisualizationGenerator
from calculator.statistic import StatisticCalculator
from calculator.structural import StructuralRelationshipExtractor
from cleaning.cargo import CargoCleaner
from cleaning.filter import DecompositionFilter
from cleaning.ground_truth import GroundTruthCleaner
from cleaning.method_level import MethodLevelDecompositionConstructor
from cleaning.mono2micro import Mono2MicroCleaner
from cleaning.mosaic import MosaicCleaner
from utils.utils import Utils

CLEAN_CARGO = False
# Extracts ground truth for applications from {app}_{classes/methods}.csv
CLEAN_GROUND_TRUTH = False
CLEAN_MONO2MICRO = False
CLEAN_MOSAIC = False

CONSTRUCT_METHOD_DECOMPOSITIONS = False

# Copies filtered version of decomposition from {class/method}_decomposition.json
# to filtered_{class/method}_decomposition.json
FILTER_DECOMPOSITIONS = False

EXTRACT_EVOLUTIONARY_RELATIONSHIPS = False
EXTRACT_STRUCTURAL_RELATIONSHIPS = False
EXTRACT_DATA_ACCESS_RELATIONSHIPS = False
EXTRACT_SEMANTIC_RELATIONSHIPS = False
# Extracts ground truth for applications from {app}_{classes/methods}.csv
# into the data/applications/{app}/ground_truth folder
EXTRACT_RSFS = False

GENERATE_VISUALIZATIONS = False
CALCULATE_METRICS = True
CALCULATE_MOJOFM = True
CALCULATE_ENTROPY = True
CALCULATE_PARTITION_STATISTICS = True


if __name__ == "__main__":
    print("Running metric calculator...")

    applications = [
        "spring-petclinic",
        "jpetstore",
        "partsunlimited",
        "demo",
        # "open-mrs"
    ]

    relationships = [
        # "semantic_names",
        "structural_static",
        # "evolutionary_contributors",
        # "evolutionary_commits"
    ]

    data_repository = DataRepository("./data/decompositions")
    decomposition_repository = DecompositionRepository("./data/decompositions")
    application_repository = ApplicationRepository("./data/applications")

    manifest = Manifest(data_repository)
    utils = Utils()

    if CLEAN_CARGO:
        print("Cleaning CARGO data...")
        CargoCleaner(decomposition_repository, manifest, application_repository, utils).clean(applications)

    if CLEAN_MONO2MICRO:
        print("Cleaning Mono2Micro data...")
        Mono2MicroCleaner(decomposition_repository, manifest).clean(applications)

    if CLEAN_MOSAIC:
        print("Cleaning MOSAIC data...")
        MosaicCleaner(decomposition_repository, manifest).clean(applications)

    if CLEAN_GROUND_TRUTH:
        print("Cleaning ground truth data...")
        GroundTruthCleaner(decomposition_repository, manifest, application_repository, utils).clean_new(applications)

    if CONSTRUCT_METHOD_DECOMPOSITIONS:
        print("Constructing method decompositions...")
        MethodLevelDecompositionConstructor(decomposition_repository, manifest, application_repository,
                                            utils).construct_method_decompositions(applications)

    if FILTER_DECOMPOSITIONS:
        print("Filtering decompositions...")
        DecompositionFilter(decomposition_repository, application_repository, utils, manifest).filter_all(applications)

    if EXTRACT_EVOLUTIONARY_RELATIONSHIPS:
        print("Extracting evolutionary relationships...")
        for application in applications:
            EvolutionaryRelationshipExtrator().extract_method_relationships(application, data_repository, application_repository)

    if EXTRACT_STRUCTURAL_RELATIONSHIPS:
        print("Extracting structural relationships...")
        StructuralRelationshipExtractor().extract_relationships(applications, data_repository, application_repository)

    if EXTRACT_DATA_ACCESS_RELATIONSHIPS:
        print("Extracting data access relationships...")
        for application in applications:
            app = Application(application, application_repository)
            print('Method')
            print(DataAccess(app, DependencyGraph(app, data_repository)).get_table_accesses())

    if EXTRACT_SEMANTIC_RELATIONSHIPS:
        print("Extracting semantic relationships...")
        SemanticExtractor(data_repository).calculate_all(applications)

    if EXTRACT_RSFS:
        print("Extracting rsfs...")
        GroundTruthCleaner(decomposition_repository, manifest, application_repository, utils).extract_rsfs(applications)

    if GENERATE_VISUALIZATIONS:
        print("Generating visualizations...")
        VisualizationGenerator(data_repository, manifest, decomposition_repository, application_repository,
                               utils).generate(applications, relationships)

    if CALCULATE_METRICS:
        print("Calculating metrics...")
        Evaluator(data_repository, manifest).calculate_metrics(applications, relationships)

    if CALCULATE_MOJOFM:
        print("Calculating mojofm...")
        MojofmCalculator("./data/applications", decomposition_repository).calculate(manifest)

    if CALCULATE_ENTROPY:
        print("Calculating entropy...")
        EntropyCalculator(application_repository, decomposition_repository,
                          utils, manifest, data_repository).calculate(applications)

    if CALCULATE_PARTITION_STATISTICS:
        print("Calculating partition statistics...")
        StatisticCalculator(data_repository, manifest,
                            decomposition_repository, application_repository, utils).calculate_statistics(applications)
