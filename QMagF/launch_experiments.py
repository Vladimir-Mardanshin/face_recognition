import click

from experiments import single_image_benchmarks, runtime_analysis, robustness_analysis, ijb_benchmarks, memory_analysis


@click.command()
@click.option('--train_db', default=None, type=click.Choice(['colorferet', 'adience', 'morph']), help='The dataset which is used for finding alpha and beta.')
@click.option('--alpha', default=None, type=float, help='The Alpha parameter of our method.')
@click.option('--beta', default=None, type=float, help='The Beta Parameter of our method.')
@click.option('-r', '--dataset_root', default='_data/single_images/magface100', type=click.Path(exists=True), help='The directory where the mainEmbeddings and filenames files are saved.')
@click.option('-p', '--pairs_root', default='_data/pairs', type=click.Path(exists=True), help='The directory where all pairs.txt files are saved.')
@click.option('-t', '--test_db', type=click.Choice(['agedb', 'calfw', 'cfp', 'cplfw', 'lfw', 'xqlfw']), multiple=True, help='The datasets to evaluate.')
@click.option('--ijb_target', type=click.Choice(['IJBC', 'IJBB']), default='IJBC', help='Which IJB dataset to use.')
@click.option('--experiment', type=click.Choice(['single_image', 'runtime', 'robustness', 'ijb', 'memory']), help='Which experiment to run.')
def main(train_db, alpha, beta, dataset_root, pairs_root, test_db, ijb_target, experiment):
    if experiment == 'single_image':
        single_image_benchmarks.main(train_db, alpha, beta, dataset_root, pairs_root, test_db)
    elif experiment == 'runtime':
        runtime_analysis.main(train_db, dataset_root)
    elif experiment == 'robustness':
        robustness_analysis.main('_results/robustness_analysis.csv',
                                 ['_data/single_images/magface18', '_data/single_images/magface50',
                                  '_data/single_images/magface100'], ['lfw', 'morph', 'colorferet'])
    elif experiment == 'ijb':
        ijb_benchmarks.main('_data/ijb/', '_results/ijb/', ijb_target)
    elif experiment == 'memory':
        memory_analysis.main(train_db, dataset_root)


if __name__ == '__main__':
    main()
