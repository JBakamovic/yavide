import logging
import services.indexer.clang_indexer

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Index given list of files.')
    parser.add_argument('--project_root_directory', required=True, help='a root directory of project to be indexed')
    parser.add_argument('--compiler_args',          required=True, help='list of compiler args to be used while indexing')
    parser.add_argument('--filename_list',          required=True, help='list of filenames to be indexed')
    parser.add_argument('--output_db_filename',     required=True, help='indexing result will be recorded in this file (SQLite db)')
    parser.add_argument('--log_file',                              help='optional log file to log indexing actions')

    args = parser.parse_args()

    if (args.log_file):
        FORMAT = '[%(levelname)s] [%(filename)s:%(lineno)s] %(funcName)25s(): %(message)s'
        logging.basicConfig(filename=args.log_file, filemode='a', format=FORMAT, level=logging.INFO)

    services.indexer.clang_indexer.index_file_list(
        args.project_root_directory,
        args.compiler_args,
        list(str(args.filename_list).split(', ')),
        args.output_db_filename
    )

