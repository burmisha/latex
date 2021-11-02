import library.files
import library.location
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
    tripod_format = args.format

    for className, report in getTripodReports():
        filename = library.location.root('school-554', 'tripod', f'{className}-tripod.{tripod_format}')

        if tripod_format == 'tex':
            text = report.GetTex()
        elif tripod_format == 'txt':
            text = report.GetText()
        else:
            raise RuntimeError(f'Invalid tripod format: {tripod_format}')

        fileWriter.Write(filename, text=text)


def populate_parser(parser):
    parser.add_argument('-f', '--format', help='Format', choices=['tex', 'txt'], required=True)
    parser.set_defaults(func=run)
