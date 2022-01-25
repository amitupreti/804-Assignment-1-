import vtk

## Read the model with VtkSTLREADER and import the model
reader = vtk.vtkSTLReader()
reader.SetFileName("Waving_Groot_15.5cm.stl")


# Rotate the models by xyz
def rotateActor(actor,x,y,z):
    actor.RotateX(x)
    actor.RotateY(y)
    actor.RotateZ(z)
    return actor

# Setups the common property
def setProperty(property):
    
    property.ShadingOn()
    property.SetColor(1, 1, 0)
    property.SetDiffuse(0.8) 
    property.SetAmbient(0.3) 
    property.SetSpecular(1.0) 
    property.SetSpecularPower(100.0)


# lightining for last 3 models
def setupLight():
    light = vtk.vtkLight ()
    light.SetLightTypeToSceneLight()
    light.SetAmbientColor(1, 1, 1)
    light.SetDiffuseColor(1, 1, 1)
    light.SetSpecularColor(1, 1, 1)
    light.SetPosition(-100, 100, 25)
    light.SetFocalPoint(0,0,0)
    light.SetIntensity(0.8)
    return light

def CreateViewPort(reader,writeFileName,ROTATION_ANGLE_X=-90,ROTATION_ANGLE_Y=0,ROTATION_ANGLE_Z=0):
    
    #Setup normal vectors
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(reader.GetOutputPort())

    # setup mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())
    
    # Setup actors for different views
    
    actor1 = vtk.vtkActor()
    actor2 = vtk.vtkActor()
    actor3 = vtk.vtkActor()
    actor4 = vtk.vtkActor()

    #Actor 1
    mapper.SetInputConnection(reader.GetOutputPort())
    actor1.SetMapper(mapper)
    actor1 = rotateActor(actor1,ROTATION_ANGLE_X,ROTATION_ANGLE_Y,ROTATION_ANGLE_Z)
    actor1.GetProperty().SetRepresentationToWireframe()

    # Actor 2
    actor2.SetMapper(mapper)

    property2 = actor2.GetProperty()
    property2.SetInterpolationToFlat() # Set shading to Flat
    setProperty(property2)

   
    actor2 = rotateActor(actor2,ROTATION_ANGLE_X,ROTATION_ANGLE_Y,ROTATION_ANGLE_Z)


    # Setup the lights for last 3 models

    light = setupLight()
    actor3.SetMapper(mapper)
    property3 = actor3.GetProperty()
    property3.SetInterpolationToGouraud() # Set shading to Gouraud
    setProperty(property3)
    actor3 = rotateActor(actor3,ROTATION_ANGLE_X,ROTATION_ANGLE_Y,ROTATION_ANGLE_Z)


    actor4.SetMapper(mapper)
    property4 = actor4.GetProperty()
    property4.SetInterpolationToPhong() # Set shading to Phong
    setProperty(property4)
    actor4 = rotateActor(actor4,ROTATION_ANGLE_X,ROTATION_ANGLE_Y,ROTATION_ANGLE_Z)


    render1 = vtk.vtkRenderer()
    render2 = vtk.vtkRenderer()
    render3 = vtk.vtkRenderer()
    render4 = vtk.vtkRenderer()

    # Setup the 4 ports and select which model goes in which port

    render1.SetViewport(0, 0.5, 0.5, 1)
    render2.SetViewport(0.5, 0.5, 1.0, 1.0)
    render3.SetViewport(0, 0, 0.5, 0.5) # xmin, ymin, xmax, ymax
    render4.SetViewport(0.5, 0, 1.0, 0.5)
    render1.AddActor(actor1)
    render2.AddActor(actor2)
    render3.AddActor(actor3)
    render4.AddActor(actor4)

    render2.AddLight(light)


    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetSize(700, 600)
    renderWindow.AddRenderer(render1)
    renderWindow.AddRenderer(render2)
    renderWindow.AddRenderer(render3)
    renderWindow.AddRenderer(render4)
    renderWindow.Render()

    # Save As Image

    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(renderWindow)
    w2i.Update()

    jwriter = vtk.vtkJPEGWriter()    
    jwriter.SetInputData(w2i.GetOutput())
    jwriter.SetFileName(writeFileName)
    jwriter.Write()

CreateViewPort(ROTATION_ANGLE_X=-90,ROTATION_ANGLE_Y=0,ROTATION_ANGLE_Z=0,reader=reader,writeFileName='angle_1_normal.png')
CreateViewPort(ROTATION_ANGLE_X=-90,ROTATION_ANGLE_Y=0,ROTATION_ANGLE_Z=90,reader=reader,writeFileName='angle_2_normal.png')
CreateViewPort(ROTATION_ANGLE_X=-90,ROTATION_ANGLE_Y=0,ROTATION_ANGLE_Z=180,reader=reader,writeFileName='angle_3_normal.png')
CreateViewPort(ROTATION_ANGLE_X=-90,ROTATION_ANGLE_Y=0,ROTATION_ANGLE_Z=270,reader=reader,writeFileName='angle_4_normal.png')

