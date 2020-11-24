import ast

s = '{"http":"10.167.75.21"}'
d = ast.literal_eval(s)
print(d)
