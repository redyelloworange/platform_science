import itertools
from unittest import TestCase

from shipment_plans import Shipment, ShipmentPlan, ShipmentPlanCalculator
from suitability_score import SuitabilityScoreCalculator


class TestShipment(TestCase):
    def setUp(self) -> None:
        self._suitability_score_calculator = SuitabilityScoreCalculator()

    def test_create(self):
        driver_name = 'Bart Simpson'
        shipment_destination = '123456789'
        shipment = Shipment.create(
            driver_name,
            shipment_destination,
            self._suitability_score_calculator)
        self.assertEqual(
            shipment.driver,
            driver_name)
        self.assertEqual(
            shipment.destination,
            shipment_destination)
        self.assertEqual(
            20.25,
            shipment.suitability_score)


class TestShipmentPlan(TestCase):
    def test_create_empty(self):
        shipment_plan = ShipmentPlan.create()
        self.assertEqual(
            0,
            shipment_plan.total_suitability_score)

    def test_create_populated(self):
        shipment_plan = ShipmentPlan.create([
            Shipment('Bart Barclay', '1234567890', 6.75)
        ])
        self.assertEqual(
            6.75,
            shipment_plan.total_suitability_score)

    def test_add_shipment(self):
        shipment_plan = ShipmentPlan.create()
        shipment_plan.add_shipment(
            Shipment(
                'Lisa Simpson',
                '1234567890A',
                20.25))
        self.assertEqual(
            20.25,
            shipment_plan.total_suitability_score)


class TestShipmentPlanCalculator(TestCase):
    def setUp(self) -> None:
        self._shipment_plan_calculator = ShipmentPlanCalculator()

    def test_calculate_highest_score_idx_with_fixed_value(self):
        shipment = \
            self\
                ._shipment_plan_calculator\
                ._calculate_highest_score_shipment_with_fixed_driver(
                    'Lisa Darville',
                    [
                        '0123456789AB',
                        '0123456789ABCD',
                        '0123456789ABCDEF'
                    ]
                )
        self.assertEqual(
            7.5,
            shipment.suitability_score)

    def test_generate_optimal_shipment_plans(self):
        drivers = (
            'Homer Simpson',
            'Red Barclay',
            'Bo Darville',
            'Cledus Snow'
        )
        destinations = (
            '742 Evergreen Terrace',
            '221B Baker Street',
            '17 Cherry Tree Lane',
            '350 Fifth Avenue',
            '4 Privet Drive'
        )
        optimal_shipment_plan = \
            self._shipment_plan_calculator.generate_optimal_shipment_plan(
                drivers,
                destinations
            )

        # All of these destinations sum to 43.5, so any one is a valid solution
        valid_combinations = [
            set([('Homer Simpson', '742 Evergreen Terrace'),
                 ('Red Barclay', '221B Baker Street'),
                 ('Bo Darville', '350 Fifth Avenue'),
                 ('Cledus Snow', '17 Cherry Tree Lane')]),
            set([('Homer Simpson', '742 Evergreen Terrace'),
                 ('Red Barclay', '221B Baker Street'),
                 ('Bo Darville', '4 Privet Drive'),
                 ('Cledus Snow', '17 Cherry Tree Lane')]),
            set([('Homer Simpson', '742 Evergreen Terrace'),
                 ('Red Barclay', '17 Cherry Tree Lane'),
                 ('Bo Darville', '350 Fifth Avenue'),
                 ('Cledus Snow', '221B Baker Street')]),
            set([('Homer Simpson', '742 Evergreen Terrace'),
                 ('Red Barclay', '17 Cherry Tree Lane'),
                 ('Bo Darville', '4 Privet Drive'),
                 ('Cledus Snow', '221B Baker Street')]),
            set([('Homer Simpson', '221B Baker Street'),
                 ('Red Barclay', '742 Evergreen Terrace'),
                 ('Bo Darville', '350 Fifth Avenue'),
                 ('Cledus Snow', '17 Cherry Tree Lane')]),
            set([('Homer Simpson', '221B Baker Street'),
                 ('Red Barclay', '742 Evergreen Terrace'),
                 ('Bo Darville', '4 Privet Drive'),
                 ('Cledus Snow', '17 Cherry Tree Lane')]),
            set([('Homer Simpson', '221B Baker Street'),
                 ('Red Barclay', '17 Cherry Tree Lane'),
                 ('Bo Darville', '350 Fifth Avenue'),
                 ('Cledus Snow', '742 Evergreen Terrace')]),
            set([('Homer Simpson', '221B Baker Street'),
                 ('Red Barclay', '17 Cherry Tree Lane'),
                 ('Bo Darville', '4 Privet Drive'),
                 ('Cledus Snow', '742 Evergreen Terrace')]),
            set([('Homer Simpson', '17 Cherry Tree Lane'),
                 ('Red Barclay', '742 Evergreen Terrace'),
                 ('Bo Darville', '350 Fifth Avenue'),
                 ('Cledus Snow', '221B Baker Street')]),
            set([('Homer Simpson', '17 Cherry Tree Lane'),
                 ('Red Barclay', '742 Evergreen Terrace'),
                 ('Bo Darville', '4 Privet Drive'),
                 ('Cledus Snow', '221B Baker Street')]),
            set([('Homer Simpson', '17 Cherry Tree Lane'),
                 ('Red Barclay', '221B Baker Street'),
                 ('Bo Darville', '350 Fifth Avenue'),
                 ('Cledus Snow', '742 Evergreen Terrace')]),
            set([('Homer Simpson', '17 Cherry Tree Lane'),
                 ('Red Barclay', '221B Baker Street'),
                 ('Bo Darville', '4 Privet Drive'),
                 ('Cledus Snow', '742 Evergreen Terrace')])
        ]
        self.assertEqual(
            43.5,
            optimal_shipment_plan.total_suitability_score)
        self.assertIn(
            set([
                (shipment.driver, shipment.destination)
                for shipment
                in optimal_shipment_plan._shipments]),
            valid_combinations
        )
