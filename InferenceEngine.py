import sys
import itertools

# First step is to extract data from the file in similar way to first assignment


def read_file_data(data):
    file = open(data, 'r')  # Open the file

    file_read = file.read()  # Read the contents of the file

    # Split the contents by newline characters
    transformation = file_read.split('\n')

    KB = transformation[1]

    q = transformation[3]

    KB = KB.split(';')[:-1]  # Split by ';' and remove the last empty element
    KB = [i.strip() for i in KB]  # Remove leading/trailing whitespaces

    return KB, q

# Function to get all unique literals from the Knowledge Base (KB)


def get_literals(KB):

    # Initialize an empty set to store unique literals
    literals = set()

    # Loop through each clause in the knowledge base
    for clause in KB:

        # If clause is an implication
        if '=>' in clause:
            # split into antecedent and consequent
            antecedent, consequent = clause.split('=>')
            literals.update(i.strip() for i in antecedent.split('&'))
            literals.add(consequent.strip())
        else:
            literals.add(clause.strip())

    return list(literals)

# Function to evaluate a clause by mapping the of literals to their truth values.
def evaluate_clause(clause, truth_values):
    if '=>' in clause:
        antecedent, consequent = clause.split('=>')
        antecedents = antecedent.split('&')
        return all(truth_values[i.strip()] for i in antecedents) <= truth_values[consequent.strip()]
    else:
        return truth_values[clause.strip()]

# Checks all posible combinations of truth tables by iterating through all combinations
# For the Pseudocode TT-CHECK-ALL this is that segment
def evaluate_truth_table(KB, q):
    literals = get_literals(KB)
    KB_true_models = [] 
    for values in itertools.product([False, True], repeat=len(literals)):
        truth_values = dict(zip(literals, values))
        if all(evaluate_clause(clause, truth_values) for clause in KB):
            KB_true_models.append(truth_values)
    return all(model[q] for model in KB_true_models)


# This counts the number of models (truth assignments) for which the KB and q are both true.
def count_models(KB, q):

    # Get all unique literals from the Knowledge Base
    literals = get_literals(KB)

    model_count = 0

    for values in itertools.product([False, True], repeat=len(literals)):
        # Map each literal to a truth value
        truth_values = dict(zip(literals, values))

        if all(evaluate_clause(clause, truth_values) for clause in KB):
            if truth_values[q]:
                model_count += 1
    return model_count


def forward_chaining(KB, q):
    proposition_queue = []
    for prop in KB:
        if len(prop) <= 2:
            proposition_queue.append(prop)
    symbolCount = {}
    for prop in KB:
        if '=>' in prop:
            antecedent, consequent = prop.split('=>')
            if '&' in antecedent:
                antecedents = antecedent.split('&')
                symbolCount["{}".format(prop)] = len(antecedents)
            else:
                symbolCount["{}".format(prop)] = 1
    result = False
    visited = []
    while len(proposition_queue) != 0:
        trueProp = proposition_queue.pop(0)
        visited.append(trueProp)
        for prop in KB:
            if '=>' in prop:
                if trueProp == q:
                    print("YES: ", end="")
                    for propo in visited:
                        print(f"{propo}, ", end="")
                    result = True
                    break
                antecedent, consequent = prop.split('=>')
                if trueProp in antecedent:
                    symbolCount["{}".format(prop)] -= 1
                    if symbolCount["{}".format(prop)] == 0:
                        proposition_queue.append(consequent.strip())
    if (result == False):
        print("NO")


def backward_chaining(KB, q):
    knownProps = {}
    for prop in KB:
        if len(prop) <= 2:
            knownProps[prop] = True
        else:
            antecedent, consequent = prop.split('=>')
            knownProps[consequent.strip()] = False
    visited = []
    result = truth_value(KB, knownProps, q, visited)
    if type(result) == tuple:
        if False in result:
            print("NO")
        else:
            print("YES: ", end="")
            for prop in visited:
                print(f"{prop}, ", end="")
    if type(result) == bool:
        if result == False:
            print("NO")
        else:
            print("YES: ", end="")
            for prop in visited:
                print(f"{prop}, ", end="")


def truth_value(KB, knownProps, q, visited):
    visited.append(q)
    if q not in knownProps:
        return False
    if knownProps[q] == True:
        return True

    for prop in KB:
        if '=>' in prop:
            antecedent, consequent = prop.split('=>')
            if (consequent.strip() == q):
                antecedent = antecedent.split('&')
                if len(antecedent) == 2:
                    return truth_value(KB, knownProps, antecedent[0].strip(), visited), truth_value(KB, knownProps, antecedent[1].strip(), visited)
                else:
                    return truth_value(KB, knownProps, antecedent[0].strip(), visited)

    return False


def main():
    if len(sys.argv) != 3:
        print("Usage: iengine <method of inference> <filename>")
        sys.exit(1)

    data = sys.argv[2]
    method_of_inference = sys.argv[1].lower()
    KB, q = read_file_data(data)

    print("\nKB:", KB)
    print("\nQuery:", q)

    if method_of_inference == 'tt':  # Truth Table method
        result = evaluate_truth_table(KB, q)
        if result:
            print("YES:", count_models(KB, q))
        else:
            print("NO")

    elif method_of_inference == "fc":  # Forward Chaining
        result = forward_chaining(KB, q)
    elif method_of_inference == "bc":  # Backward Chaining
        result = backward_chaining(KB, q)
    else:
        print("Unknown method of inference.")


if __name__ == "__main__":
    main()
