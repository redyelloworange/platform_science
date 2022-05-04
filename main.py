#! /usr/bin/python3.9

import argparse
import os

from src.file_parser import parse_newline_separated_file
from src.shipment_plans import generate_optimal_shipment_plan

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--driver-file',
        help='A newline-separated list of drivers',
        required=True)
    parser.add_argument(
        '--shipment-destination-file',
        help='A newline-separated list of shipment destinations',
        required=True)
    parser.add_argument(
        '--show-suitability-score',
        help='Show the suitability score of each shipment',
        action='store_true'
    )
    args = parser.parse_args()

    drivers = parse_newline_separated_file(args.driver_file)
    shipment_destinations = parse_newline_separated_file(
        args.shipment_destination_file)
    optimal_shipment_plan = generate_optimal_shipment_plan(
        drivers,
        shipment_destinations)
    if len(optimal_shipment_plan._shipments) > 0:
        for shipment\
                in sorted(
                    optimal_shipment_plan._shipments,
                    key=lambda s: s.driver):
            print(
                f'{shipment.driver}, {shipment.destination}'
                + (f' ({shipment.suitability_score})'
                  if args.show_suitability_score else ''))
        print('=' * os.get_terminal_size().columns)

    print(
        'Total suitability score: '
        f'{optimal_shipment_plan.total_suitability_score}')