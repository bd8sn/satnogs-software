# -*- coding: utf-8 -*-

""" Implements all functions defined in dataio.py.
    Contains all logic required to implement defined functionality.
"""


def set_observer(observer):
    """ Defines a new observer.
    """
    pass


def get_observer(observer_name):
    """ Retrieves an observer by name.
    """
    pass


def get_observer_list():
    """ Retrieves all observers.
    """
    pass


def set_satellite(satellite):
    """ Defines a new satellite.
    """
    pass


def get_satellite(satellite_name):
    """ Retrieves a satellite.
    """
    pass


def get_satellite_list():
    """ Retrieves all satellites.
    """
    pass


def set_schedule_slot(slot):
    """ Reserves a schedule slot.
    """
    pass


def del_schedule_slot(slot):
    """ Deletes a schedule reservation.
    """
    pass


# does this function move (too much) logic into the db?
def check_schedule_slot_availability(slot):
    """ Checks whether a schedule slot is available for reservation.
    """
    pass


def get_schedule_list():
    """ Retrieves schedule.
    """
    pass


def get_next_schedule_slot():
    """ Retrieves nearest reservation.
    """
    pass