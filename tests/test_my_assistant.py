# tests/test_my_assistant.py
#  Author: Antonia Xenikis
from fake_model import FakeModel
from my_assistant import StudioHelper
from my_queue import BookingQueue
from my_tool import ClassSchedule
from my_toolbox import StudioToolbox


class SilentModel:
    """A model that never has an answer. It stands in for Ollama being switched off."""

    def decide(self, instructions, history, tools):
        return None


def make_helper(model):
    """Build a fresh helper with its own tools and the model it is given."""
    schedule = ClassSchedule(
        {
            "monday": "6:00 am Reformer and 5:30 pm Mat",
            "wednesday": "9:00 am Reformer",
            "friday": "none",
        }
    )
    tools = StudioToolbox(schedule, BookingQueue())
    return StudioHelper("Nia", "Be brief.", tools, model)


def ask_for_tool(name, arguments):
    """Build the decision a model returns when it wants a tool."""
    return {"tool": name, "arguments": arguments}


def test_model_can_look_up_classes():
    model = FakeModel(
        [ask_for_tool("look_up_classes", {"day": "monday"}), {"text": "Done."}]
    )
    helper = make_helper(model)
    helper.respond("What is open on Monday?")
    assert helper.history[1]["content"] == (
        "Classes on monday: 6:00 am Reformer and 5:30 pm Mat."
    )


def test_made_up_name_is_refused():
    model = FakeModel(
        [
            ask_for_tool(
                "request_booking",
                {"name": "Dana Cruz", "day": "Monday", "time": "6:00 am"},
            ),
            {"text": "What is your name?"},
        ]
    )
    helper = make_helper(model)
    helper.respond("Please book Monday at 6:00 am")
    assert "has not given that name" in helper.history[1]["content"]
    assert helper.tools.booking_queue.waiting() == []


def test_booking_request_waits_for_the_front_desk():
    model = FakeModel(
        [
            ask_for_tool(
                "request_booking",
                {"name": "Dana Cruz", "day": "Monday", "time": "6:00 am"},
            ),
            {"text": "Sent to the front desk."},
        ]
    )
    helper = make_helper(model)
    helper.respond("I am Dana Cruz. Please book Monday at 6:00 am")
    queue = helper.tools.booking_queue
    assert len(queue.waiting()) == 1
    assert queue.bookings == []


def test_cancel_request_goes_to_the_front_desk():
    helper = make_helper(FakeModel([]))
    assert "front desk" in helper.respond("Please cancel my class")


def test_safe_reply_when_the_model_has_no_answer():
    helper = make_helper(SilentModel())
    assert "try again" in helper.respond("hello")


def test_unknown_tool_is_refused():
    model = FakeModel(
        [ask_for_tool("delete_class", {"day": "monday"}), {"text": "Sorry."}]
    )
    helper = make_helper(model)
    helper.respond("Delete Monday")
    assert helper.history[1]["content"] == "There is no tool named delete_class."


def test_approve_books_once():
    model = FakeModel(
        [
            ask_for_tool(
                "request_booking",
                {"name": "Dana Cruz", "day": "Monday", "time": "6:00 am"},
            ),
            {"text": "Sent."},
        ]
    )
    helper = make_helper(model)
    helper.respond("I am Dana Cruz. Please book Monday at 6:00 am")
    queue = helper.tools.booking_queue
    queue.approve(1)
    queue.approve(1)
    assert len(queue.bookings) == 1
