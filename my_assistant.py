HANDOFF_WORDS = ["cancel", "refund", "payment"]
MAX_TOOL_ROUNDS = 3
HANDOFF_REPLY = (
    "I can't change your booking or handle payments. I'm passing you to the front desk."
)


class StudioHelper:
    """A studio assistant that can use tools, with a limit on how many rounds."""

    def __init__(self, name, instructions, tools, model):
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        if self.needs_front_desk(user_message):
            return HANDOFF_REPLY
        return self.model_reply()

    def needs_front_desk(self, user_message):
        lowered = user_message.lower()
        for word in HANDOFF_WORDS:
            if word in lowered:
                return True
        return False

    def model_reply(self):
        """Ask the model. Run each tool it asks for, then ask again, up to a limit."""
        for _ in range(MAX_TOOL_ROUNDS):
            tool_list = self.tools.tool_list()
            decision = self.model.decide(self.instructions, self.history, tool_list)
            if decision is None:
                return "Sorry, I can't answer that right now. Please try again in a moment."
            if "text" in decision:
                return decision["text"]
            name = decision["tool"]
            arguments = decision["arguments"]
            result = self.tools.run(name, arguments, self.history)
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
        return "Sorry, I couldn't finish that. I'm passing you to the front desk."

    def count_user_messages(self):
        count = 0
        for entry in self.history:
            if entry["role"] == "user":
                count += 1
        return count
