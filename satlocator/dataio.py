# -*- coding: utf-8 -*-

""" Backend defines behaviour.
    No specific implementation should be used in this module.
    Calls to this module should be backend agnostic.
"""

from dataio_backend_finder import dataio_backend


def set_observer(observer):
    """ Defines a new observer.
    """
    result = dataio_backend.set_observer(observer)
    return result


def get_observer(observer_name):
    """ Retrieves an observer by name.
    """
    result = dataio_backend.get_observer(observer_name)
    return result


def del_observer(observer_name):
    """ Removes an observer by name.
    """
    result = dataio_backend.del_observer(observer_name)
    return result


def get_observer_list():
    """ Retrieves all observers.
    """
    result = dataio_backend.get_observer_list()
    return result


def set_satellite(satellite):
    """ Defines a new satellite.
    """
    result = dataio_backend.set_satellite(satellite)
    return result


def get_satellite(satellite_name):
    """ Retrieves a satellite.
    """
    result = dataio_backend.get_satellite(satellite_name)
    return result


def del_satellite(satellite_name):
    """ Removes a satellite.
    """
    result = dataio_backend.del_satellite(satellite_name)
    return result


def get_satellite_list():
    """ Retrieves all satellites.
    """
    result = dataio_backend.get_satellite_list()
    return result


def set_schedule_slot(slot):
    """ Reserves a schedule slot.
    """
    result = dataio_backend.set_schedule_slot(slot)
    return result


def del_schedule_slot(slot):
    """ Deletes a schedule reservation.
    """
    result = dataio_backend.del_schedule_slot(slot)
    return result


def check_schedule_slot_availability(slot):
    """ Checks whether a schedule slot is available for reservation.
    """
    result = dataio_backend.check_schedule_slot_availability(slot)
    return result


def get_schedule_list():
    """ Retrieves schedule.
    """
    result = dataio_backend.get_schedule_list()
    return result


def get_next_schedule_slot():
    """ Retrieves nearest reservation.
    """
    result = dataio_backend.get_next_schedule_slot()
    return result


def set_current_observer(observer):
    """ Defines current observer.
    """
    result = dataio_backend.set_current_observer(observer)
    return result


def get_current_observer():
    """ Retrieves current observer.
    """
    result = dataio_backend.get_current_observer()
    return result


def set_current_satellite(satellite):
    """ Defines current satellite.
    """
    result = dataio_backend.set_current_satellite(satellite)
    return result


def get_current_satellite():
    """ Retrieves current satellite.
    """
    result = dataio_backend.get_current_satellite()
    return result
