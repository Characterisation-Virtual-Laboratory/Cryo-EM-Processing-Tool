import subprocess as subp
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Box, Label, Layout

#style and Layout
styleBasic    = {'description_width': '100px'}
styleAdvanced = {'description_width': '130px'}
basicLayout   = Layout(width='60%')
advLayout     = Layout(width='100%')

##Debug assistance
debug = widgets.Textarea(
    description='Debugging:',
    description_tooltip='Standard output',
    disabled=False,
    rows=10,
    style=styleBasic,
    layout=basicLayout)

def buildDebug():
    display(debug)

#Input Widgets
inMrc = widgets.Text(
    value='/home/jvanschy/br76_scratch/relion21_tutorial/betagal/Micrographs/',
    placeholder='path for input MCR file or folder containing MRC files',
        description='Input: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

outMrc = widgets.Text(
    value='/home/jvanschy/br76_scratch/relion21_tutorial/betagal/JayMotionCorr/',
    placeholder='path for output MCR file',
    description='Output: ',
    disabled=False,
    style=styleBasic,
    layout=basicLayout)

gainFile = widgets.Text(
    placeholder='path for MRC file that stores the gain reference',
    description='Gain: ',
    disabled=False,
    style=styleBasic,
    layout=basicLayout)

patch = widgets.Text(
    placeholder='Number of patches for alignment e.g. 5 5',
    description='Patch: ',
    disabled=False,
    style=styleBasic,
    layout=basicLayout)

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
    style=styleBasic,
    layout=basicLayout)

pixelSize = widgets.FloatSlider(
    value=0.5,
    min=0,
    max=4.0,
    step=0.01,
    description='Pixel Size (A): ',
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='.01f',
    style=styleBasic,
    layout=basicLayout)

voltage = widgets.IntText(
    value=300,
    description='Voltage (kV): ',
    disabled=False,
    style=styleBasic,
    layout=basicLayout)

gpu = widgets.Text(
    value='',
    placeholder='indicate the GPUs to use',
    description='GPU Usage: ',
    disabled=False,
    style=styleBasic,
    layout=basicLayout)

inTiff = widgets.Text(
    placeholder='path for input TIFF file',
    description='Input TIFF: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

fullSum = widgets.Text(
    placeholder='path for global-motion corrected MRC file',
    description='Output global-motion: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

defectFile = widgets.Text(
    placeholder='path for the Defect file that details camera defects',
    description='DefectFile: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

processing = widgets.Select(
    options=['Serial', 'Single'],
    description='Processing type: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

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
    style=styleAdvanced,
    layout=advLayout)

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
    style=styleAdvanced,
    layout=advLayout)

stack = widgets.IntText(
    value=0,
    description='Frames per stack: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

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
    style=styleAdvanced,
    layout=advLayout)

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
    style=styleAdvanced,
    layout=advLayout)

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
    style=styleAdvanced,
    layout=advLayout)

throw = widgets.IntText(
    min=0,
    description='Throw: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

trunc = widgets.IntText(
    min=0,
    description='Trunc: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

group = widgets.IntText(
    value=0,
    description='Group frames: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

fmRef = widgets.Select(
    options=['Central', 'First'],
    description='Reference frame: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

tilt = widgets.Text(
    value='',
    placeholder='specify the starting angle followed by the tilt step. e.g. 0 2',
    description='Tilt Angle and Step: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

rotGain = widgets.Select(
    options=['No rotation - default', 'Rotate 90', 'Rotate 180', 'Rotate 270'],
    description='Rotate Gain: ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

flipGain = widgets.Select(
    options=['No flip - default', 'upside down - horizontal axis', 'left right - vertical axis'],
    description='Flip Gain ',
    disabled=False,
    style=styleAdvanced,
    layout=advLayout)

#Output Widgets
outputLayout = Layout(width='90%')

args = widgets.Textarea(
    description='Arguments',
    description_tooltip='Arguments',
    disabled=False,
    rows=2,
    style=styleBasic,
    layout=outputLayout)

stdout = widgets.Textarea(
    description='Standard output',
    description_tooltip='Standard output',
    disabled=False,
    rows=20,
    style=styleBasic,
    layout=outputLayout)

stderr = widgets.Textarea(
    description='Standard Error',
    description_tooltip='Standard Error output',
    disabled=False,
    rows=5,
    style=styleBasic,
    layout=outputLayout)

#Jobs Widgets
existingJobs = []
header = [("Job# | inMrc | outMrc | pixelSize | patch | bFactor | voltage | gainFile |  gpu | inTiff | fullSum | defectFile | processing | iteration | tolerance | stack | binningFactor | initDose | frameDose | throw | trunc | group | fmRef | tilt | rotGain | flipGain |")]


jobsList = widgets.SelectMultiple(
    description='Jobs: ',
    options=header,
    disabled=False,
    style={'description_width': 'initial'},
    rows=10,
    layout=Layout(width='90%'))

addButton = widgets.Button(
    description='Add',
    disabled=False,
    button_style='',
    tooltip='Add job')

deleteButton = widgets.Button(
    description='Delete',
    disabled=False,
    button_style='',
    tooltip='Delete job(s)')

saveButton = widgets.Button(
    description='Save',
    disabled=False,
    button_style='',
    tooltip='Save job(s)')

loadButton = widgets.Button(
    description='Load',
    disabled=False,
    button_style='',
    tooltip='Load job(s)')

runButton = widgets.Button(
    description='Run All',
    disabled=False,
    button_style='',
    tooltip='Run all jobs')

runProgress = widgets.IntProgress(
    value=0, 
    min=0, 
    max=10, 
    step=1, 
    description='Progress:', 
    bar_style='', 
    orientation='horizontal')

#Build the input widgets
def buildInputWidgets():
    basic = VBox([inMrc, outMrc, pixelSize, patch, bFactor, voltage, gainFile, gpu])
    advanced1 = VBox([inTiff, fullSum, defectFile, iteration, tolerance, stack, binningFactor, initDose, frameDose, throw, trunc, group])
    advanced2 = VBox([processing, fmRef, tilt, rotGain, flipGain])

    advBoxLayout = Layout(display='flex',
                        flex_flow='row',
                        align_items='stretch',
                        border='none',
                        width='100%')
    advanced = Box(children=[advanced1, advanced2], layout=advBoxLayout)
    tab = widgets.Tab(children=[basic, advanced])
    tab.set_title(0, 'Basic')
    tab.set_title(1, 'Advanced')
    display(tab)

#buildNewJob - returns a dict containing input values    
def buildNewJob():
    newJob = {"inMrc":inMrc.value}
    newJob['outMrc']        = outMrc.value
    newJob['pixelSize']     = pixelSize.value   
    newJob['patch']         = patch.value
    newJob['bFactor']       = bFactor.value 
    newJob['voltage']       = voltage.value   
    newJob['gainFile']      = gainFile.value
    newJob['gpu']           = gpu.value
    newJob['inTiff']        = inTiff.value
    newJob['fullSum']       = fullSum.value
    newJob['defectFile']    = defectFile.value
 
    if  processing.value == "Single":
        newJob['processing'] = "0"
    if  processing.value == "Serial":
        newJob['processing'] = "1"
        
    newJob['iteration']     = iteration.value
    newJob['tolerance']     = tolerance.value   
    newJob['stack']         = stack.value
    newJob['binningFactor'] = binningFactor.value   
    newJob['initDose']      = initDose.value   
    newJob['frameDose']     = frameDose.value
    newJob['throw']         = throw.value   
    newJob['trunc']         = trunc.value   
    newJob['group']         = group.value   

    if  fmRef.value == "Central":
        newJob['fmRef']     = "1"
    if  fmRef.value == "First":
        newJob['fmRef']     = "0"

    newJob['tilt']          = tilt.value   

    if  rotGain.value == "No rotation - default":
        newJob['rotGain']   = "0"
    if  rotGain.value == "Rotate 90":
        newJob['rotGain']   = "1"
    if  rotGain.value == "Rotate 180":
        newJob['rotGain']   = "2"
    if  rotGain.value == "Rotate 270":
        newJob['rotGain']   = "3"

    if  flipGain.value == "No flip - default":
        newJob['flipGain']  = "0"
    if  flipGain.value == "upside down - horizontal axis":
        newJob['flipGain']  = "1"
    if  flipGain.value == "left right - vertical axis":
        newJob['flipGain']  = "2"

    return newJob

#buildArgumentsList - accepts a dict as input and 
#  returns a string containing completed arguments
#  to call MotionCor2
def buildArgumentsList(jobToProcess):
    args = ''
    
    if  jobToProcess['inMrc'] is not '':
        args += "-InMrc " + jobToProcess['inMrc']
    if  jobToProcess['inTiff'] is not '':
        args += " -InTiff " + jobToProcess['inTiff']
    if  jobToProcess['outMrc'] is not '':
        args += " -OutMrc " + jobToProcess['outMrc']
    if  jobToProcess['fullSum'] is not '':
        args += " -FullSum " + jobToProcess['fullSum']
    if  jobToProcess['defectFile'] is not '':
        args += " -DefectFile " + jobToProcess['defectFile']
    if  jobToProcess['gainFile'] is not '':
        args += " -Gain " + jobToProcess['gainFile']
    if  jobToProcess['patch'] is not '':
        args += " -Patch " + jobToProcess['patch']
    if  jobToProcess['tilt'] is not '':
        args += " -Tilt " + jobToProcess['tilt']
    if  jobToProcess['gpu'] is not '':
        args += " -Gpu " + jobToProcess['gpu']
    if  jobToProcess['processing'] is not '':
        args += " -Serial " + jobToProcess['processing']
    if  jobToProcess['fmRef'] is not '':
        args += " -FmRef " + jobToProcess['fmRef']
    if  jobToProcess['rotGain'] is not '':
        args += " -RotGain " + jobToProcess['rotGain']
    if  jobToProcess['flipGain'] is not '':
        args += " -FlipGain " + jobToProcess['flipGain']
    if  jobToProcess['iteration'] is not '':
        args += " -Iter " + str(jobToProcess['iteration'])
    if  jobToProcess['tolerance'] is not '':
        args += " -Tol " + str(jobToProcess['tolerance'])
    if  jobToProcess['bFactor'] is not '':
        args += " -Bft " + str(jobToProcess['bFactor'])
    if  jobToProcess['stack'] is not '':
        args += " -StackZ " + str(jobToProcess['stack'])
    if  jobToProcess['binningFactor'] is not '':
        args += " -FtBin " + str(jobToProcess['binningFactor'])
    if  jobToProcess['initDose'] is not '':
        args += " -InitDose " + str(jobToProcess['initDose'])
    if  jobToProcess['frameDose'] is not '':
        args += " -FmDose " + str(jobToProcess['frameDose'])
    if  jobToProcess['pixelSize'] is not '':
        args += " -PixSize " + str(jobToProcess['pixelSize'])
    if  jobToProcess['voltage'] is not '':
        args += " -kV " + str(jobToProcess['voltage'])
    if  jobToProcess['throw'] is not '':
        args += " -Throw " + str(jobToProcess['throw'])
    if  jobToProcess['trunc'] is not '':
        args += " -Trunc " + str(jobToProcess['trunc'])
    if  jobToProcess['group'] is not '':
        args += " -Group " + str(jobToProcess['group'])
    
    return args

# saveOutput - write to disk the stdout, stderr and args
#   values used in calling motionCor2.
def saveOutput(folder, runOutput, runArgs, runStderr):
    outputFilename = "motionCor2-output.txt"
    argsFilename   = "motionCor2-arguments.txt"
    errorFilename  = "motionCor2-error.txt"
    
    debug.value = debug.value + folder + "\n"
    debug.value = debug.value + runOutput + "\n"
    debug.value = debug.value + runArgs + "\n"
    debug.value = debug.value + runStderr + "\n"
    
    fOutput = open(folder + outputFilename, "w")
    fOutput.write(runOutput)
    fOutput.close()
    
    fArgs = open(folder + argsFilename, "w")
    fArgs.write(runArgs)
    fArgs.close()
    
    fError = open(folder + errorFilename, "w")
    fError.write(runStderr)
    fError.close()

def call_motioncor2(jobToRun):
    
    #Clear output from previous run
    stdout.value = ''
    stderr.value = ''
    args.value = ''
    
    if  jobToRun is not None:
        #clear stdout, args , stderr
        stdout.value = ""
        args.value = ""
        
        #Calling motioncor2
        #Note: shell=True. There are security implications for this. This was enabled as the arguments were not
        #being passed in to motioncor2.

        #try:
        #response = subp.run("motioncor2 " + buildArgumentsList(), shell=True, stdout=subp.PIPE, stderr=subp.PIPE)
        job = buildArgumentsList(jobToRun)
        response = subp.Popen("motioncor2 " + job, shell=True, stdout=subp.PIPE, stderr=subp.PIPE)
        #except sp.TimeoutExpired:
        #    stderr.value = 'Call timed out!'
        #except sp.SubprocessError:
        #     stderr.value = 'Subprocess Error!'

        while True:
            output = response.stdout.readline().decode()
            if  output == '' and response.poll() is not None:
                break
            if  output:
                stdout.value = stdout.value + output

        #stderr.value = response.stderr
        args.value = job

        #saveOutput(folder, stdout, args, stderr)
        debug.value = debug.value + "Before saveOutput\n"
        #debug.value = debug.value + "outMrc: " + jobToRun["outMrc"] + "\n"
        #debug.value = debug.value + "stdout: " + stdout.value + "\n"
        #debug.value = debug.value + "args: " + args.value + "\n"
        #debug.value = debug.value + "stderr: " + stderr.value + "\n"
        saveOutput(jobToRun["outMrc"], stdout.value, args.value, stderr.value)
        debug.value = debug.value + "After saveOutput\n"
        

def runSingleJob(b):
    call_motioncor2(buildNewJob())        
        
def buildOutputWidgets():
    runMotionCor2 = widgets.Button(
        description='Run',
        disabled=False,
        button_style='',
        tooltip='Run motioncor2',
        icon='check')

    runMotionCor2.on_click(runSingleJob)

    display(runMotionCor2)
    organiseOutputs = VBox([stdout, stderr, args])
    display(organiseOutputs)

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
        if  (str(selectedJobsList[i]).startswith('Job#') == False):
            listedJobsList.remove(selectedJobsList[i])
    #update
    jobsList.options = listedJobsList

def saveJobs(b):
    global savedJobs
    listedJobs = jobsList.options
    savedJobs = list(listedJobs)
    #store the variable in the IPython database.
    #%store savedJobs

def loadJobs(b):
    global savedJobs
    #restore all saved variables from the IPython database.
    #%store -r savedJobs
    #update the screen
    jobsList.options = savedJobs

def runAllJobs(b):
    #obtain the listedJobs
    listedJobs = jobsList.options
    listedJobsList = list(listedJobs)

    runProgress.max = len(listedJobsList)
    
    #Run each job, but not the Header row.
    for i in range(len(listedJobsList)):
        #setting progress bar to show job has started running.
        if  (str(listedJobsList[i]).startswith('Job#') == True):
            runProgress.value = i+1    

        if  (str(listedJobsList[i]).startswith('Job#') == False):
            call_motioncor2(listedJobsList[i])
            runProgress.value = i+1    
    
def buildJobsWidgets():
    buttons = HBox([addButton, deleteButton, saveButton, loadButton, runButton, runProgress])
    selectableTable = VBox([jobsList, buttons])

    #Add fuctions to buttons.
    addButton.on_click(addJob)
    deleteButton.on_click(deleteJob)
    saveButton.on_click(saveJobs)
    loadButton.on_click(loadJobs)
    runButton.on_click(runAllJobs)

    display(selectableTable)
