class Category:

  def __init__(self, category):
    self.category = category
    self.ledger = []

  def deposit(self, amount, description=""):
    # Add a deposit to the ledger
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=""):
    # Check if there are enough funds and then add a withdrawal to the ledger
    if self.check_funds(amount):
      self.ledger.append({"amount": -amount, "description": description})
      return True
    return False

  def get_balance(self):
    # Calculate the current balance by summing all ledger entries
    sum = 0
    for i in self.ledger:
      sum += i["amount"]
    return sum
    # return sum(item["amount"] for item in self.ledger) ----> another way to write
    #                                                  same code using sum() method

  def transfer(self, amount, budget_category):
    # Check if there are enough funds for the transfer and perform the transfer
    if self.check_funds(amount):
      self.withdraw(amount,
                    f"Transfer to {budget_category.category}")  # calling
      # withdraw() method
      budget_category.deposit(amount,
                              f"Transfer from {self.category}")  # calling
      # deposit() method
      return True
    return False

  def check_funds(self, amount):
    # Check if the requested amount can be withdrawn (not exceeding the balance)
    return amount <= self.get_balance()

  def __str__(self):
    # Generate a formatted string representation of the budget category
    output = self.category.center(30, "*") + "\n"
    for item in self.ledger:
      # Truncate the description to 23 characters and format the amount
      output += item["description"][:23].ljust(23) + "{:.2f}".format(
          item["amount"]).rjust(7) + "\n"
    output += "Total: {:.2f}".format(self.get_balance())

    return output


def create_spend_chart(categories):
  chart = "Percentage spent by category\n"
  # Calculate total spending for each category
  spendings = [
      -sum(item["amount"] for item in category.ledger if item["amount"] < 0)
      for category in categories
  ]
  total_spent = sum(spendings)
  # Calculate the percentage spent for each category
  percentages = [(spending / total_spent) * 100 for spending in spendings]

  # Create the chart rows
  for i in range(100, -1, -10):
    chart += str(i).rjust(3) + "| "
    for percent in percentages:
      if percent >= i:
        chart += "o  "  # Display "o" if the percentage is greater or equal to the current row
      else:
        chart += "   "  # Display spaces otherwise
    chart += "\n"

  chart += "    ----------\n     "
  max_length = max(len(category.category) for category in categories)
  # Create the category labels below the chart
  for i in range(max_length):
    for category in categories:
      if i < len(category.category):
        chart += category.category[i] + "  "
      else:
        chart += "   "  # Add spaces for categories that don't have a label character
    if i < max_length - 1:
      chart += "\n     "

  return chart
