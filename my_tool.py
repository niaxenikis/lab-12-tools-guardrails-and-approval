class ClassSchedule:
    """Looks up studio classes by day."""

    def __init__(self, classes):
        self.classes = classes

    def find_day(self, text):
        """Return the day named in the text, or None."""
        lowered = text.lower()
        for day in self.classes:
            if day in lowered:
                return day
        return None

    def classes_for(self, day):
        """Return the classes on a day."""
        return self.classes[day]

    def look_up_classes(self, day):
        """Look up the classes on a day.

        Args:
            day: The day of the week, such as Monday.
        """
        found = self.find_day(day)
        if found is None:
            return "That day was not found. I can check Monday, Wednesday, or Friday."
        return f"Classes on {found}: {self.classes_for(found)}."
