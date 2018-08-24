import sys
import time
import glob
import os
import Extractor as extractor
import ConfigPaths as config
import CrossReference as crossref
import TextWriter as text_writer
from DatabaseFunctionalityModules.DatabaseConnection import add_data
from DatabaseFunctionalityModules.ID_Fixer import fix_pub_and_author_id
from Authors import build_author_list

input_dir = os.path.abspath('../inputs/') + '/'
output_dir = os.path.abspath('../outputs/') + '/'
pdffigures2_dir = config.pdffigures2_dir
thread_count = config.thread_count


if __name__ == '__main__':

    init_start = time.time()

    is_ready_to_run = extractor.check_resources()

    if is_ready_to_run:
        # remove spaces from names of PDF's since spaces causes pdffigures2 to skip pdf
        # os.chdir(input_dir)
        # for file in glob.glob("*.pdf"):
        #     extractor.remove_space(file)
        #
        # print("GROBID extracting text, metadata and references")
        # try:
        #     extractor.data_extractor(input_dir, output_dir)
        # except Exception as e:
        #     print(e)
        #     sys.exit("GROBID encountered an error")
        #
        # print("PDFFigures2.0 extracting figures and figure captions")
        #
        # try:
        #     extractor.extract_figures(input_dir, output_dir, pdffigures2_dir, thread_count)
        # except Exception as e:
        #     print(e)
        #     sys.exit("PDFFigures encountered an error")

        print("Parsing XML and JSON Files")
        try:
            devices = extractor.parse_output_files(output_dir)
        except Exception as e:
            print(e)
            sys.exit("Parser encountered an error")

        connections = {}
        authors = []
        if config.should_init_crossrefs:
            start = time.time()
            connections = crossref.initialize_connections(devices)
            finish = time.time()
            print("Initialized Connections in %f seconds" % (finish - start))
        if config.add_to_db:
            authors = build_author_list(devices)
            add_data(devices, connections, authors)
            fix_pub_and_author_id()
        if config.writeToFile:
            start = time.time()
            text_writer.writeFiles(devices, connections, authors)
            finish = time.time()
            print("Wrote Files in %f seconds" % (finish - start))

        extractor.clean_output_folder(output_dir)
    finish = time.time()
    print("---------- Total Time Taken: %f ---------------------" % (finish - init_start))
