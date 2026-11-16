# my_main.py
# Author: Antonia Xenikis

from my_assistant import StudioHelper
from my_queue import BookingQueue
from my_tool import ClassSchedule
from my_toolbox import StudioToolbox
from ollama_model import OllamaModel

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Nia, a helper for a Pilates studio.
Answer in one short sentence.
Only state facts that appear in these instructions or in tool results.
Use look_up_classes when the client asks which classes are open on a day.
Use request_booking only when the client wants to book and has given their name, the day, and the time.
If the client only says hello, greet them and ask how you can help.
If you do not know, say you do not know and offer to pass the client to the front desk."""

CLASSES = {
    "monday": "6:00 am Reformer and 5:30 pm Mat",
    "wednesday": "9:00 am Reformer",
    "friday": "none",
}

schedule = ClassSchedule(CLASSES)
booking_queue = BookingQueue()
tools = StudioToolbox(schedule, booking_queue)
model = OllamaModel(MODEL_NAME)
helper = StudioHelper("Nia", INSTRUCTIONS, tools, model)

print("Type a message, or type quit to stop.")
user_message = input("You: ")
while user_message != "quit":
    print(f"{helper.name}: {helper.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(helper.history)}")

print("Front desk review")
for request in booking_queue.waiting():
    number = request["number"]
    print(f"Request {number}: {request['name']}, {request['day']} {request['time']}")
    answer = input("Approve? yes or no: ")
    if answer == "yes":
        print(booking_queue.approve(number))
    else:
        print(booking_queue.reject(number))

print(f"Bookings: {len(booking_queue.bookings)}")
