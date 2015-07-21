import csv
import tempfile
import click
from sys import stdout
from collections import defaultdict
import errno


@click.command()
@click.option('--header/--no-header', default=False, help='use when input file contains a header line. Default False.')
@click.option('--key-field-number', default=0, help='Values will be normalized by the sum of values that have this '
              'field in common. Default 0 (first field). Set to -1 to average across all values.')
@click.option('--value-field-number', default=1,
              help='Values will be normalized by the sum of values that have this field in common. '
                   'Default 1 (second field)')
@click.option('--normalize', 'transformation', flag_value='normalize', default=True,
              help='Normalize the values. On by default.')
@click.option('--average', 'transformation', flag_value='average', default=False,
              help='Instead of normalizing, only calculate average')
@click.option('--count', 'transformation', flag_value='count', default=False,
              help='Instead of normalizing, only count occurrences')
@click.argument('input_file', type=click.File('r'))
def normalize_field(input_file, header, key_field_number, value_field_number, transformation):
    """
    Gets csv file as input, and adds another field at the end of every line with the v/sum(v), where v is the value at
    'value-field' and the sum is over all the values with the same key (specified by 'key-field'). """
    sums = defaultdict(int)
    counts = defaultdict(int)
    fp = csv.reader(input_file)

    key_field = int(key_field_number)
    value_field = int(value_field_number)

    if header:
        h = fp.next()

    # I'm going to use a temporary file to save the input stream to, and then reiterate over that file and concatenate
    # the normalized field at the end of each line. I'm using a temp file and not the original input file to support
    # working from stdin (which doesn't support seek operations)

    with tempfile.TemporaryFile() as temp_file:
        writer_tf = csv.writer(temp_file)
        for l in fp:  # iterate over the input csv
            if len(l) < value_field or len(l) < key_field:
                raise ValueError("Bad number of items in line: " + str(l))

            (k, v) = (l[key_field], float(l[value_field]))
            sums[k] += v
            counts[k] += 1
            writer_tf.writerow(l)

        # return to the beginning of the temp file
        temp_file.seek(0)
        reader_tp = csv.reader(temp_file)
        out = csv.writer(stdout)
        if header:
            # print the header line if there is one
            if transformation == 'average':
                h.append("Avg_" + h[value_field])
            elif transformation == 'count':
                h.append("Count_" + h[value_field])
            else:
                h.append("Normalized_" + h[value_field])
            out.writerow(h)
        for l in reader_tp:
            (k, v) = (l[key_field], float(l[value_field]))
            if transformation == 'average':
                l.append(str(sums[k] / counts[k]))
            elif transformation == 'count':
                l.append(str(counts[k]))
            else:
                l.append(str(v / sums[k]))
            out.writerow(l)


if __name__ == "__main__":
    try:
        normalize_field()
    except KeyboardInterrupt:
        pass
    except IOError, e:  # catch closing of pipes
        if e.errno != errno.EPIPE:
            raise e
