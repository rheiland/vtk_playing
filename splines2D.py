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

    points = vtk.vtkPoints()
    points.InsertPoint(0, 0, 0, 0)
    points.InsertPoint(1, 1, 1, 0)
    points.InsertPoint(2, 3, 0, 0)
    points.InsertPoint(3, 5, 2, 0)

    points2 = vtk.vtkPoints()
    points2.InsertPoint(0, 0, -1, 0)
    points2.InsertPoint(1, 1, 0.5, 0)
    points2.InsertPoint(2, 3, -1, 0)
    points2.InsertPoint(3, 5, 0, 0)

    # Fit a spline to the points
    spline = vtk.vtkParametricSpline()
    spline.SetPoints(points)

    spline2 = vtk.vtkParametricSpline()
    spline2.SetPoints(points2)

    functionSource = vtk.vtkParametricFunctionSource() 
    functionSource.SetParametricFunction(spline)
    functionSource.Update()

    functionSource2 = vtk.vtkParametricFunctionSource() 
    functionSource2.SetParametricFunction(spline2)
    functionSource2.Update()

    # sphere = vtk.vtkSphereSource()
    # sphere.SetPhiResolution(21)
    # sphere.SetThetaResolution(21)
    # sphere.SetRadius(0.1)

    splineMapper = vtk.vtkPolyDataMapper()
    splineMapper.SetInputConnection(functionSource.GetOutputPort())

    splineMapper2 = vtk.vtkPolyDataMapper()
    splineMapper2.SetInputConnection(functionSource2.GetOutputPort())

    splineActor = vtk.vtkActor()
    splineActor.SetMapper(splineMapper)
    splineActor.GetProperty().SetColor(colors.GetColor3d('Red'))
    splineActor.GetProperty().SetLineWidth(3.0)

    splineActor2 = vtk.vtkActor()
    splineActor2.SetMapper(splineMapper2)
    splineActor2.GetProperty().SetColor(colors.GetColor3d('White'))
    splineActor2.GetProperty().SetLineWidth(3.0)

    # Setup render window, renderer, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.SetWindowName('Splines 2D')
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    renderer.AddActor(splineActor)
    renderer.AddActor(splineActor2)

    renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))
    renderer.ResetCamera()

    renderWindow.SetSize(800, 800)
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
