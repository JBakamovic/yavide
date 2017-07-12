import logging
import services.indexer.clang_indexer

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Index given list of files.')
    parser.add_argument('--project_root_directory', required=True, help='a root directory of project to be indexed')
    parser.add_argument('--input_list',             required=True, help='input file containing all source filenames to be indexed (one filename per each line)')
    parser.add_argument('--output_db_filename',     required=True, help='indexing result will be recorded in this file (SQLite db)')
    parser.add_argument('--log_file',               required=True, help='log file to log indexing actions')

    args = parser.parse_args()

    if (args.log_file):
        FORMAT = '[%(levelname)s] [%(filename)s:%(lineno)s] %(funcName)25s(): %(message)s'
        logging.basicConfig(filename=args.log_file, filemode='w', format=FORMAT, level=logging.INFO)

    services.indexer.clang_indexer.index_file_list(
        args.project_root_directory,
        args.input_list,
        args.output_db_filename
    )

