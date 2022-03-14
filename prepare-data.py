#!/usr/bin/python3

import random

# If the length of both lines is smaller than this the pair is accepted
SHORT_LINE_ACCEPT_LENGTH = 30
# If the length of either of the lines is larger than this the pair is always rejected
LONG_LINE_REJECT_LENGTH = 512
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

        if len(line_source) > LONG_LINE_REJECT_LENGTH or len(line_destination) > LONG_LINE_REJECT_LENGTH:
            return True

        if len(line_source) / len(line_destination) < SKIP_RATIO:
            return True
        if len(line_destination) / len(line_source) < SKIP_RATIO:
            return True

        return False

    def create_file(self, legend, skip_lines, total_lines, splitted_source, splitted_destination, write_mode):
        f_orig_source = open(self.filename_source, 'r')
        f_orig_destination = open(self.filename_destination, 'r')

        f_splitted_source = open(splitted_source, write_mode)
        f_splitted_destination = open(splitted_destination, write_mode)

        lines_processed = 0
        lines_valid = 0
        lines_invalid = 0
        lines_written = 0

        for source_line in f_orig_source:
            destination_line = f_orig_destination.readline()

            lines_processed += 1

            if self.if_invalid_lines(source_line, destination_line):
                lines_invalid += 1
                continue

            lines_valid += 1

            if lines_valid < skip_lines:
                continue

            if total_lines is None or lines_written < total_lines:
              f_splitted_source.write(source_line)
              f_splitted_destination.write(destination_line)
              lines_written += 1

        f_orig_source.close()
        f_orig_destination.close()

        f_splitted_source.close()
        f_splitted_destination.close()

        print("%s: %d lines (%d processed, %d valid, %d invalid)" % (legend, lines_written, lines_processed, lines_valid, lines_invalid))

def split_dataset(dataset_path, validation_lines, source_validation_file, destination_validation_file):
    print("--- Processing dataset %s" % dataset_path)
    splitter = Splitter('%s/fi.txt' % dataset_path, '%s/sv.txt' % dataset_path)
    splitter.create_file('Training file', validation_lines, None, '%s/src-train.txt' % dataset_path, '%s/tgt-train.txt' % dataset_path, 'w')
    splitter.create_file('Validation file', 0, validation_lines, source_validation_file, destination_validation_file, 'a')

split_dataset('data/finlex', 1000, 'data/src-val.txt', 'data/tgt-val.txt')
split_dataset('data/ccmatrix', 6000, 'data/src-val.txt', 'data/tgt-val.txt')
split_dataset('data/eubookshop', 1800, 'data/src-val.txt', 'data/tgt-val.txt')
split_dataset('data/dgt', 2000, 'data/src-val.txt', 'data/tgt-val.txt')
split_dataset('data/meb-pdf', 200, 'data/src-val.txt', 'data/tgt-val.txt')
