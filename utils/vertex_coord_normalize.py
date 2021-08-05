import numpy as np

f = open("example.obj")

lines = f.readlines()

vertices = []
result = []
for line in lines:
    if 'v ' in line and '#' not in line: vertices.append(np.array(line.strip().split("v")[-1].strip().split(" ")).astype(float))
    else: result.append(line)

vertices = np.array(vertices)
for idx in range(3):
    max_value, min_value = np.max(vertices[:,idx]), np.min(vertices[:,idx])
    vertices[:,idx] = vertices[:,idx] - min_value - ((max_value - min_value) / 2)

vertices_result = np.empty([vertices.shape[0], 4])
vertices_result[:, 1:] = vertices[:, 0:]
vertices_result = vertices_result.astype(np.unicode)
vertices_result[:, 0] = 'v'

vertices_lines = []
for vertices in vertices_result:
    " ".join(list(vertices))
    vertices_lines.append(" ".join(list(vertices))+"\n")
vertices_lines += result

with open("example_result.obj","w") as f:
    f.write("".join(vertices_lines))

