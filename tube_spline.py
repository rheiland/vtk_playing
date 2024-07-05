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
    points.InsertPoint(0, 1, 0, 0)
    points.InsertPoint(1, 2, 0, 0)
    points.InsertPoint(2, 3, 1, 0)
    points.InsertPoint(3, 4, 1, 0)
    points.InsertPoint(4, 5, 0, 0)
    points.InsertPoint(5, 6, 0, 0)

    # Fit a spline to the points
    spline = vtk.vtkParametricSpline()
    spline.SetPoints(points)
    functionSource = vtk.vtkParametricFunctionSource()
    functionSource.SetParametricFunction(spline)
    functionSource.SetUResolution(10 * points.GetNumberOfPoints())
    functionSource.Update()

    # Interpolate the scalars
    interpolatedRadius = vtk.vtkTupleInterpolator()
    interpolatedRadius.SetInterpolationTypeToLinear()
    interpolatedRadius.SetNumberOfComponents(1)

    # Generate the radius scalars
    tubeRadius = vtk.vtkDoubleArray()
    n = functionSource.GetOutput().GetNumberOfPoints()
    tubeRadius.SetNumberOfTuples(n)
    tubeRadius.SetName("TubeRadius")

    tMin = interpolatedRadius.GetMinimumT()
    tMin = 0.2
    tMax = interpolatedRadius.GetMaximumT()
    tMax = 0.6
    print(f'n={n}, tMin={tMin}, tMax={tMax}')
    for i in range(n):
        t = (tMax - tMin) / (n - 1) * i + tMin
        # print("t=",t)
        r = 1.0
        r = t
        #interpolatedRadius.InterpolateTuple(t, r) ### ??? Donesn't work for Python
        tubeRadius.SetTuple1(i, r)

    # Add the scalars to the polydata
    tubePolyData = functionSource.GetOutput()
    tubePolyData.GetPointData().AddArray(tubeRadius)
    tubePolyData.GetPointData().SetActiveScalars("TubeRadius")

    # Create the tubes
    tuber = vtk.vtkTubeFilter()
    # tuber.SetInput(tubePolyData)
    tuber.SetInputData(tubePolyData)
    tuber.SetNumberOfSides(20)
    tuber.SetVaryRadiusToVaryRadiusByAbsoluteScalar()

    # Setup actors and mappers
    lineMapper = vtk.vtkPolyDataMapper()
    # lineMapper.SetInput(tubePolyData)
    lineMapper.SetInputData(tubePolyData)
    # lineMapper.SetScalarRange(tubePolyData.GetScalarRange())

    tubeMapper = vtk.vtkPolyDataMapper()
    tubeMapper.SetInputConnection(tuber.GetOutputPort())
    tubeMapper.SetScalarRange(tubePolyData.GetScalarRange())

    lineActor = vtk.vtkActor()
    lineActor.SetMapper(lineMapper)
    tubeActor = vtk.vtkActor()
    tubeActor.SetMapper(tubeMapper)
    tubeActor.GetProperty().SetColor(colors.GetColor3d('Red'))


    # Setup render window, renderer, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.SetWindowName('TubeFilter')
    renderWindow.AddRenderer(renderer)

    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # Visualise the arrow
    # renderer.AddActor(lineActor)
    renderer.AddActor(tubeActor)

    renderer.SetBackground(colors.GetColor3d('DarkSlateGray'))
    renderer.ResetCamera()

    renderWindow.SetSize(800, 800)
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
