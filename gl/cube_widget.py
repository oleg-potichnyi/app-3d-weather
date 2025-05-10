from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtGui import QColor
import OpenGL.GL as gl
import OpenGL.GLU as glu


class CubeWidget(QOpenGLWidget):
    """OpenGL widget for displaying a 3D cube
    with the ability to rotate and zoom with the mouse."""
    def __init__(self) -> None:
        super().__init__()
        self.angle_x = 0
        self.angle_y = 0
        self.scale = 1.0
        self.last_x = 0
        self.last_y = 0
        self.cube_colors = [
            QColor(255, 0, 0),
            QColor(0, 255, 0),
            QColor(0, 0, 255),
            QColor(255, 255, 0),
            QColor(0, 255, 255),
            QColor(255, 0, 255)
        ]

    def initializeGL(self) -> None:
        """Initialize OpenGL settings (lighting, depth, etc.)."""
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)

    def paintGL(self) -> None:
        """OpenGL scene rendering (rotating cube)."""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        gl.glTranslatef(0.0, 0.0, -5.0)
        gl.glRotatef(self.angle_x, 1.0, 0.0, 0.0)
        gl.glRotatef(self.angle_y, 0.0, 1.0, 0.0)
        gl.glScalef(self.scale, self.scale, self.scale)

        self.draw_cube()

    def draw_cube(self) -> None:
        """Function for drawing a simple cube."""
        gl.glBegin(gl.GL_QUADS)

        gl.glColor3f(
            self.cube_colors[0].redF(),
            self.cube_colors[0].greenF(),
            self.cube_colors[0].blueF()
        )
        gl.glVertex3f(-1.0, -1.0, 1.0)
        gl.glVertex3f(1.0, -1.0, 1.0)
        gl.glVertex3f(1.0, 1.0, 1.0)
        gl.glVertex3f(-1.0, 1.0, 1.0)

        gl.glColor3f(
            self.cube_colors[1].redF(),
            self.cube_colors[1].greenF(),
            self.cube_colors[1].blueF()
        )
        gl.glVertex3f(-1.0, -1.0, -1.0)
        gl.glVertex3f(-1.0, 1.0, -1.0)
        gl.glVertex3f(1.0, 1.0, -1.0)
        gl.glVertex3f(1.0, -1.0, -1.0)

        gl.glColor3f(
            self.cube_colors[2].redF(),
            self.cube_colors[2].greenF(),
            self.cube_colors[2].blueF()
        )
        gl.glVertex3f(-1.0, -1.0, -1.0)
        gl.glVertex3f(-1.0, -1.0, 1.0)
        gl.glVertex3f(-1.0, 1.0, 1.0)
        gl.glVertex3f(-1.0, 1.0, -1.0)

        gl.glColor3f(
            self.cube_colors[3].redF(),
            self.cube_colors[3].greenF(),
            self.cube_colors[3].blueF()
        )
        gl.glVertex3f(1.0, -1.0, -1.0)
        gl.glVertex3f(1.0, 1.0, -1.0)
        gl.glVertex3f(1.0, 1.0, 1.0)
        gl.glVertex3f(1.0, -1.0, 1.0)

        gl.glColor3f(
            self.cube_colors[4].redF(),
            self.cube_colors[4].greenF(),
            self.cube_colors[4].blueF()
        )
        gl.glVertex3f(-1.0, 1.0, -1.0)
        gl.glVertex3f(-1.0, 1.0, 1.0)
        gl.glVertex3f(1.0, 1.0, 1.0)
        gl.glVertex3f(1.0, 1.0, -1.0)

        gl.glColor3f(
            self.cube_colors[5].redF(),
            self.cube_colors[5].greenF(),
            self.cube_colors[5].blueF()
        )
        gl.glVertex3f(-1.0, -1.0, -1.0)
        gl.glVertex3f(1.0, -1.0, -1.0)
        gl.glVertex3f(1.0, -1.0, 1.0)
        gl.glVertex3f(-1.0, -1.0, 1.0)

        gl.glEnd()

    def resizeGL(self, w, h) -> None:
        """Handling window resizing."""
        if h == 0:
            h = 1
        gl.glViewport(0, 0, w, h)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45.0, w / h, 0.1, 50.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def mousePressEvent(self, event) -> None:
        """Clicking the mouse button."""
        if event.button() == Qt.LeftButton:
            self.last_x = event.x()
            self.last_y = event.y()

    def mouseMoveEvent(self, event) -> None:
        """Mouse movement is rotation."""
        dx = event.x() - self.last_x
        dy = event.y() - self.last_y

        self.angle_x += dy * 0.5
        self.angle_y += dx * 0.5

        self.last_x = event.x()
        self.last_y = event.y()

        self.update()

    def wheelEvent(self, event) -> None:
        """Mouse wheel - zoom."""
        delta = event.angleDelta().y()
        if delta > 0:
            self.scale *= 1.1
        else:
            self.scale /= 1.1

        self.update()

    def reset_view(self) -> None:
        """Reset the object's position."""
        self.angle_x = 0
        self.angle_y = 0
        self.scale = 1.0
        self.update()

    def choose_color(self, face_index: int) -> None:
        """Allows the user to select a color for a specific cube face."""
        current_color = self.cube_colors[face_index]
        color = QColorDialog.getColor(initial=current_color, parent=self)
        if color.isValid():
            self.cube_colors[face_index] = color
            self.update()
