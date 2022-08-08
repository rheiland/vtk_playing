#!/usr/bin/env python

import vtk

import sys

# some radii
radii = vtk.vtkFloatArray()
radii.InsertNextValue(1.0)
radii.InsertNextValue(0.1)
radii.InsertNextValue(0.2)
radii.SetName("radius")

# define the colours for the spheres
tags = vtk.vtkFloatArray()
tags.InsertNextValue(1.0)
tags.InsertNextValue(0.5)
tags.InsertNextValue(0.7)
tags.SetName("tag")

data = vtk.vtkFloatArray()
data.SetNumberOfComponents(2)
data.SetNumberOfTuples(3)
data.CopyComponent(0, radii, 0)
data.CopyComponent(1, tags, 0)
data.SetName("data")

# define the locations of the spheres
points = vtk.vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1, 1, 0)

# construct the grid
grid = vtk.vtkUnstructuredGrid()
grid.SetPoints(points)
grid.GetPointData().AddArray(data)
grid.GetPointData().SetActiveScalars("data")

# Create a sphere to use as a glyph source for vtkGlyph3D.
sphere = vtk.vtkSphereSource()
sphere.SetRadius(0.5)
sphere.SetPhiResolution(16)
sphere.SetThetaResolution(16)

# make the glyphs
glyph = vtk.vtkGlyph3D()
# glyph.SetInput(grid)
# glyph.SetSource(sphere.GetOutput())
glyph.SetInputData(grid)
glyph.SetSourceConnection(sphere.GetOutputPort())

glyph.ClampingOff()
glyph.SetScaleModeToScaleByScalar()
glyph.SetScaleFactor(1.0)
glyph.SetColorModeToColorByScalar()

# set up the mapper
mapper = vtk.vtkPolyDataMapper()
# mapper.SetInput(glyph.GetOutput())
mapper.SetInputConnection(glyph.GetOutputPort())

mapper.ScalarVisibilityOn()
mapper.ColorByArrayComponent("data", 1)

# set up the actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# do renderer setup stuff
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetSize(640, 480)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# add the actor to the renderer
ren.AddActor(actor)

# render
iren.Initialize()
renWin.Render()
iren.Start()
