import numpy as np
import re

class GraphDisplay():
    def __init__(self, graph=None, rotatex = 0, rotatey = 0, rotatez = 0):

        self.graph = graph
        self.height = 600
        self.width = 600

        self.center = [self.width/2, self.width/2, 0]
        self.x0 = [-self.width/2, 0, 0]
        self.x1 = [self.width/2, 0, 0]

        self.y0 = [0, -self.width/2, 0]
        self.y1 = [0, self.width/2, 0]

        self.z0 = [0, 0, -self.width/2]
        self.z1 = [0, 0, self.width/2]
        self.R = None
        self.rotation_matrix(rotatex, rotatey, rotatez)

    def rotation_matrix(self, xdeg=0.0, ydeg=0.0, zdeg=0.0):
        xrad = xdeg * np.pi / 180
        yrad = ydeg * np.pi / 180
        zrad = zdeg * np.pi / 180

        rotate_x = np.asmatrix([[1, 0, 0], [0, np.cos(xrad), -np.sin(xrad)], [0, np.sin(xrad), np.cos(xrad)]])
        rotate_y = np.asmatrix([[np.cos(yrad), 0, np.sin(yrad)], [0, 1, 0], [-np.sin(yrad), 0, np.cos(yrad)]])
        rotate_z = np.asmatrix([[np.cos(zrad), -np.sin(zrad), 0], [np.sin(zrad), np.cos(zrad), 0], [0, 0, 1]])

        self.R = rotate_z*rotate_y*rotate_x

        self.x0 = np.asarray(self.center + self.x0*self.R)[0]
        self.x1 = np.asarray(self.center + self.x1*self.R)[0]

        self.y0 = np.asarray(self.center + self.y0*self.R)[0]
        self.y1 = np.asarray(self.center + self.y1*self.R)[0]

        self.z0 = np.asarray(self.center + self.z0*self.R)[0]
        self.z1 = np.asarray(self.center + self.z1*self.R)[0]

    def create_label_xy(self, text='label'):
        return '''
        ctx.beginPath();
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.font = "10px Arial";
        ctx.fillText("For Immigration", {}, 30);
        ctx.fillText("Imod Immigration", {}, {});
        ctx.fillText("Socialistisk", 10, {});
        ctx.fillText("Liberal", {}, {});
       
        
        '''.format(10 + self.width/2,
                   10 + self.width/2,
                   self.height-30,
                   self.height/2-10,
                   self.width-60,
                   self.height/2-10,
                   )

    def create_xaxis(self):
        return '''
            ctx.beginPath();
            var gradx = ctx.createLinearGradient({}, {}, {}, {});
            gradx.addColorStop(0, "transparent");
            gradx.addColorStop({}, "white");
            ctx.strokeStyle = gradx;
            ctx.moveTo({}, {});
            ctx.lineTo({}, {});
            ctx.lineWidth = 1;
            ctx.stroke();
        '''.format(self.x0[0], self.x0[1], self.x1[0], self.x1[1], abs(self.x0[2]/self.width), self.x0[0], self.x0[1], self.x1[0], self.x1[1])

    def create_yaxis(self):
        return '''
             ctx.beginPath();
             var grady= ctx.createLinearGradient({}, {}, {}, {});
             grady.addColorStop(0, "transparent");
             grady.addColorStop({}, "white");
             ctx.strokeStyle = grady;
             ctx.moveTo({}, {});
             ctx.lineTo({}, {});
             ctx.lineWidth = 1;
             ctx.stroke();
         '''.format(self.y0[0], self.y0[1], self.y1[0], self.y1[1], abs(self.y0[2]/self.width), self.y0[0], self.y0[1], self.y1[0], self.y1[1])

    def create_zaxis(self):
        return '''
            ctx.beginPath();
            var gradz = ctx.createLinearGradient({}, {}, {}, {});
            gradz.addColorStop(0, "transparent");
            gradz.addColorStop({}, "white");

            ctx.strokeStyle = gradz;
            ctx.moveTo({}, {});
            ctx.lineTo({}, {});
            ctx.lineWidth = 1;
            ctx.stroke();
         '''.format(self.z0[0], self.z0[1], self.z1[0], self.z1[1], abs(self.z0[2]/self.width), self.z0[0], self.z0[1], self.z1[0], self.z1[1])

    def create_connection(self, p0, p1):
        return '''
            ctx.beginPath();
            ctx.strokeStyle = "rgb(190, 190, 255, 0.2)";
            ctx.moveTo({}, {});
            ctx.lineTo({}, {});
            ctx.lineWidth = 2;
            ctx.stroke();
        
        '''.format( p0[0], p0[1], p1[0], p1[1], p0[0], p0[1], p1[0], p1[1])

    def create_connections(self):
        data = ''
        for cni in self.graph.connections:
            for cnj in self.graph.connections[cni]:
                node_i = self.graph.nodes[cni].feature_vector
                node_i = self.center +  self.width/3 * np.asarray(node_i) * self.R
                node_i = np.asarray(node_i)[0]

                node_j = self.graph.nodes[cnj].feature_vector
                node_j = self.center + self.width/3 * np.asarray(node_j) * self.R
                node_j = np.asarray(node_j)[0]

                data += self.create_connection(node_i, node_j)
        return data

    def node(self, x, y, name, size=10, rgb=(255, 0, 0, 0)):
        return '''
  
            var centerX = {};
            var centerY = {};
            var radius = {};
          
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'rgba({}, {}, {}, {})';
            ctx.fill();
            ctx.lineWidth = 1;
            ctx.lineStyle = 'rgba(0, 0, 0, 1)'
            ctx.stroke();
            ctx.fillText('{}', {}, {});  
          
                        
        '''.format(x, y, size, rgb[0], rgb[1], rgb[2], rgb[3], name,  14 + x, y)

    def create_nodes(self):
        data = ''
        for n in self.graph.nodes.values():
            feature_vector = self.center + self.width/3*np.asarray(n.feature_vector)*self.R
            feature_vector = np.asarray(feature_vector)[0]

            opacity = 1
            if feature_vector[2] < 0:
                opacity = abs(feature_vector[2])/200

            color = feature_vector
            if n.party:
                aff = n.party
            else:
                aff = n.screen_name

            data += self.node(
                              color[0],
                              color[1],
                              aff,
                              0.8*np.log(1 + n.followers),
                              [feature_vector[0],
                               feature_vector[2],
                               feature_vector[1],
                               opacity],
                               )
        return data

    def script(self):
        return """<script>
                    var c = document.getElementById("myCanvas");
                    var ctx = c.getContext("2d");
                    // Create gradient
                    var grd = ctx.createLinearGradient(0,0,0,{});
                    grd.addColorStop(0,"rgb(43, 56, 81)");
                    grd.addColorStop(1,"rgb(43, 56, 81)");
                    // Fill with gradient
                    ctx.fillStyle = grd;
                    ctx.fillRect(0,0,{},{});
                    
                    {}
                    {}
                    {}
                    {}
                    {}
                    {}
                  
                  
        </script>""".format(
                            self.height,
                            self.width,
                            self.height,
                            self.create_xaxis(),
                            self.create_yaxis(),
                            self.create_zaxis(),
                            self.create_connections(),
                            self.create_nodes(),
                            self.create_label_xy(text='label'),
                            )

    def canvas(self):
        return '<canvas style="padding-top: 10px;" id="myCanvas" width={}; height={};>'.format(self.width, self.height)