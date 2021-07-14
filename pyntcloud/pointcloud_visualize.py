import numpy as np
import plotly.graph_objs as go

coordinate = np.load('./npy/armadillo.obj.npy')
coordinate = coordinate

print(coordinate, coordinate.shape)

layout = go.Layout(title = "PT" )
plot_data = go.Scatter3d(x = coordinate[:,0], y = coordinate[:,1], z = coordinate[:,2],
                    mode = 'markers', marker = dict(size = 1))

fig = go.Figure(data = [plot_data], layout = layout)
fig.show()