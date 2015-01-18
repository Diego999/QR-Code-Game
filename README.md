# QR-Code-Game
Find the shortest path starting from the top of the QR Code to the bottom, in a way to minimize the number of black cases and then, the number of white cases.

# Algorithm

It consider the QR Code as a grid graph and where each pixel is a vertice.
Each vertex has an edge to its neighbors. The value of a edge is as follows :

- If current case is a white case and the neighbor case is a black one -> 1
- If current case is a white case and also its neighbor -> 0 + epsilon
- If current case is a black case and the neighbor case is a white one -> 0 + epsilon
- If current case is a black case and also its neighbor -> 1

So moving in a black case has a cost. 0 + epsilon is a weight in order to minimize the number of white case in a path, if we have several "optimal" path.

And then, we create 2 subsets of vertices : the first one is the top vertices, the second one the bottom vertices.

Finally, we use dijsktra for each pair of vertices between thoses subsets, and we keep the shortest one.

The algorithm runs in O(V^(3/2) Lg(V))

# Requirements :

- [graph-tools](http://graph-tool.skewed.de/)
- pypng
- [pyqrcode](https://github.com/mnooner256/pyqrcode) 

# Examples :

- Small example

![QR Code](http://img11.hostingpics.net/pics/369238code.png)
![Solution QR Code](http://img11.hostingpics.net/pics/549684scode.png)
![Graph](http://img11.hostingpics.net/pics/813882graphcode.png)

- Larger example

![QR Code](http://img11.hostingpics.net/pics/514457code.png)
![Solution QR Code](http://img11.hostingpics.net/pics/577126scode.png)
![Graph](http://img11.hostingpics.net/pics/483599graphcode.png)