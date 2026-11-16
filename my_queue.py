# my_queue.py
# Author: Antonia Xenikis


class BookingQueue:
    """Bookings waiting for the studio to approve. Nothing is booked until they do."""

    def __init__(self):
        """Start with no requests and no bookings."""
        self.requests = []
        self.bookings = []

    def request_booking(self, name, day, time):
        """Ask the studio to book a class for one person. The studio must approve it.

        Args:
            name: The person's full name.
            day: The day of the class, like monday.
            time: The time of the class, like 9:00 am.
        """
        number = len(self.requests) + 1
        request = {
            "number": number,
            "name": name,
            "day": day.lower(),
            "time": time,
            "status": "waiting",
        }
        self.requests.append(request)
        return f"Request {number} was sent to the studio. You are not booked yet."

    def waiting(self):
        """Return the requests that are still waiting for a decision."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Return the request with this number, or None."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve one waiting request and make the booking."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        self.bookings.append(request)
        return f"Request {number} approved."

    def reject(self, number):
        """Reject one waiting request. Nothing is booked."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} rejected."
