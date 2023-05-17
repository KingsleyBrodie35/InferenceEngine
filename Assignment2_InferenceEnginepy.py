import sys
import itertools

#First step is to extract data from the file in similar way to first assignment

def read_file_data(data):
    file = open(data, 'r')  # Open the file

    file_read = file.read()  # Read the contents of the file

    transformation = file_read.split('\n')  # Split the contents by newline characters

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

def main():
    if len(sys.argv) != 3:
        print("Usage: iengine <method of inference> <filename>")
        sys.exit(1)

    data = sys.argv[2]
    method_of_inference = sys.argv[1].lower()

    KB, q = read_file_data(data)

    print("KB:", KB)
    print("\nQuery:", q)

    if method_of_inference == 'tt':  # Truth Table method
        result = evaluate_truth_table(KB, q)
        print("Result:", result)
    else:
        print("Unknown method of inference.")

if __name__ == "__main__":
    main()