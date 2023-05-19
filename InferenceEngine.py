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


def get_literals(KB):
    literals = set()
    for clause in KB:
        if '=>' in clause:
            antecedent, consequent = clause.split('=>')
            literals.update(i.strip() for i in antecedent.split('&'))
            literals.add(consequent.strip())
        else:
            literals.add(clause.strip())
    return list(literals)


def evaluate_clause(clause, truth_values):
    if '=>' in clause:
        antecedent, consequent = clause.split('=>')
        antecedents = antecedent.split('&')
        return (all(truth_values[i.strip()] for i in antecedents)) == truth_values[consequent.strip()]
    else:
        return truth_values[clause.strip()]


def evaluate_truth_table(KB, q):
    literals = get_literals(KB)
    for values in itertools.product([False, True], repeat=len(literals)):
        truth_values = dict(zip(literals, values))
        if all(evaluate_clause(clause, truth_values) for clause in KB):
            if truth_values[q]:
                return True
    return False


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
    while len(proposition_queue) != 0:
        trueProp = proposition_queue.pop(0)
        for prop in KB:
            if '=>' in prop:
                if prop == q:
                    return True
                antecedent, consequent = prop.split('=>')
                if trueProp in antecedent:
                    symbolCount["{}".format(prop)] -= 1
                    if symbolCount["{}".format(prop)] == 0:
                        proposition_queue.append(consequent)
    return False


def main():
    if len(sys.argv) != 4:
        print("Usage: iengine <method of inference> <filename>")
        sys.exit(1)

    data = sys.argv[3]
    method_of_inference = sys.argv[2].lower()

    KB, q = read_file_data(data)

    print("KB:", KB)
    print("\nQuery:", q)

    if method_of_inference == 'tt':  # Truth Table method
        result = evaluate_truth_table(KB, q)
        print("Result:", result)
    if method_of_inference == "fc":  # Forward Chaining
        result = forward_chaining(KB, q)
        print("Result:", result)
    else:
        print("Unknown method of inference.")


if __name__ == "__main__":
    main()
