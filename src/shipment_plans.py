from typing import List, Tuple, Dict

from src.suitability_score import SuitabilityScoreCalculator

class Shipment(object):
    def __init__(
            self,
            driver: str,
            shipment_destination: str,
            suitability_score: float):
        self.driver = driver
        self.destination = shipment_destination
        self.suitability_score = suitability_score

    @staticmethod
    def create(
            driver: str,
            shipment_destination: str,
            suitability_score_calculator: SuitabilityScoreCalculator):
        return Shipment(
            driver,
            shipment_destination,
            suitability_score_calculator.calculate_suitability_score(
                driver, shipment_destination))

class ShipmentPlan(object):
    def __init__(
            self,
            shipments: List[Shipment]=None,
            total_suitability_score: float=0):
        # I have a broad philosophy of not letting constructors do real work
        # for allowing mocking, serialization, etc., so create() does the
        # actual heavy lifting of making sure that shipments and
        # total_suitability_score match up
        if shipments is None:
            shipments = []
        self._shipments = shipments
        self._total_suitability_score = total_suitability_score

    def copy(self):
        return ShipmentPlan(
            self._shipments.copy(),
            self._total_suitability_score)

    @staticmethod
    def create(shipments: List[Shipment]=None):
        if shipments is None:
            shipments = []
        return ShipmentPlan(
            shipments,
            sum([shipment.suitability_score for shipment in shipments]))

    @property
    def total_suitability_score(self):
        return self._total_suitability_score

    def add_shipment(self, shipment: Shipment):
        self._shipments.append(shipment)
        self._total_suitability_score =\
            self._total_suitability_score + shipment.suitability_score

class ShipmentPlanCalculator(object):
    def __init__(
            self,
            suitability_score_calculator: SuitabilityScoreCalculator=None,
            shipment_plan_memoizations:
                Dict[Tuple[Tuple[str], Tuple[str]], ShipmentPlan]=None):
        if suitability_score_calculator is None:
            suitability_score_calculator = SuitabilityScoreCalculator()
        self._suitability_score_calculator = suitability_score_calculator
        if shipment_plan_memoizations is None:
            shipment_plan_memoizations = {}
        # Dictionary of
        # key:
        #   Tuple of:
        #       (tuple of drivers, tuple of shipment_destinations)
        # value:
        #   shipment plan
        self._shipment_plan_memoizations = shipment_plan_memoizations

    # This will only be called once per cycle with a given driver so does
    # not need to be memoized
    def _calculate_highest_score_shipment_with_fixed_driver(
            self,
            driver: str,
            shipment_destinations: List[str]) \
            -> Shipment:
        idx_for_highest_score = None
        highest_score_shipment = Shipment('', '', -1)
        for shipment_destination_idx in range(len(shipment_destinations)):
            shipment = Shipment.create(
                driver,
                shipment_destinations[shipment_destination_idx],
                self._suitability_score_calculator)
            # It's arbitrary whether to take the first or the last highest
            # matching score, but here we're taking the first matching
            if shipment.suitability_score > \
                    highest_score_shipment.suitability_score:
                idx_for_highest_score = shipment_destination_idx
                highest_score_shipment = shipment
        if idx_for_highest_score is not None:
            return highest_score_shipment
        else:
            return None, None

    # This uses tuples instead of lists since tuples are hashable
    def generate_optimal_shipment_plan(
            self,
            drivers: Tuple[str],
            shipment_destinations: Tuple[str]) \
            -> ShipmentPlan:
        key = (drivers, shipment_destinations)
        if key in self._shipment_plan_memoizations:
            return self._shipment_plan_memoizations[key]

        if len(drivers) == 0:
            to_return = ShipmentPlan([])
        elif len(drivers) == 1:
            highest_score_shipment \
                = self._calculate_highest_score_shipment_with_fixed_driver(
                    drivers[0],
                    shipment_destinations)
            to_return = ShipmentPlan.create([highest_score_shipment])
        else:
            # Pick a driver and generate all possible destinations for that
            # driver
            highest_score_shipment_plan = ShipmentPlan()
            for shipment_destination_idx in range(len(shipment_destinations)):
                shipment = Shipment.create(
                    drivers[0],
                    shipment_destinations[shipment_destination_idx],
                    self._suitability_score_calculator)
                # noinspection PyTypeChecker
                # This is erroneously being evaluated as Tuple[Any]
                optimal_sub_shipment_plan = \
                    self.generate_optimal_shipment_plan(
                        drivers[1:],
                        shipment_destinations[:shipment_destination_idx]
                        + shipment_destinations[
                          (shipment_destination_idx + 1):]
                    ).copy()
                optimal_sub_shipment_plan.add_shipment(shipment)
                if optimal_sub_shipment_plan.total_suitability_score >= \
                        highest_score_shipment_plan.total_suitability_score:
                    highest_score_shipment_plan = optimal_sub_shipment_plan

            to_return = highest_score_shipment_plan

        self._shipment_plan_memoizations[key] \
            = to_return

        return to_return

def generate_optimal_shipment_plan(
            drivers: List[str],
            shipment_destinations: List[str],
            shipment_plan_calculator: ShipmentPlanCalculator=None)\
        -> ShipmentPlan:
    if shipment_plan_calculator is None:
        shipment_plan_calculator = ShipmentPlanCalculator()
    return shipment_plan_calculator.generate_optimal_shipment_plan(
        tuple(drivers),
        tuple(shipment_destinations))
