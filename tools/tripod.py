import library.files
import library.logging
import library.tripod

import os


def getTripodReports():
    results = library.files.load_yaml_data('tripod.yaml')
    for className, personsResults in results.items():
        report = library.tripod.getEmptyReport(className)
        for personResult in personsResults:
            personResult = personResult.replace(' ', '').replace('-', '3').replace('_', '3')
            assert len(personResult) == 35
            for index, answer in enumerate(personResult, 1):
                report.AddAnswer(index, int(answer))
        yield className, report


def run(args):
    fileWriter = library.files.FileWriter()
    tripodFormat = args.format
    getText, extension = {
        'tex': (lambda r: r.GetTex(), 'tex'),
        'txt': (lambda r: r.GetText(), 'txt'),
    }[tripodFormat]
    for className, report in getTripodReports():
        fileWriter.Write(os.path.join('school-554', 'tripod'), className + '-tripod.%s' % extension, text=getText(report))


def populate_parser(parser):
    parser.add_argument('-f', '--format', help='Format', choices=['tex', 'txt'], required=True)
    parser.set_defaults(func=run)
