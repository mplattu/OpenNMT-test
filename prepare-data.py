#!/usr/bin/python3

import random

# If the length of both lines is smaller than this the pair is accepted
SHORT_LINE_ACCEPT_LENGTH = 30
# If the ratio between lines is smaller than this the line pair is rejected
SKIP_RATIO = 0.50

class Splitter:
    def __init__ (self, filename_source, filename_destination):
        self.filename_source = filename_source
        self.filename_destination = filename_destination

        source_lines = self.count_lines(self.filename_source)
        destination_lines = self.count_lines(self.filename_destination)

        print("Lines (source file)     : %d" % (source_lines))
        print("Lines (destination file): %d" % (destination_lines))

        if source_lines != destination_lines:
            raise Exception("Source files have different number of lines")

    def count_lines(self, filename):
        with open(filename, 'r') as fp:
            for count, line in enumerate(fp):
                pass
        return count + 1

    def if_invalid_lines(self, line_source, line_destination):
        if len(line_source) < SHORT_LINE_ACCEPT_LENGTH and len(line_destination) < SHORT_LINE_ACCEPT_LENGTH:
            return False

        if len(line_source) / len(line_destination) < SKIP_RATIO:
            return True
        if len(line_destination) / len(line_source) < SKIP_RATIO:
            return True

        return False

    def create_file(self, legend, ratio, splitted_source, splitted_destination, write_mode):
        f_orig_source = open(self.filename_source, 'r')
        f_orig_destination = open(self.filename_destination, 'r')

        f_splitted_source = open(splitted_source, write_mode)
        f_splitted_destination = open(splitted_destination, write_mode)

        lines_processed = 0
        lines_written = 0
        lines_invalid = 0

        for source_line in f_orig_source:
            destination_line = f_orig_destination.readline()

            lines_processed += 1

            lines_invalid = self.if_invalid_lines(source_line, destination_line)

            if lines_invalid:
                lines_invalid += 1
                continue

            rnd = random.random()

            if rnd < ratio:
                f_splitted_source.write(source_line)
                f_splitted_destination.write(destination_line)
                lines_written += 1

        f_orig_source.close()
        f_orig_destination.close()

        f_splitted_source.close()
        f_splitted_destination.close()

        print("%s: %d lines (%d processed, %d invalid)" % (legend, lines_written, lines_processed, lines_invalid))


splitter_finlex = Splitter('data/finlex/fi.txt', 'data/finlex/sv.txt')
splitter_finlex.create_file("Training file", 0.90, 'data/finlex/src-train.txt', 'data/finlex/tgt-train.txt', 'w')
splitter_finlex.create_file("Validation files", 0.0016, 'data/src-val.txt', 'data/tgt-val.txt', 'a')

splitter_ccmatrix = Splitter('data/ccmatrix/fi.txt', 'data/ccmatrix/sv.txt')
splitter_ccmatrix.create_file("Training file", 0.90, 'data/ccmatrix/src-train.txt', 'data/ccmatrix/tgt-train.txt', 'w')
splitter_ccmatrix.create_file("Validation files", 0.0016, 'data/src-val.txt', 'data/tgt-val.txt', 'a')
