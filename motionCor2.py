
import subprocess as subp
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Label, Layout
import dicttoxml

style = {'description_width': 'initial'}

#Input Widgets
inMrc = widgets.Text(
    value='/home/jvanschy/br76_scratch/relion21_tutorial/betagal/Micrographs/',
    placeholder='path for input MCR file or folder containing MRC files',
    description='Input: ',
    disabled=False,
    style=style)

inTiff = widgets.Text(
    placeholder='path for input TIFF file',
    description='Input TIFF: ',
    disabled=False,
    style=style)

outMrc = widgets.Text(
    value='/home/jvanschy/br76_scratch/relion21_tutorial/betagal/JayMotionCorr/',
    placeholder='path for output MCR file',
    description='Output: ',
    disabled=False,
    style=style)

fullSum = widgets.Text(
    placeholder='path for global-motion corrected MRC file',
    description='Output global-motion: ',
    disabled=False,
    style=style)

defectFile = widgets.Text(
    placeholder='path for the Defect file that details camera defects',
    description='DefectFile: ',
    disabled=False,
    style=style)

processing = widgets.Select(
    options=['Serial', 'Single'],
    description='Processing type: ',
    disabled=False,
    style=style)

gainFile = widgets.Text(
    placeholder='path for MRC file that stores the gain reference',
    description='Gain: ',
    disabled=False,
    style=style)

patch = widgets.Text(
    placeholder='Number of patches for alignment e.g. 5 5',
    description='Patch: ',
    disabled=False,
    style=style)

iteration = widgets.IntSlider(
    value=7,
    min=0,
    max=20,
    step=1,
    description='Iteration: ',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    style=style)

tolerance = widgets.FloatSlider(
    value=0.5,
    min=0,
    max=10,
    step=0.1,
    description='Tolerance: ',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f',
    style=style)

bFactor = widgets.IntSlider(
    value=150,
    min=0,
    max=1500,
    step=1,
    description='B-Factor',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    style=style)

stack = widgets.IntText(
    value=0,
    description='Frames per stack: ',
    disabled=False,
    style=style)

binningFactor = widgets.FloatSlider(
    value=1,
    min=1,
    max=10,
    step=0.1,
    description='Binning Factor',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f',
    style=style)

initDose = widgets.IntSlider(
    value=0,
    min=0,
    max=5,
    step=1,
    description='Initial Dose (e/A2)',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    style=style)

frameDose = widgets.IntSlider(
    value=0,
    min=0,
    max=5,
    step=1,
    description='Frame Dose (e/A2)',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d',
    style=style)

pixelSize = widgets.FloatSlider(
    value=0.5,
    min=0,
    max=4.0,
    step=0.1,
    description='Pixel Size (A): ',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.1f',
    style=style)

voltage = widgets.IntText(
    value=300,
    description='Voltage (kV): ',
    disabled=False,
    style=style)

throw = widgets.IntText(
    min=0,
    description='Throw: ',
    disabled=False,
    style=style)

trunc = widgets.IntText(
    min=0,
    description='Trunc: ',
    disabled=False,
    style=style)

group = widgets.IntText(
    value=0,
    description='Group frames: ',
    disabled=False,
    style=style)

fmRef = widgets.Select(
    options=['Central', 'First'],
    description='Reference frame: ',
    disabled=False,
    style=style)

tilt = widgets.Text(
    value='',
    placeholder='specify the starting angle followed by the tilt step. e.g. 0 2',
    description='Tilt Angle and Step: ',
    disabled=False,
    style=style)

rotGain = widgets.Select(
    options=['No rotation - default', 'Rotate 90', 'Rotate 180', 'Rotate 270'],
    description='Rotate Gain: ',
    disabled=False,
    style=style)

flipGain = widgets.Select(
    options=['No flip - default', 'upside down - horizontal axis', 'left right - vertical axis'],
    description='Flip Gain ',
    disabled=False,
    style=style)

gpu = widgets.Text(
    value='',
    placeholder='indicate the GPUs to use',
    description='GPU Usage: ',
    disabled=False,
    style=style)

#Output Widgets
args = widgets.Textarea(
    description='Arguments',
    description_tooltip='Arguments',
    disabled=False,
    rows=20,
    style=style,
    layout=Layout(width='90%'))

stdout = widgets.Textarea(
    description='Standard output',
    description_tooltip='Standard output',
    disabled=False,
    rows=20,
    style=style,
    layout=Layout(width='90%'))

stderr = widgets.Textarea(
    description='Standard Error',
    description_tooltip='Standard Error output',
    disabled=False,
    rows=20,
    style=style,
    layout=Layout(width='90%'))

#Jobs Widgets
existingJobs = [('Job1 | value 1'), ('Job2 | value 2'), ('Job3 | value 3'), ('Job3 | value4')]
saveJobs = [('')]

jobsList = widgets.SelectMultiple(
    description='Jobs: ', 
    options=existingJobs, 
    disabled=False, 
    style={'description_width': 'initial'}, 
    rows=10, 
    layout=Layout(width='90%'))

add = widgets.Button(
    description='Add', 
    disabled=False, 
    button_style='', 
    tooltip='Add job')

delete = widgets.Button(
    description='Delete', 
    disabled=False, 
    button_style='',
    tooltip='Delete job(s)')

save = widgets.Button(
    description='Save', 
    disabled=False, 
    button_style='', 
    tooltip='Save job(s)')

load = widgets.Button(
    description='Load', 
    disabled=False, 
    button_style='', 
    tooltip='Load job(s)')

run = widgets.Button(
    description='Run', 
    disabled=False, 
    button_style='', 
    tooltip='Run all jobs')

#Build the input widgets
def buildInputWidgets():
    io1 = VBox([inMrc, inTiff, outMrc, fullSum, defectFile, processing, gainFile, patch, iteration, tolerance, bFactor, stack, binningFactor])
    io2 = VBox([initDose, frameDose, pixelSize, voltage, throw, trunc, group, fmRef, tilt, rotGain, flipGain, gpu])
    inputFields = HBox([io1, io2])
    display(inputFields)

#Create the widgets to call motioncor2 and to display the output data
#def checkMandatoryFields():
#Jay call this inside call_motioncor2.
#Need to style mandatory fields somehow and setup, 

#Build argument list
def buildArgumentsList():
    args = ''
    
    if  inMrc.value is not '':
        args += "-InMrc " + inMrc.value
    if  inTiff.value is not '':
        args += " -InTiff " + inTiff.value
    if  outMrc.value is not '':
        args += " -OutMrc " + outMrc.value
    if  fullSum.value is not '':
        args += " -FullSum " + fullSum.value
    if  defectFile.value is not '':
        args += " -DefectFile " + defectFile.value
    if  gainFile.value is not '':
        args += " -Gain " + gainFile.value
    if  patch.value is not '':
        args += " -Patch " + patch.value
    if  tilt.value is not '':
        args += " -Tilt " + tilt.value
    if  gpu.value is not '':
        args += " -Gpu " + gpu.value

    if  processing.value == "Single":
        args += " -Serial 0"
    if  processing.value == "Serial":
        args += " -Serial 1"
    if  fmRef.value == "Central":
        args += " -FmRef 1"
    if  fmRef.value == "First":
        args += " -FmRef 0"
    if  rotGain.value == "No rotation - default":
        args += " -RotGain 0"
    if  rotGain.value == "Rotate 90":
        args += " -RotGain 1"
    if  rotGain.value == "Rotate 180":
        args += " -RotGain 2"
    if  rotGain.value == "Rotate 270":
        args += " -RotGain 3"
    if  flipGain.value == "No flip - default":
        args += " -FlipGain 0"
    if  flipGain.value == "upside down - horizontal axis":
        args += " -FlipGain 1"
    if  flipGain.value == "left right - vertical axis":
        args += " -FlipGain 2"
    
    if  iteration.value > 0:
        args += " -Iter " + str(iteration.value)
    if  tolerance.value > 0:
        args += " -Tol " + str(tolerance.value)
    if  bFactor.value > 0:
        args += " -Bft " + str(bFactor.value)
    if  stack.value > 0:
        args += " -StackZ " + str(stack.value)
    if  binningFactor.value > 1:
        args += " -FtBin " + str(binningFactor.value)
    if  initDose.value > 0:
        args += " -InitDose " + str(initDose.value)
    if  frameDose.value > 0:
        args += " -FmDose " + str(frameDose.value)
    if  pixelSize.value > 0:
        args += " -PixSize " + str(pixelSize.value)
    if  voltage.value > 0:
        args += " -kV " + str(voltage.value)
    if  throw.value > 0:
        args += " -Throw " + str(throw.value)
    if  trunc.value > 0:
        args += " -Trunc " + str(trunc.value)
    if  group.value > 0:
        args += " -Group " + str(group.value)
    
    return args
    
def call_motioncor2(b):
    
    #Clear output from previous run
    stdout.value = ''
    stderr.value = ''
    args.value = ''
    
    #Calling motioncor2
    #Note: shell=True. There are security implications for this. This was enabled as the arguments were not
    #being passed in to motioncor2 for some reason. Unable to determine why.
    #response = subp.run(["motioncor2 ",  buildArgumentsList()], stdout=subp.PIPE, stderr=subp.PIPE)
    #try:
    #response = subp.run("motioncor2 " + buildArgumentsList(), shell=True, stdout=subp.PIPE, stderr=subp.PIPE)
    response = subp.Popen("motioncor2 " + buildArgumentsList(), shell=True, stdout=subp.PIPE, stderr=subp.PIPE)
    #except sp.TimeoutExpired:
    #    stderr.value = 'Call timed out!'
    #except sp.SubprocessError:
    #    stderr.value = 'Subprocess Error!'

    while True:
        output = response.stdout.readline().decode()
        if  output == '' and response.poll() is not None:
            break
        if  output:
            stdout.value = stdout.value + output
    
    #stdout.value = response.stdout
    #stderr.value = response.stderr
    args.value = buildArgumentsList()

def buildOutputWidgets():
    runMotionCor2 = widgets.Button(
        description='Run',
        disabled=False,
        button_style='',
        tooltip='Run motioncor2',
        icon='check')

    runMotionCor2.on_click(call_motioncor2)

    display(runMotionCor2)
    organiseOutputs = VBox([stdout, stderr, args])
    display(organiseOutputs)

#Jobs widget supporting functions.
def buildNewJob():
    newJob = {"inMrc":inMrc.value}
    newJob['inTiff']        = inTiff.value
    newJob['outMrc']        = outMrc.value
    newJob['fullSum']       = fullSum.value
    newJob['defectFile']    = defectFile.value
    newJob['processing']    = processing.value
    newJob['gainFile']      = gainFile.value
    newJob['patch']         = patch.value
    newJob['iteration']     = iteration.value
    newJob['tolerance']     = tolerance.value   
    newJob['bFactor']       = bFactor.value 
    newJob['stack']         = stack.value
    newJob['binningFactor'] = binningFactor.value   
    newJob['initDose']      = initDose.value   
    newJob['frameDose']     = frameDose.value   
    newJob['pixelSize']     = pixelSize.value   
    newJob['voltage']       = voltage.value   
    newJob['throw']         = throw.value   
    newJob['trunc']         = trunc.value   
    newJob['group']         = group.value   
    newJob['tilt']          = tilt.value   
    newJob['rotGain']       = rotGain.value   
    newJob['flipGain']      = flipGain.value
    newJob['gpu']           = gpu.value
    newJobXML = dicttoxml.dicttoxml(newJob, attr_type=False, root=False)
    return newJobXML

def addJob(b):
    listedJobs = jobsList.options
    listedJobsList = list(listedJobs)
    newJob = buildNewJob()
    #converting to tuple
    newJobTuple = (newJob,)
    listedJobsList.extend(newJobTuple)
    jobsList.options = listedJobsList

def deleteJob(b):
    #obtain the listedJobs
    listedJobs = jobsList.options
    listedJobsList = list(listedJobs)
    #obtain the selectedJobs
    selectedJobs = jobsList.value
    selectedJobsList = list(selectedJobs)
    #remove selected jobs
    for i in range(len(selectedJobsList)):
        listedJobsList.remove(selectedJobsList[i])
    #update 
    jobsList.options = listedJobsList

def saveJobs(b):
    listedJobs = jobsList.options
    saveJobs = list(listedJobs)
    #store the variable in the IPython database.
    #%store saveJobs

def loadJobs(b):
    #restore all saved variables from the IPython database.
    #%store -r 
    #update the screen
    jobsList.options = saveJobs
    
def buildJobsWidgets():
    buttons = HBox([add, delete, save, load, run])
    selectableTable = VBox([jobsList, buttons])
    
    #Add fuctions to buttons.
    add.on_click(addJob)
    delete.on_click(deleteJob)
    save.on_click(saveJobs)
    load.on_click(loadJobs)

    display(selectableTable)