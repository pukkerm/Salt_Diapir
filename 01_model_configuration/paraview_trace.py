# trace generated using paraview version 5.13.0-RC1
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 13

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# find source
tinseriesxdmf = FindSource('tin.series.xdmf')

# set active source
SetActiveSource(tinseriesxdmf)

# Properties modified on tinseriesxdmf
tinseriesxdmf.PointArrayStatus = ['EroDep']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
tinseriesxdmfDisplay = Show(tinseriesxdmf, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
tinseriesxdmfDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show color bar/color legend
tinseriesxdmfDisplay.SetScalarBarVisibility(renderView1, True)

# find source
stratiViewpvd = FindSource('stratiView.pvd')

# show data in view
stratiViewpvdDisplay = Show(stratiViewpvd, renderView1, 'StructuredGridRepresentation')

# trace defaults for the display properties.
stratiViewpvdDisplay.Representation = 'Outline'

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'EroDep'
eroDepLUT = GetColorTransferFunction('EroDep')

# get opacity transfer function/opacity map for 'EroDep'
eroDepPWF = GetOpacityTransferFunction('EroDep')

# get 2D transfer function for 'EroDep'
eroDepTF2D = GetTransferFunction2D('EroDep')

# Properties modified on renderView1
renderView1.CenterOfRotation = [124500.0, 99500.0, -1341.16015625]
renderView1.CameraPosition = [413264.1327028394, -127837.00271082227, 359804.086884608]
renderView1.CameraFocalPoint = [139026.44879653642, 91584.55354667932, -16541.34275979896]
renderView1.CameraViewUp = [-0.6710842316391397, 0.31354351559310756, 0.6718157618535163]
renderView1.CameraParallelScale = 161211.0148549556

# create a new 'Transform'
transform1 = Transform(registrationName='Transform1', Input=tinseriesxdmf)

# Properties modified on transform1.Transform
transform1.Transform.Scale = [1.0, 1.0, 10.0]

# show data in view
transform1Display = Show(transform1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
transform1Display.Representation = 'Surface'

# hide data in view
Hide(tinseriesxdmf, renderView1)

# show color bar/color legend
transform1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=transform1.Transform)

# hide data in view
Hide(stratiViewpvd, renderView1)

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=transform1)

# Properties modified on calculator1
calculator1.Function = 'coordsZ'

# show data in view
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'

# hide data in view
Hide(transform1, renderView1)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'Result'
resultLUT = GetColorTransferFunction('Result')

# get opacity transfer function/opacity map for 'Result'
resultPWF = GetOpacityTransferFunction('Result')

# get 2D transfer function for 'Result'
resultTF2D = GetTransferFunction2D('Result')

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
resultLUT.ApplyPreset('Green-Blue Asymmetric Divergent (62Blbc)', True)

# invert the transfer function
resultLUT.InvertTransferFunction()

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
resultLUT.ApplyPreset('Muted Blue-Green', True)

# rescale color and/or opacity maps used to exactly fit the current data range
calculator1Display.RescaleTransferFunctionToDataRange(False, True)

# rescale color and/or opacity maps used to exactly fit the current data range
calculator1Display.RescaleTransferFunctionToDataRange(False, True)

# get animation scene
animationScene1 = GetAnimationScene()

animationScene1.GoToLast()

# set active source
SetActiveSource(transform1)

# show data in view
transform1Display = Show(transform1, renderView1, 'UnstructuredGridRepresentation')

# show color bar/color legend
transform1Display.SetScalarBarVisibility(renderView1, True)

# rescale color and/or opacity maps used to exactly fit the current data range
transform1Display.RescaleTransferFunctionToDataRange(False, True)

# Rescale transfer function
eroDepLUT.RescaleTransferFunction(0.0, 80.0)

# Rescale transfer function
eroDepPWF.RescaleTransferFunction(0.0, 80.0)

# Rescale 2D transfer function
eroDepTF2D.RescaleTransferFunction(0.0, 80.0, 0.0, 1.0)

# Properties modified on eroDepLUT
eroDepLUT.EnableOpacityMapping = 1

animationScene1.Play()

animationScene1.Play()

animationScene1.Play()

# set active source
SetActiveSource(tinseriesxdmf)

# Properties modified on tinseriesxdmf
tinseriesxdmf.GridStatus = ['Block.0[30]']

# update the view to ensure updated data information
renderView1.Update()

# Rescale transfer function
eroDepLUT.RescaleTransferFunction(-1451.792724609375, 188.94003295898438)

# Rescale transfer function
eroDepPWF.RescaleTransferFunction(-1451.792724609375, 188.94003295898438)

# Rescale transfer function
eroDepLUT.RescaleTransferFunction(0.0, 80.0)

# Rescale transfer function
eroDepPWF.RescaleTransferFunction(0.0, 80.0)

# Properties modified on tinseriesxdmf
tinseriesxdmf.GridStatus = ['Block.0', 'Block.0[10]', 'Block.0[11]', 'Block.0[12]', 'Block.0[13]', 'Block.0[14]', 'Block.0[15]', 'Block.0[16]', 'Block.0[17]', 'Block.0[18]', 'Block.0[19]', 'Block.0[1]', 'Block.0[20]', 'Block.0[21]', 'Block.0[22]', 'Block.0[23]', 'Block.0[24]', 'Block.0[25]', 'Block.0[26]', 'Block.0[27]', 'Block.0[28]', 'Block.0[29]', 'Block.0[2]', 'Block.0[30]', 'Block.0[3]', 'Block.0[4]', 'Block.0[5]', 'Block.0[6]', 'Block.0[7]', 'Block.0[8]', 'Block.0[9]']

# update the view to ensure updated data information
renderView1.Update()

# Rescale transfer function
eroDepLUT.RescaleTransferFunction(-1451.792724609375, 188.94003295898438)

# Rescale transfer function
eroDepPWF.RescaleTransferFunction(-1451.792724609375, 188.94003295898438)

# Properties modified on renderView1
renderView1.CameraPosition = [413264.1327028394, -127837.00271082227, 359804.086884608]

# Rescale transfer function
eroDepLUT.RescaleTransferFunction(0.0, 80.0)

# Rescale transfer function
eroDepPWF.RescaleTransferFunction(0.0, 80.0)

animationScene1.Play()

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

# Show orientation axes
renderView1.OrientationAxesVisibility = 1

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(2290, 1598)

# current camera placement for renderView1
renderView1.CameraPosition = [413264.1327028393, -127837.00271082224, 359804.086884608]
renderView1.CameraFocalPoint = [139026.44879653642, 91584.55354667932, -16541.34275979896]
renderView1.CameraViewUp = [-0.6710842316391397, 0.31354351559310756, 0.6718157618535163]
renderView1.CameraParallelScale = 161211.0148549556

# save animation
SaveAnimation(filename='E:/dataset/test/Canyon/data/fan_20260122/fan300/5.mp4', viewOrLayout=renderView1, location=16, ImageResolution=[2290, 1598],
    OverrideColorPalette='WhiteBackground',
    FrameRate=10,
    FrameWindow=[0, 30], 
    # MP4 Writer options
    FileName='')

# set active source
SetActiveSource(calculator1)

# hide data in view
Hide(calculator1, renderView1)

# hide data in view
Hide(transform1, renderView1)

# set active source
SetActiveSource(stratiViewpvd)

# create a new 'Clip'
clip1 = Clip(registrationName='Clip1', Input=stratiViewpvd)

# Properties modified on clip1.ClipType
clip1.ClipType.Position = [100000.0, 50000.0, -2560.016666666667]
clip1.ClipType.Length = [150000.0, 100000.0, 4857.300614539992]

# show data in view
clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
clip1Display.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get color transfer function/color map for 'relativeelevation'
relativeelevationLUT = GetColorTransferFunction('relativeelevation')

# Rescale transfer function
relativeelevationLUT.RescaleTransferFunction(-2560.016666666667, 1.723002496803181)

# get opacity transfer function/opacity map for 'relativeelevation'
relativeelevationPWF = GetOpacityTransferFunction('relativeelevation')

# Rescale transfer function
relativeelevationPWF.RescaleTransferFunction(-2560.016666666667, 1.723002496803181)

# get 2D transfer function for 'relativeelevation'
relativeelevationTF2D = GetTransferFunction2D('relativeelevation')

# rescale color and/or opacity maps used to exactly fit the current data range
clip1Display.RescaleTransferFunctionToDataRange(False, True)

# set scalar coloring
ColorBy(clip1Display, ('POINTS', 'thickness'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(relativeelevationLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
clip1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'thickness'
thicknessLUT = GetColorTransferFunction('thickness')

# get opacity transfer function/opacity map for 'thickness'
thicknessPWF = GetOpacityTransferFunction('thickness')

# get 2D transfer function for 'thickness'
thicknessTF2D = GetTransferFunction2D('thickness')

# rescale color and/or opacity maps used to exactly fit the current data range
clip1Display.RescaleTransferFunctionToDataRange(False, True)

# set scalar coloring
ColorBy(clip1Display, ('POINTS', 'layer ID'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(thicknessLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
clip1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'layerID'
layerIDLUT = GetColorTransferFunction('layerID')

# get opacity transfer function/opacity map for 'layerID'
layerIDPWF = GetOpacityTransferFunction('layerID')

# get 2D transfer function for 'layerID'
layerIDTF2D = GetTransferFunction2D('layerID')

# rescale color and/or opacity maps used to exactly fit the current data range
clip1Display.RescaleTransferFunctionToDataRange(False, True)

# set active source
SetActiveSource(transform1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=clip1.ClipType)

# show data in view
transform1Display = Show(transform1, renderView1, 'UnstructuredGridRepresentation')

# show color bar/color legend
transform1Display.SetScalarBarVisibility(renderView1, True)

# hide data in view
Hide(transform1, renderView1)

# set active source
SetActiveSource(calculator1)

# show data in view
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# hide data in view
Hide(calculator1, renderView1)

# set active source
SetActiveSource(clip1)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=clip1.ClipType)

# create a new 'Transform'
transform2 = Transform(registrationName='Transform2', Input=clip1)

# Properties modified on transform2.Transform
transform2.Transform.Scale = [1.0, 1.0, 100.0]

# show data in view
transform2Display = Show(transform2, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
transform2Display.Representation = 'Surface'

# hide data in view
Hide(clip1, renderView1)

# show color bar/color legend
transform2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# Rescale transfer function
relativeelevationLUT.RescaleTransferFunction(-2560.016666666667, 1.723002496803181)

# Rescale transfer function
relativeelevationPWF.RescaleTransferFunction(-2560.016666666667, 1.723002496803181)

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=transform2)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [145000.0, 100000.00000000001, -127920.80781865508]

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'

# hide data in view
Hide(transform2, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [150000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [160000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

renderView1.ResetActiveCameraToNegativeX()

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# hide data in view
Hide(slice1, renderView1)

# set active source
SetActiveSource(slice1)

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

#changing interaction mode based on data extents
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [495000.0000000001, 100000.00000000001, -105061.97418162298]
renderView1.CameraFocalPoint = [160000.0, 100000.00000000001, -105061.97418162298]

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [150000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

renderView1.ResetActiveCameraToNegativeX()

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [170000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

renderView1.ResetActiveCameraToNegativeX()

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [160000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [165000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [167000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [169000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [155000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [154000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [151000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [150000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'layer ID'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(relativeelevationLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on renderView1
renderView1.CenterOfRotation = [147000.0, 99999.99999999999, -69491.91118302374]
renderView1.CameraPosition = [341065.1324940005, 105610.93644557502, -65959.099346921]
renderView1.CameraFocalPoint = [147000.0, 105610.93644557502, -65959.099346921]
renderView1.CameraParallelScale = 41510.539074207736

# get color legend/bar for layerIDLUT in view renderView1
layerIDLUTColorBar = GetScalarBar(layerIDLUT, renderView1)

# change scalar bar placement
layerIDLUTColorBar.Position = [0.9022379912663755, 0.011889862327909888]

# change scalar bar placement
layerIDLUTColorBar.WindowLocation = 'Any Location'
layerIDLUTColorBar.ScalarBarLength = 0.07968710888610775

# change scalar bar placement
layerIDLUTColorBar.Position = [0.9066048034934497, 0.269712140175219]
layerIDLUTColorBar.ScalarBarLength = 0.0796871088861078

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
layerIDLUT.ApplyPreset('GBBr', True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
layerIDLUT.ApplyPreset('BrBG', True)

# Properties modified on layerIDLUT
layerIDLUT.NumberOfTableValues = 30

# change scalar bar placement
layerIDLUTColorBar.Position = [0.8812772925764192, 0.32603254067584475]

# change scalar bar placement
layerIDLUTColorBar.Position = [0.893504366812227, 0.3247809762202753]

# change scalar bar placement
layerIDLUTColorBar.Position = [0.8943777292576418, 0.5212765957446808]
layerIDLUTColorBar.ScalarBarLength = 0.07968710888610786

# invert the transfer function
layerIDLUT.InvertTransferFunction()

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [160000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'thickness'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(layerIDLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'layer ID'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(thicknessLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [170000.0, 100000.00000000001, -127920.80781865508]

# update the view to ensure updated data information
renderView1.Update()

# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [0.0, 1.0, 0.0]

# update the view to ensure updated data information
renderView1.Update()

renderView1.ResetActiveCameraToPositiveY()

# reset view to fit data
renderView1.ResetCamera(False, 0.9)

# set active source
SetActiveSource(transform2)

# toggle interactive widget visibility (only when running from the GUI)
ShowInteractiveWidgets(proxy=transform2.Transform)

# Properties modified on transform2.Transform
transform2.Transform.Scale = [1.0, 1.0, 10.0]

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(slice1)

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=transform2.Transform)

# Properties modified on slice1Display.DataAxesGrid
slice1Display.DataAxesGrid.GridAxesVisibility = 1

# Properties modified on slice1Display.DataAxesGrid
slice1Display.DataAxesGrid.GridAxesVisibility = 0

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 1

# Properties modified on slice1Display.DataAxesGrid
slice1Display.DataAxesGrid.GridAxesVisibility = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 0

# Properties modified on slice1Display.DataAxesGrid
slice1Display.DataAxesGrid.GridAxesVisibility = 0

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.ShowGrid = 1
renderView1.AxesGrid.XAxisUseCustomLabels = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.ShowGrid = 0

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.XAxisUseCustomLabels = 0

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.UseCustomBounds = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.UseCustomBounds = 0

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.XAxisUseCustomLabels = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.YAxisUseCustomLabels = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.ZAxisUseCustomLabels = 1

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.XAxisUseCustomLabels = 0

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.YAxisLabels = [0.0, 250000.0]

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.YAxisUseCustomLabels = 0

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.XAxisUseCustomLabels = 1
renderView1.AxesGrid.XAxisLabels = [0.0, 250000.0]
renderView1.AxesGrid.YAxisUseCustomLabels = 1
renderView1.AxesGrid.YAxisLabels = []

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.XAxisLabels = [0.0, 250000.0, 100000.0]

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.XAxisLabels = [100000.0, 150000.0, 200000.0, 250000.0]

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 0

# Properties modified on renderView1.AxesGrid
renderView1.AxesGrid.Visibility = 1

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(2290, 1598)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.InteractionMode = '2D'
renderView1.CameraPosition = [169168.43192018286, -472347.2586368099, -15915.359150655751]
renderView1.CameraFocalPoint = [169168.43192018286, 100000.00000000001, -15915.359150655751]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 39008.409707427345


##--------------------------------------------
## You may need to add some code at the end of this python script depending on your usage, eg:
#
## Render all views to see them appears
# RenderAllViews()
#
## Interact with the view, usefull when running from pvpython
# Interact()
#
## Save a screenshot of the active view
# SaveScreenshot("path/to/screenshot.png")
#
## Save a screenshot of a layout (multiple splitted view)
# SaveScreenshot("path/to/screenshot.png", GetLayout())
#
## Save all "Extractors" from the pipeline browser
# SaveExtracts()
#
## Save a animation of the current active view
# SaveAnimation()
#
## Please refer to the documentation of paraview.simple
## https://kitware.github.io/paraview-docs/latest/python/paraview.simple.html
##--------------------------------------------