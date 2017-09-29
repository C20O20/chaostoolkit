# -*- coding: utf-8 -*-
import os.path

from jsonschema import ValidationError
import pytest

from chaostoolkit.layers import load_layers
from chaostoolkit.plan import apply_action, apply_steady_probe, \
    apply_close_probe, execute_plan, load_plan
from chaostoolkit.errors import FailedProbe, InvalidPlan, UnknownAction,\
    UnknownProbe

layers = load_layers({"platforms": [{"key": "noop"}]})


def test_plan_that_do_not_exist_cannot_be_loaded():
    with pytest.raises(IOError) as excinfo:
        load_plan("wherever.json")


#def test_invalid_plan_should_be_reported():
#    with pytest.raises(ValidationError) as excinfo:
#        load_plan(
#            os.path.join(os.path.dirname(__file__), "fixtures",
#                         "invalid-plan.json"))


def test_valid_plan_should_be_loaded():
    plan = load_plan(
        os.path.join(os.path.dirname(__file__), "fixtures",
                     "kill-restart-microservice.json"))
    assert plan is not None


def test_plan_needs_a_method():
    with pytest.raises(InvalidPlan) as excinfo:
        execute_plan({}, layers)

    assert "a plan must have a method defined" in str(excinfo)


def test_plan_may_have_no_steps():
    assert execute_plan({"method": []}, layers) is None


def test_a_step_without_action_is_silent():
    step = {}
    assert apply_action(step, layers) is None


def test_action_needs_a_name():
    step = {
        "action": {
            "parameters": {
                "name": "cherrypy-webapp"
            }
        }
    }

    with pytest.raises(InvalidPlan) as excinfo:
        apply_action(step, layers)

    assert "action requires a name" in str(excinfo)


def test_action_must_be_implemented():
    step = {
        "action": {
            "layer": "noop",
            "name": "microservice-goes-boom",
            "parameters": {
                "name": "cherrypy-webapp"
            }
        }
    }

    with pytest.raises(UnknownAction) as excinfo:
        apply_action(step, layers)

    assert "action 'microservice_goes_boom' is not implemented" in str(excinfo)


def test_a_step_without_steady_probe_is_silent():
    step = {}
    assert apply_steady_probe(step, layers) is None


def test_steady_probe_needs_a_name():
    step = {
        "probes": {
            "steady": {
            }
        }
    }

    with pytest.raises(InvalidPlan) as excinfo:
        apply_steady_probe(step, layers)

    assert "steady probe requires a probe name to apply" in str(excinfo)


def test_steady_probe_must_be_implemented():
    step = {
        "probes": {
            "steady": {
                "layer": "noop",
                "name": "microservice-should-be-happy"
            }
        }
    }

    with pytest.raises(UnknownProbe) as excinfo:
        apply_steady_probe(step, layers)

    assert "probe 'microservice_should_be_happy' is not implemented" in\
        str(excinfo)


def test_a_step_without_close_probe_is_silent():
    step = {}
    assert apply_close_probe(step, layers) is None


def test_close_probe_needs_a_name():
    step = {
        "probes": {
            "close": {
            }
        }
    }

    with pytest.raises(InvalidPlan) as excinfo:
        apply_close_probe(step, layers)

    assert "close probe requires a probe name to apply" in str(excinfo)


def test_close_probe_must_be_implemented():
    step = {
        "probes": {
            "close": {
                "layer": "noop",
                "name": "microservice-should-be-happy"
            }
        }
    }

    with pytest.raises(UnknownProbe) as excinfo:
        apply_close_probe(step, layers)

    assert "probe 'microservice_should_be_happy' is not implemented" in\
        str(excinfo)
