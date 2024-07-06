#!/usr/bin/env python

# This example creates a tube around a line.
# This is helpful because when you zoom the camera, 
# the thickness of a line remains constant, 
# while the thickness of a tube varies.


import vtk 
# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    colors = vtkNamedColors()

    asource = vtk.vtkSTLReader()
    asource.SetFileName("vessel.stl")

    dataMapper = vtkPolyDataMapper()
    dataMapper.SetInputConnection(asource.GetOutputPort())

    model = vtkActor()
    model.SetMapper(dataMapper)
    model.GetProperty().SetColor(1, 0, 0)
    model.VisibilityOn()


    # Setup render window, renderer, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.SetWindowName('TubeFilter')
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # Visualise the arrow
    # renderer.AddActor(lineActor)
    renderer.AddActor(model)

    renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))
    renderer.ResetCamera()

    renderWindow.SetSize(800, 800)
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
