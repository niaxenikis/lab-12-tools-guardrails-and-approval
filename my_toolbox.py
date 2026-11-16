# my_toolbox.py
# Author: Antonia Xenikis


class StudioToolbox:
    """Every tool request from the model comes through here and is checked."""

    def __init__(self, schedule, booking_queue):
        """Hold the tools the model is allowed to ask for."""
        self.schedule = schedule
        self.booking_queue = booking_queue

    def tool_list(self):
        """Return the tools the model may ask for. They are not called here."""
        return [
            self.schedule.look_up_classes,
            self.booking_queue.request_booking,
        ]

    def run(self, name, arguments, history):
        """Check one tool request. Run the tool only if every check passes."""
        if name == "look_up_classes":
            day = self.clean(arguments, "day")
            if day == "":
                return "The day is missing. Ask the client which day."
            if not self.client_said(history, day):
                return "The client has not given that day. Ask them for it."
            return self.schedule.look_up_classes(day)
        if name == "request_booking":
            person = self.clean(arguments, "name")
            day = self.clean(arguments, "day")
            time = self.clean(arguments, "time")
            if person == "" or day == "" or time == "":
                return "The name, day, and time are all needed."
            if not self.client_said(history, person):
                return "The client has not given that name. Ask them for it."
            if not self.client_said(history, day):
                return "The client has not given that day. Ask them for it."
            if not self.client_said(history, time):
                return "The client has not given that time. Ask them for it."
            if self.schedule.find_day(day) is None:
                return (
                    "That day was not found. I can check Monday, Wednesday, or Friday."
                )
            return self.booking_queue.request_booking(person, day, time)
        return f"There is no tool named {name}."

    def clean(self, arguments, key):
        """Return one argument as text without extra spaces, or "" if it is missing."""
        return str(arguments.get(key, "")).strip()

    def client_said(self, history, text):
        """Return True if text appears in a message the client typed."""
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False
