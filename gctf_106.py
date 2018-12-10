import os
import glob
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Box, Label, Layout

#Gctf  input fields and functions to execute jobs

class contrastTransFunc:
    #Settings:
    program = 'Gctf-v1.06_sm_20_cu8.0_x86_64'
    jobPrefix = 'ctf'
    header = [("Job# | inMrc | outMrc | spherAberration | voltage | ampContrast | pixelSize | gpu | enablePhasePlate |phaseShiftLow | phaseShiftHigh | phaseShiftStep | phaseShiftTarget | estAstigmation | boxSize | resLowest | resHighest | defocusLow | defocusHigh | defocusStep | detectorSize | bfac | doEquiPhaseAvg | oversampFactorEPA | overlap | convsize | doHighResRefinement | highResRefinement_lowRes | highResRefinement_highRes | highResRefinement_bfac | bfacEstLow | bfacEstHigh | frameCtfRefinement | frameCtfAverage | frameCtfFitting | frameCtfAverageType | localDefocusRefinement | localDefocusRadius | localDefocusAveType | localDefocusBoxsize | localDefocusOverlap | localDefocusLowRes | localDefocusHighRes | localDefocusAstm | userCtfInputRefine | userCtfDefocusU | userCtfDefocusV | userCtfDefocusA | userCtfBfactor | userCtfDefocusUError | userCtfDefocusVError | userCtfDefocusAError | userCtfBfactorError | doPhaseFlip | doValidation | ctfDiag_lowRes | ctfDiag_highRes | ctfDiag_Bfact | inputCTFstar | boxSuffix | outputCTFstar | logSuffix | writePowerSpectrumFile | plotResRing | doUnfinished | skipMRCcheck | skipGPUcheck ")]
    starFileName  = 'micrographs_ctf.star'
    
    #style and Layout
    styleBasic    = {'description_width': '160px'}
    styleAdvanced = {'description_width': '200px'}
    basicLayout   = Layout(width='60%')
    advLayout     = Layout(width='40%')
    errorLayout   = Layout(width='60%', border='2px solid red')
    
    #Input fields for Gctf
    jobNumber = widgets.Text(
        description='Job no: ',
        disabled=True,
        style=styleBasic,
        layout=basicLayout)

    inMrc = widgets.Text(
        value='',
        placeholder='path for input mrc file or folder containing mrc files',
        description='Input: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    outMrc = widgets.Text(
        value='',
        placeholder='path for saving job output, errors and arguments',
        description='Output: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    spherAberration = widgets.FloatSlider(
        value=2.7,
        min=0,
        max=10,
        step=0.1,
        description='Spherical aberration (mm): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleBasic,
        layout=basicLayout)

    voltage = widgets.IntText(
        value=300,
        description='Voltage (kV): ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    ampContrast = widgets.FloatSlider(
        value=0.1,
        min=0,
        max=0.5,
        step=0.01,
        description='Amplitutde contrast: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.2f',
        style=styleBasic,
        layout=basicLayout)

    pixelSize = widgets.FloatSlider(
        value=1.34,
        min=0,
        max=5.0,
        step=0.01,
        description='Pixel size (A): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.2f',
        style=styleBasic,
        layout=basicLayout)

    gpu = widgets.Text(
        value='',
        placeholder='indicate the GPUs to use',
        description='GPU usage: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    ##Phase plate options
    phaseShiftLow = widgets.FloatSlider(
        value=0.0,
        min=0.0,
        max=360,
        step=0.1,
        description='Phase shift - lowest (degrees): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.01f',
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftHigh = widgets.FloatSlider(
        value=180.0,
        min=0.0,
        max=360,
        step=0.1,
        description='Phase shift - highest (degrees): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.01f',
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftStep = widgets.FloatSlider(
        value=10.0,
        min=0.0,
        max=10,
        step=0.1,
        description='Phase shift - step: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)

    #default to Resolution limit to ensure Ctf Max Resolution value is calculated.
    phaseShiftTarget = widgets.Select(
        options=[('CCC', '1'), ('Resolution limit', '2')],
        description='Phase shift target ',
        value='2',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftTargetMulti = widgets.SelectMultiple(
        options=[('CCC', '1'), ('Resolution limit', '2')],
        description='Phase shift target ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftTargetMultiButton = widgets.Button(
        description='Add jobs',
        disabled=False,
        button_style='',
        tooltip='Add multiple jobs',
        icon='check')    

    ##Additional options
    estAstigmation = widgets.IntText(
        value=1000,
        description='Est astigmation (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    boxSize = widgets.IntText(
        value=1024,
        description='Box size (pixel): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    resLowest = widgets.IntText(
        value=50,
        description='Lowest resolution (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    resHighest = widgets.IntText(
        value=4,
        description='Highest resolution (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusLow = widgets.IntText(
        value=5000,
        description='Lowest defocus (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusHigh = widgets.IntText(
        value=90000,
        description='Highest defocus (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusStep = widgets.IntText(
        value=500,
        description='Defocus step (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    detectorSize = widgets.FloatText(
        value=14.0,
        description='Detector size: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    bfac = widgets.IntSlider(
        value=150,
        min=0,
        max=500,
        step=1,
        description='Bfactor (A^2): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    ##Advanced Additional options
    doEquiPhaseAvg = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='Do equi phase average: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    oversampFactorEPA = widgets.IntSlider(
        value=4,
        min=0,
        max=20,
        step=1,
        description='EPA - oversamp factor: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    overlap = widgets.FloatSlider(
        value=0.5,
        min=0,
        max=1,
        step=0.1,
        description='Overlapping factor: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)

    convsize = widgets.IntSlider(
        value=85,
        min=0,
        max=200,
        step=1,
        description='Smoothing box size: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    #High resolution refinement options
    doHighResRefinement = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='High res refinement: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    highResRefinement_lowRes = widgets.FloatText(
        value=15.0,
        description='High res refine-low res(A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    highResRefinement_highRes = widgets.FloatText(
        value=4.0,
        description='High res refine-high res(A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    highResRefinement_bfac = widgets.IntText(
        value=50,
        description='High res refine-bfac(A^2): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    #Bfactor estimation options
    bfacEstLow = widgets.FloatSlider(
        value=15.0,
        min=0,
        max=50,
        step=0.1,
        description='Bfact est. - low res: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)
    
    bfacEstHigh = widgets.FloatSlider(
        value=6.0,
        min=0,
        max=50,
        step=0.1,
        description='Bfact est. - high res: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)
    
    #Movies options to calc frame defocuses
    frameCtfRefinement = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='Calc movie frame defocus: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)
    
    frameCtfAverage = widgets.IntText(
        value=1,
        description='CTF refinement - avg # frames:',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    frameCtfFitting = widgets.Select(
        options=[('No', 0), ('Linear', 1)],
        description='Frame defocus fitting: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)
    
    frameCtfAverageType = widgets.Select(
        options=[('Coherent', 0), ('Incoherent', 1)],
        description='Frame defocus avg type: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)
    
    #Local options to calc particle defocuses
    localDefocusRefinement = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='Calc particle defocus: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)
    
    localDefocusRadius = widgets.IntText(
        value=1024,
        description='Local radius: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    localDefocusAveType = widgets.Select(
        options=[('Equal', 0), ('Distance', 1), ('Gaussian - dist & freq', 2)],
        description='Particle average type: ',
        value=2,
        disabled=False,
        rows=3,
        style=styleAdvanced,
        layout=advLayout)
    
    localDefocusBoxsize = widgets.IntText(
        value=512,
        description='Box size: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    localDefocusOverlap = widgets.FloatSlider(
        value=0.5,
        min=0,
        max=1,
        step=0.1,
        description='Overlap factor: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)
    
    localDefocusLowRes = widgets.IntText(
        value=15,
        description='Lowest resolution (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    localDefocusHighRes = widgets.IntText(
        value=5,
        description='Highest resolution (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    localDefocusAstm = widgets.Select(
        options=[('Only refine Z-height', 0), ('Refine local Astigmatism', 1)],
        description='Refine local Astigmatism: ',
        value=0,
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    ##CTF refinement options
    userCtfInputRefine = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='User CTF refinement: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)
    
    userCtfDefocusU = widgets.FloatText(
        value=20000.0,
        description='Initial defocus U: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    userCtfDefocusV = widgets.FloatText(
        value=20000.0,
        description='Initital defocus V: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    userCtfDefocusA = widgets.FloatText(
        value=0.0,
        description='Initial defocus angle: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    userCtfBfactor = widgets.FloatText(
        value=200.0,
        description='Initial bfactor: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    userCtfDefocusUError = widgets.FloatText(
        value=500.0,
        description='Initial defocus U est. error: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    userCtfDefocusVError = widgets.FloatText(
        value=500.0,
        description='Initial defocus V est. error: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    userCtfDefocusAError = widgets.FloatText(
        value=15.0,
        description='Initial defocus angle est. error: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    userCtfBfactorError = widgets.FloatText(
        value=50.0,
        description='Initial Bfactor est. error: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ##Correction options
    doPhaseFlip = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='Flip phase ?: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)
    
    ##Validation options
    doValidation = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='Validate CTF determination ?: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)
    
    ##CTF output file options
    ctfDiag_lowRes =  widgets.FloatText(
        value=100.0,
        description='CTF diagnosis-low res: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ctfDiag_highRes = widgets.FloatText(
        value=2.8,
        description='CTF diagnosis-high res: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ctfDiag_Bfact = widgets.IntText(
        value=50,
        description='CTF diagnosis - Bfactor: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ##IO options
    inputCTFstar = widgets.Text(
        value='',
        placeholder='',
        description='Input STAR file:',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    boxSuffix = widgets.Text(
        value='',
        placeholder='Input .box/.star in EMAN/Relion box format, used for local refinement',
        description='Input .box/.star file:',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    outputCTFstar = widgets.Text(
        value='',
        placeholder='Use "NULL" to skip',
        description='Output STAR file:',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    logSuffix = widgets.Text(
        value='',
        placeholder='_gctf.log',
        description='Log file suffix:',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)
    
    writePowerSpectrumFile = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        value=1,
        description='Write diag power spectrum scale?: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)
    
    plotResRing = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        value=1,
        description='Plot est. resolution ring?: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    doUnfinished  = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='Continue processing: ',
        value=1,
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    skipMRCcheck = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='Skip MRC check: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    skipGPUcheck = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='Skip GPU check: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    runButton = widgets.Button(
        description='Run',
        disabled=False,
        button_style='',
        tooltip='Run program',
        icon='check')

    enablePhasePlate = widgets.RadioButtons(
        options=['Disable', 'Enable'], 
        description='Enable phase plate processing:', 
        disabled=False,
        style=styleAdvanced, 
        layout=advLayout)

    #
    ## Job Maintenance fields
    #  --start--
    existingJobs = []
    jobCounter = 1
    
    #screen fields
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

    selectButton = widgets.Button(
        description='Select', 
        disabled=False, 
        button_style='', 
        tooltip='Select job for editing.')

    updateButton = widgets.Button(
        description='Update',
        disabled=False,
        button_style='',
        tooltip='Update job.')

    runAllButton = widgets.Button(
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
    #  --end--
    ## Job Maintenance fields
    #      

    errorText = widgets.Textarea(
        description='',
        description_tooltip='Error messages',
        placeholder='Errors',
        disabled=True,
        rows=1,
        style=styleBasic,
        layout=basicLayout)    
    
    ##Debug assistance
    debug = widgets.Output(
        style=styleBasic,
        layout=Layout(width='90%')) 

    debugText = widgets.Textarea(
        description='Debugging:',
        description_tooltip='Standard output',
        disabled=False,
        rows=10,
        style=styleBasic,
        layout=Layout(width='90%'))  
    
    # __init__() - initialise the class jobMaintenance
    #    Arguments:
    #        callProgramFunc - the function for executing the program
    #        showDebug - display debug fields
    #    
    def __init__(self, callProgramFunc, showDebug):
        self.callProgram = callProgramFunc
        self.showDebug = showDebug
    
    # runSingleJob() - execute a single job
    #
    @debug.capture(clear_output=True)
    def runSingleJob(self, target):
        self.runProgress.max = 2
        self.runProgress.value = 1        
        self.callProgram(self.program, self.buildArgumentsList(self.buildJob('', self.jobNumber)), self.outMrc.value)
        self.runProgress.value = self.runProgress.max
    
    #Multi value field processing support
    # addPhaseShiftTargetJobs() - add new jobs for all 'phaseShiftTarget' values entered
    #
    @debug.capture(clear_output=True)
    def addPhaseShiftTargetJobs(self, target):
        self.addJobs("phaseShiftTarget", self.phaseShiftTargetMulti.value)
   
    # buildInputWidgets() - write all the Gctf input fields to the screen.
    #
    @debug.capture(clear_output=True)
    def buildInputWidgets(self):
        #linking button on_click to function    
        self.runButton.on_click(self.runSingleJob)
        self.phaseShiftTargetMultiButton.on_click(self.addPhaseShiftTargetJobs)
        
        phaseShiftTargetInputs = HBox([self.phaseShiftTarget, self.phaseShiftTargetMulti, self.phaseShiftTargetMultiButton])    

        normal     = VBox([self.jobNumber, self.inMrc, self.outMrc, self.spherAberration, self.voltage, self.ampContrast,
                           self.pixelSize, self.gpu])
        phasePlate = VBox([self.enablePhasePlate, self.phaseShiftLow, self.phaseShiftHigh, self.phaseShiftStep, phaseShiftTargetInputs])
        additional = VBox([self.detectorSize, self.defocusLow, self.defocusHigh, self.defocusStep, self.estAstigmation, 
                           self.bfac, self.resLowest, self.resHighest, self.boxSize])
        
        advanced   = VBox([self.doEquiPhaseAvg, self.oversampFactorEPA, self.overlap, self.convsize, 
                           self.doHighResRefinement, self.highResRefinement_lowRes, self.highResRefinement_highRes, 
                           self.highResRefinement_bfac, self.bfacEstLow, self.bfacEstHigh])
        defocus    = VBox([self.frameCtfRefinement, self.frameCtfAverage, self.frameCtfFitting, self.frameCtfAverageType,
                           self.localDefocusRefinement, self.localDefocusRadius, self.localDefocusAveType, self.localDefocusBoxsize,
                           self.localDefocusOverlap, self.localDefocusLowRes, self.localDefocusHighRes, self.localDefocusAstm])
        ctfRefine  = VBox([self.userCtfInputRefine, self.userCtfDefocusU, self.userCtfDefocusV, self.userCtfDefocusA,
                           self.userCtfBfactor, self.userCtfDefocusUError, self.userCtfDefocusVError, self.userCtfDefocusAError, 
                           self.userCtfBfactorError])
        ctfIO      = VBox([self.doPhaseFlip, self.doValidation, self.ctfDiag_lowRes, self.ctfDiag_highRes, self.ctfDiag_Bfact,
                           self.inputCTFstar, self.boxSuffix, self.outputCTFstar, self.logSuffix, self.writePowerSpectrumFile,
                           self.plotResRing, self.doUnfinished, self.skipMRCcheck, self.skipGPUcheck])

        tab = widgets.Tab(children=[normal, phasePlate, additional, advanced, defocus, ctfRefine, ctfIO])
        tab.set_title(0, 'Normal')
        tab.set_title(1, 'Phase Plate Options')
        tab.set_title(2, 'Additional Options')
        tab.set_title(3, 'Advanced Additional')
        tab.set_title(4, 'Defocus Frame/Local')
        tab.set_title(5, 'CTF Refinement')
        tab.set_title(6, 'CTF and IO')        

        if  self.showDebug:
            return VBox([self.debug, self.debugText, tab, self.runButton])
        else:
            return VBox([tab, self.runButton])

    # buildNewJobs() - construct a job containing all arguments.
    #    Arguments:
    #        fieldName - the field name for which a range of values has been specified
    #        values - a range of values for the specified 'fieldName'
    #   Return:
    #     A) When 'fieldName' and 'values' are populated:
    #        - list of dicts representing jobs
    #     B) When 'fieldName' and 'values' are not populated:
    #        - dict representing a single job
    #
    @debug.capture(clear_output=True)
    def buildNewJobs(self, fieldName, values):
        fieldList = []
        jobList = []

        #Building a single job
        if  not fieldName and not values:
            newJob = self.buildJob('', self.jobCounter)
            self.jobCounter = self.jobCounter + 1
            return newJob
        
        #Building multiple jobs
        if  fieldName == 'phaseShiftTarget':
            fieldList = list(values)

        for i in range(len(fieldList)):
            fieldCleaned = fieldList[i].strip()
        
            if  fieldCleaned:
                if  fieldName == 'phaseShiftTarget':
                    newJob = self.buildJob(fieldCleaned, self.jobCounter)

                self.jobCounter = self.jobCounter + 1
                jobList.append(newJob)                    

        return jobList

    # buildJob() - construct a single job containing all arguments.
    #    Arguments:
    #        phaseShiftTargetValue - use the phaseShiftTarget if specified, otherwise use screen value
    #        jobNo - the next job number to use
    #    Return:
    #        dict containing all arguments.
    #
    @debug.capture(clear_output=True)
    def buildJob(self, phaseShiftTargetValue, jobNo):
        
        jobNoWithPrefix = self.jobPrefix + str(jobNo)
        if  jobNo:
            newJob = {'jobNumber':jobNoWithPrefix}
        else:
            newJob = {'jobNumber':self.jobNumber.value}

        newJob['inMrc']                     = self.inMrc.value
        newJob['outMrc']                    = self.outMrc.value
        newJob['spherAberration']           = self.spherAberration.value
        newJob['voltage']                   = self.voltage.value
        newJob['ampContrast']               = self.ampContrast.value   
        newJob['pixelSize']                 = self.pixelSize.value
        newJob['gpu']                       = self.gpu.value 
        
        newJob['enablePhasePlate']          = self.enablePhasePlate.value
        newJob['phaseShiftLow']             = self.phaseShiftLow.value
        newJob['phaseShiftHigh']            = self.phaseShiftHigh.value
        newJob['phaseShiftStep']            = self.phaseShiftStep.value

        if  phaseShiftTargetValue:
            newJob['phaseShiftTarget']      = phaseShiftTargetValue
        else:    
            newJob['phaseShiftTarget']      = self.phaseShiftTarget.value

        newJob['estAstigmation']            = self.estAstigmation.value   
        newJob['boxSize']                   = self.boxSize.value
        newJob['resLowest']                 = self.resLowest.value   
        newJob['resHighest']                = self.resHighest.value   
        newJob['defocusLow']                = self.defocusLow.value   
        newJob['defocusHigh']               = self.defocusHigh.value   
        newJob['defocusStep']               = self.defocusStep.value
        newJob['detectorSize']              = self.detectorSize.value
        newJob['bfac']                      = self.bfac.value   
        newJob['doEquiPhaseAvg']            = self.doEquiPhaseAvg.value
        newJob['oversampFactorEPA']         = self.oversampFactorEPA.value   
        newJob['overlap']                   = self.overlap.value   
        newJob['convsize']                  = self.convsize.value   
        newJob['doHighResRefinement']       = self.doHighResRefinement.value
        newJob['highResRefinement_lowRes']  = self.highResRefinement_lowRes.value   
        newJob['highResRefinement_highRes'] = self.highResRefinement_highRes.value   
        newJob['highResRefinement_bfac']    = self.highResRefinement_bfac.value   
        newJob['bfacEstLow']                = self.bfacEstLow.value
        newJob['bfacEstHigh']               = self.bfacEstHigh.value
        newJob['frameCtfRefinement']        = self.frameCtfRefinement.value
        newJob['frameCtfAverage']           = self.frameCtfAverage.value
        newJob['frameCtfFitting']           = self.frameCtfFitting.value
        newJob['frameCtfAverageType']       = self.frameCtfAverageType.value
        newJob['localDefocusRefinement']    = self.localDefocusRefinement.value
        newJob['localDefocusRadius']        = self.localDefocusRadius.value
        newJob['localDefocusAveType']       = self.localDefocusAveType.value
        newJob['localDefocusBoxsize']       = self.localDefocusBoxsize.value
        newJob['localDefocusOverlap']       = self.localDefocusOverlap.value
        newJob['localDefocusLowRes']        = self.localDefocusLowRes.value
        newJob['localDefocusHighRes']       = self.localDefocusHighRes.value
        newJob['localDefocusAstm']          = self.localDefocusAstm.value
        newJob['userCtfInputRefine']        = self.userCtfInputRefine.value
        newJob['userCtfDefocusU']           = self.userCtfDefocusU.value
        newJob['userCtfDefocusV']           = self.userCtfDefocusV.value
        newJob['userCtfDefocusA']           = self.userCtfDefocusA.value
        newJob['userCtfBfactor']            = self.userCtfBfactor.value
        newJob['userCtfDefocusUError']      = self.userCtfDefocusUError.value
        newJob['userCtfDefocusVError']      = self.userCtfDefocusVError.value
        newJob['userCtfDefocusAError']      = self.userCtfDefocusAError.value
        newJob['userCtfBfactorError']       = self.userCtfBfactorError.value
        newJob['doPhaseFlip']               = self.doPhaseFlip.value
        newJob['doValidation']              = self.doValidation.value
        newJob['ctfDiag_lowRes']            = self.ctfDiag_lowRes.value   
        newJob['ctfDiag_highRes']           = self.ctfDiag_highRes.value   
        newJob['ctfDiag_Bfact']             = self.ctfDiag_Bfact.value   
        newJob['inputCTFstar']              = self.inputCTFstar.value 
        newJob['boxSuffix']                 = self.boxSuffix.value
        newJob['outputCTFstar']             = self.outputCTFstar.value   
        newJob['logSuffix']                 = self.logSuffix.value
        newJob['writePowerSpectrumFile']    = self.writePowerSpectrumFile.value
        newJob['plotResRing']               = self.plotResRing.value
        newJob['doUnfinished']              = self.doUnfinished.value
        newJob['skipMRCcheck']              = self.skipMRCcheck.value
        newJob['skipGPUcheck']              = self.skipGPUcheck.value
        return newJob

    # updateScreenFields() - updates screen fields using supplied dict.
    #    Arguments:
    #        selectedJob - a dict containing all screen values.
    #
    @debug.capture(clear_output=True)
    def updateScreenFields(self, selectedJob):
        
        self.jobNumber.value                 = selectedJob['jobNumber']
        self.inMrc.value                     = selectedJob['inMrc']
        self.outMrc.value                    = selectedJob['outMrc']
        self.spherAberration.value           = selectedJob['spherAberration']
        self.voltage.value                   = selectedJob['voltage']
        self.ampContrast.value               = selectedJob['ampContrast']
        self.pixelSize.value                 = selectedJob['pixelSize']
        self.gpu.value                       = selectedJob['gpu']
        self.enablePhasePlate.value          = selectedJob['enablePhasePlate']
        self.phaseShiftLow.value             = selectedJob['phaseShiftLow']
        self.phaseShiftHigh.value            = selectedJob['phaseShiftHigh']
        self.phaseShiftStep.value            = selectedJob['phaseShiftStep']
        self.phaseShiftTarget.value          = selectedJob['phaseShiftTarget']
        self.estAstigmation.value            = selectedJob['estAstigmation']
        self.boxSize.value                   = selectedJob['boxSize']
        self.resLowest.value                 = selectedJob['resLowest']
        self.resHighest.value                = selectedJob['resHighest']
        self.defocusLow.value                = selectedJob['defocusLow']
        self.defocusHigh.value               = selectedJob['defocusHigh']
        self.defocusStep.value               = selectedJob['defocusStep']
        self.detectorSize.value              = selectedJob['detectorSize']
        self.bfac.value                      = selectedJob['bfac']
        self.doEquiPhaseAvg.value            = selectedJob['doEquiPhaseAvg']
        self.oversampFactorEPA.value         = selectedJob['oversampFactorEPA']
        self.overlap.value                   = selectedJob['overlap']
        self.convsize.value                  = selectedJob['convsize']
        self.doHighResRefinement.value       = selectedJob['doHighResRefinement']
        self.highResRefinement_lowRes.value  = selectedJob['highResRefinement_lowRes']
        self.highResRefinement_highRes.value = selectedJob['highResRefinement_highRes']
        self.highResRefinement_bfac.value    = selectedJob['highResRefinement_bfac']
        self.bfacEstLow.value                = selectedJob['bfacEstLow']                
        self.bfacEstHigh.value               = selectedJob['bfacEstHigh']               
        self.frameCtfRefinement.value        = selectedJob['frameCtfRefinement']
        self.frameCtfAverage.value           = selectedJob['frameCtfAverage']            
        self.frameCtfFitting.value           = selectedJob['frameCtfFitting']           
        self.frameCtfAverageType.value       = selectedJob['frameCtfAverageType']
        self.localDefocusRefinement.value    = selectedJob['localDefocusRefinement']
        self.localDefocusRadius.value        = selectedJob['localDefocusRadius']
        self.localDefocusAveType.value       = selectedJob['localDefocusAveType']  
        self.localDefocusBoxsize.value       = selectedJob['localDefocusBoxsize']  
        self.localDefocusOverlap.value       = selectedJob['localDefocusOverlap']   
        self.localDefocusLowRes.value        = selectedJob['localDefocusLowRes']  
        self.localDefocusHighRes.value       = selectedJob['localDefocusHighRes']       
        self.localDefocusAstm.value          = selectedJob['localDefocusAstm'] 
        self.userCtfInputRefine.value        = selectedJob['userCtfInputRefine']
        self.userCtfDefocusU.value           = selectedJob['userCtfDefocusU']  
        self.userCtfDefocusV.value           = selectedJob['userCtfDefocusV']   
        self.userCtfDefocusA.value           = selectedJob['userCtfDefocusA'] 
        self.userCtfBfactor.value            = selectedJob['userCtfBfactor']    
        self.userCtfDefocusUError.value      = selectedJob['userCtfDefocusUError']      
        self.userCtfDefocusVError.value      = selectedJob['userCtfDefocusVError'] 
        self.userCtfDefocusAError.value      = selectedJob['userCtfDefocusAError'] 
        self.userCtfBfactorError.value       = selectedJob['userCtfBfactorError']   
        self.doPhaseFlip.value               = selectedJob['doPhaseFlip']   
        self.doValidation.value              = selectedJob['doValidation']
        self.ctfDiag_lowRes.value            = selectedJob['ctfDiag_lowRes']
        self.ctfDiag_highRes.value           = selectedJob['ctfDiag_highRes']
        self.ctfDiag_Bfact.value             = selectedJob['ctfDiag_Bfact']
        self.inputCTFstar.value              = selectedJob['inputCTFstar']
        self.boxSuffix.value                 = selectedJob['boxSuffix']
        self.outputCTFstar.value             = selectedJob['outputCTFstar']
        self.logSuffix.value                 = selectedJob['logSuffix']
        self.writePowerSpectrumFile.value    = selectedJob['writePowerSpectrumFile']
        self.plotResRing.value               = selectedJob['plotResRing']
        self.doUnfinished.value              = selectedJob['doUnfinished']
        self.skipMRCcheck.value              = selectedJob['skipMRCcheck']
        self.skipGPUcheck.value              = selectedJob['skipGPUcheck']
        
    # buildArgumentsList() - builds a string of arguments for calling Motion Correction.
    #    Arguments:
    #        jobToProcess - a dict containing all screen values.
    #
    @debug.capture(clear_output=True)
    def buildArgumentsList(self, jobToProcess):
        args = ''
        
        if  jobToProcess['spherAberration']:
            args += " --cs " + str(jobToProcess['spherAberration'])
        if  jobToProcess['voltage']:
            args += " --kv " + str(jobToProcess['voltage'])
        if  jobToProcess['ampContrast']:
            args += " --ac " + str(jobToProcess['ampContrast'])
        if  jobToProcess['pixelSize']:
            args += " --apix " + str(jobToProcess['pixelSize'])
        if  jobToProcess['gpu']:
            args += " --gid " + jobToProcess['gpu']            

        if  jobToProcess['enablePhasePlate'] == 'Enable':
            if  jobToProcess['phaseShiftLow']:
                args += " --phase_shift_L " + str(jobToProcess['phaseShiftLow'])
            if  jobToProcess['phaseShiftHigh']:
                args += " --phase_shift_H " + str(jobToProcess['phaseShiftHigh'])
            if  jobToProcess['phaseShiftStep']:
                args += " --phase_shift_S " + str(jobToProcess['phaseShiftStep'])
            if  jobToProcess['phaseShiftTarget']:
                args += " --phase_shift_T " + str(jobToProcess['phaseShiftTarget'])
                
        if  jobToProcess['estAstigmation']:
            args += " --astm " + str(jobToProcess['estAstigmation'])
        if  jobToProcess['boxSize']:
            args += " --boxsize " + str(jobToProcess['boxSize'])
        if  jobToProcess['resLowest']:
            args += " --resL " + str(jobToProcess['resLowest'])
        if  jobToProcess['resHighest']:
            args += " --resH " + str(jobToProcess['resHighest'])
        if  jobToProcess['defocusLow']:
            args += " --defL " + str(jobToProcess['defocusLow'])
        if  jobToProcess['defocusHigh']:
            args += " --defH " + str(jobToProcess['defocusHigh'])
        if  jobToProcess['defocusStep']:
            args += " --defS " + str(jobToProcess['defocusStep'])
        if  jobToProcess['detectorSize']:
            args += " --dstep " + str(jobToProcess['detectorSize'])
        if  jobToProcess['bfac']:
            args += " --bfac " + str(jobToProcess['bfac'])
        if  jobToProcess['doEquiPhaseAvg']:
            args += " --do_EPA " + str(jobToProcess['doEquiPhaseAvg'])
        if  jobToProcess['oversampFactorEPA']:
            args += " --EPA_oversmp " + str(jobToProcess['oversampFactorEPA'])
        if  jobToProcess['overlap']:
            args += " --overlap " + str(jobToProcess['overlap'])
        if  jobToProcess['convsize']:
            args += " --convsize " + str(jobToProcess['convsize'])
        if  jobToProcess['doHighResRefinement']:
            args += " --do_Hres_ref " + str(jobToProcess['doHighResRefinement'])
        if  jobToProcess['highResRefinement_lowRes']:
            args += " --Href_resL " + str(jobToProcess['highResRefinement_lowRes'])
        if  jobToProcess['highResRefinement_highRes']:
            args += " --Href_resH " + str(jobToProcess['highResRefinement_highRes'])
        if  jobToProcess['highResRefinement_bfac']:
            args += " --Href_bfac " + str(jobToProcess['highResRefinement_bfac'])

        if  jobToProcess['bfacEstLow']:
            args += " --B_resL " + str(jobToProcess['bfacEstLow'])
        if  jobToProcess['bfacEstHigh']:
            args += " --B_resH " + str(jobToProcess['bfacEstHigh'])    
            
        #Only add aguments if frameCtfRefinement == 'Yes'    
        if  jobToProcess['frameCtfRefinement'] == '1':
            args += " --do_mdef_refine " + str(jobToProcess['frameCtfRefinement'])            
            if  jobToProcess['frameCtfAverage']:
                args += " --mdef_aveN " + str(jobToProcess['frameCtfAverage'])            
            if  jobToProcess['frameCtfFitting']:
                args += " --mdef_fit " + str(jobToProcess['frameCtfFitting'])            
            if  jobToProcess['frameCtfAverageType']:
                args += " --mdef_ave_type " + str(jobToProcess['frameCtfAverageType'])
                
        #Only add arguments if localDefocusRefinement == 'Yes'
        if  jobToProcess['localDefocusRefinement'] == '1':
            args += " --do_local_refine " + str(jobToProcess['localDefocusRefinement'])            
            if  jobToProcess['localDefocusRadius']:
                args += " --local_radius " + str(jobToProcess['localDefocusRadius'])            
            if  jobToProcess['localDefocusAveType']:
                args += " --local_avetype " + str(jobToProcess['localDefocusAveType'])            
            if  jobToProcess['localDefocusBoxsize']:
                args += " --local_boxsize " + str(jobToProcess['localDefocusBoxsize'])            
            if  jobToProcess['localDefocusOverlap']:
                args += " --local_overlap " + str(jobToProcess['localDefocusOverlap'])            
            if  jobToProcess['localDefocusLowRes']:
                args += " --local_resL " + str(jobToProcess['localDefocusLowRes'])            
            if  jobToProcess['localDefocusHighRes']:
                args += " --local_resH " + str(jobToProcess['localDefocusHighRes'])            
            if  jobToProcess['localDefocusAstm']:
                args += " --refine_local_astm " + str(jobToProcess['localDefocusAstm'])            

        if  jobToProcess['userCtfInputRefine']:
            args += " --refine_intput_ctf " + str(jobToProcess['userCtfInputRefine'])            
        if  jobToProcess['userCtfDefocusU']:
            args += " --defU_init " + str(jobToProcess['userCtfDefocusU'])            
        if  jobToProcess['userCtfDefocusV']:
            args += " --defV_init " + str(jobToProcess['userCtfDefocusV'])            
        if  jobToProcess['userCtfDefocusA']:
            args += " --defA_init " + str(jobToProcess['userCtfDefocusA'])            
        if  jobToProcess['userCtfBfactor']:
            args += " --B_init " + str(jobToProcess['userCtfBfactor'])            
        if  jobToProcess['userCtfDefocusUError']:
            args += " --defU_err " + str(jobToProcess['userCtfDefocusUError'])            
        if  jobToProcess['userCtfDefocusVError']:
            args += " --defV_err " + str(jobToProcess['userCtfDefocusVError'])            
        if  jobToProcess['userCtfDefocusAError']:
            args += " --defA_err " + str(jobToProcess['userCtfDefocusAError'])            
        if  jobToProcess['userCtfBfactorError']:
            args += " --B_err " + str(jobToProcess['userCtfBfactorError'])            
        if  jobToProcess['doPhaseFlip']:
            args += " --do_phase_flip " + str(jobToProcess['doPhaseFlip'])            
        if  jobToProcess['doValidation']:
            args += " --do_validation " + str(jobToProcess['doValidation'])            
        if  jobToProcess['ctfDiag_lowRes']:
            args += " --ctfout_resL " + str(jobToProcess['ctfDiag_lowRes'])
        if  jobToProcess['ctfDiag_highRes']:
            args += " --ctfout_resH " + str(jobToProcess['ctfDiag_highRes'])
        if  jobToProcess['ctfDiag_Bfact']:
            args += " --ctfout_bfac " + str(jobToProcess['ctfDiag_Bfact'])
        if  jobToProcess['inputCTFstar']:
            args += " --input_ctfstar " + jobToProcess['inputCTFstar']
        if  jobToProcess['boxSuffix']:
            args += " --boxsuffix " + jobToProcess['boxSuffix']
        if  jobToProcess['outputCTFstar']:
            args += " --ctfstar " + jobToProcess['outputCTFstar']
        if  jobToProcess['logSuffix']:
            args += " --logsuffix " + jobToProcess['logSuffix']
        if  jobToProcess['writePowerSpectrumFile']:
            args += " --write_local_ctf " + str(jobToProcess['writePowerSpectrumFile'])
        if  jobToProcess['plotResRing']:
            args += " --plot_res_ring " + str(jobToProcess['plotResRing'])
        if  jobToProcess['doUnfinished']:
            args += " --do_unfinished " + str(jobToProcess['doUnfinished'])
        if  jobToProcess['skipMRCcheck']:
            args += " --skip_check_mrc " + str(jobToProcess['skipMRCcheck'])
        if  jobToProcess['skipGPUcheck']:
            args += " --skip_check_gpu " + str(jobToProcess['skipGPUcheck'])
        if  jobToProcess['inMrc']:
            args += " " + jobToProcess['inMrc']

        return args

    #
    ## Job Maintenance functions
    #  --start--    
    
    # addJob() - builds the new job from the input variables and updates the job list.
    #
    @debug.capture(clear_output=True)
    def addJob(self, target):
        listedJobs = self.jobsList.options
        listedJobsList = list(listedJobs)
        newJob = self.buildJob("", self.jobCounter)
        #converting to tuple, update jobsList, jobNumber
        newJobTuple = (newJob,)
        listedJobsList.extend(newJobTuple)
        self.jobsList.options = listedJobsList
        self.jobCounter = self.jobCounter + 1
        self.jobNumber.value = ''

    # deleteJob() - delete selected jobs from the job list.
    #
    @debug.capture(clear_output=True)
    def deleteJob(self, target):
        #obtain the listedJobs
        listedJobs = self.jobsList.options
        listedJobsList = list(listedJobs)
        #obtain the selectedJobs
        selectedJobs = self.jobsList.value
        selectedJobsList = list(selectedJobs)
        #remove selected jobs
        for i in range(len(selectedJobsList)):
            if  (str(selectedJobsList[i]).startswith('Job#') == False):
                listedJobsList.remove(selectedJobsList[i])
        #update
        self.jobsList.options = listedJobsList
        self.jobNumber.value = ''

    # buildSymlinks() - used for 'Workflow' mode. Builds a list of symlinks to output
    #                   micrographs from motioncorr in preparation for Gctf processing.
    #    Arguments:
    #        projectDirectory - contains the home directory of the Relion project for all jobs.
    #        motionCorrFolder - contains the output folder for motionCorr jobs. Used to build symlinks
    #                      for gctf input
    #
    @debug.capture(clear_output=True)
    def buildSymlinks(self, projectDirectory, motionCorrFolder):
        #obtain a list of micrographs produced by motionCorr
        micrographs = glob.glob(projectDirectory + motionCorrFolder + '/*/Micrographs/*.mrc')

        for i in range(len(micrographs)):
            #The new name combines the motionCorr jobNo with the micrograph name.
            split = micrographs[i].rsplit('/', 3)
            newFileName = split[-3] + '-' + split[-1]
            
            if  micrographs[i].endswith('_DW.mrc'):
                #ignoring Dose Weighted micrographs
                continue
            elif os.path.exists(newFileName):
                #ignoring, symlink exists, already created.
                continue
            else:
                os.symlink(micrographs[i], newFileName)

    # buildStarFileData() - creates a list of micrographs and associated data required to create a .star file
    #    Arguments - projectDirectory - relion project directory
    #              - gctfFolderName   - folder containing gctf jobs e.g. NBCtfFind
    #              - jobFolder        - folder for the ctf job. e.g. ctf1
    #    Return a list of Micrographs and associated CTF data
    #
    @debug.capture(clear_output=True)
    def buildStarFileData(self, projectDirectory, gctfFolderName, jobFolder):
        micrographs = []

        #obtaining values from _gctf.log files
        for infile in glob.glob(projectDirectory + gctfFolderName + jobFolder + 'Micrographs/*_gctf.log'):
            try: 
                path, fileName = os.path.split(infile)
                fileHandle = open(infile)
                lineList = fileHandle.readlines()
                fileHandle.close()
            except OSError as err:
                self.errorText.value = "Error reading *_gctf.log data: {0}".format(err)       
                self.errorText.layout = self.errorLayout
                break
                
            mrc = {}
            mrc['ctfImage'] = gctfFolderName + jobFolder + 'Micrographs/' + fileName.replace('_gctf.log', '.ctf:mrc')

            lastEntryColumns = ''
            lastEntryValues  = ''

            for index, obj in enumerate(lineList):
                if  '--dstep' in lineList[index]:
                    mrc['detectorPixelSize']   = float(lineList[index].split()[1])
                if  '--kv' in lineList[index]:
                    mrc['voltage']             = float(lineList[index].split()[1])
                if  '--ac' in lineList[index]:
                    mrc['ampContrast']         = float(lineList[index].split()[1])
                if  '--cs' in lineList[index]:
                    mrc['sphericalAberration'] = float(lineList[index].split()[1])
                if  'XMAG' in lineList[index]:
                    mrc['magnification']       = float(lineList[index+1].split()[3])
                if  'Resolution limit estimated' in lineList[index]:
                    mrc['maxResolution']       = float(lineList[index].rsplit(maxsplit=1)[1])
                #Depending on how gctf is run, there may be multiple entries for Defocus_U etc - take the last row in the log.
                if  'Defocus_U   Defocus_V ' in lineList[index]:
                    lastEntryColumns           = lineList[index]
                    lastEntryValues            = lineList[index+1]

            #The columns written can vary based on how Gctf is run. e.g. Phase_shift value may or may not be present
            #Matching values to column names
            lastColumns = lastEntryColumns.split()
            lastValues  = lastEntryValues.split()
            for i in range(len(lastColumns)):
                if  lastColumns[i] == 'Defocus_U':
                    mrc['defocusU']     = float(lastValues[i])
                if  lastColumns[i] == 'Defocus_V':
                    mrc['defocusV']     = float(lastValues[i])
                if  lastColumns[i] == 'Angle':
                    mrc['defocusAngle'] = float(lastValues[i])
                if  lastColumns[i] == 'CCC':
                    mrc['figOfMerit']   = float(lastValues[i])

            micrographs.append(mrc)

        #populating source micrograph paths
        for infile in glob.glob(projectDirectory + gctfFolderName + jobFolder + 'Micrographs/*.mrc'):
            try:
                symLinkTarget = os.readlink(infile)
            except OSError as err:
                self.errorText.value = "Error reading symlink: {0}".format(err)       
                self.errorText.layout = self.errorLayout
                break

            splitFilePath = symLinkTarget.rsplit('/', 4)
            micrographNameNoDW = splitFilePath[1] + '/' + splitFilePath[2] + '/' + splitFilePath[3] + '/' + splitFilePath[4]
            micrographName = splitFilePath[1] + '/' + splitFilePath[2] + '/' + splitFilePath[3] + '/' + splitFilePath[4].replace('.mrc', '_DW.mrc')

            jobNumber = splitFilePath[2]

            for i in range(len(micrographs)):
                # ctfImage = 'NBCtfFind/ctf1/Micrographs/mc2-Falcon_2012_06_12-17_14_17_0.ctf:mrc'
                splitCtfImage = micrographs[i]['ctfImage'].split('/')
                ctfJobNumber = splitCtfImage[3].split('-', 1)[0]

                if  jobNumber == ctfJobNumber:
                    matchFile = splitCtfImage[3].replace(jobNumber + '-', '').replace('.ctf:mrc', '.mrc')

                    if  matchFile == splitFilePath[4]:
                        micrographs[i]['micrographNameNoDW'] = micrographNameNoDW
                        micrographs[i]['micrographName'] = micrographName
                        break

        return micrographs

    # createStar() - Build the ctf star file
    #    Arguments - projectDirectory - relion project directory
    #              - gctfFolderName   - folder containing gctf jobs e.g. NBCtfFind
    #              - jobFolder        - folder for the ctf job. e.g. ctf1
    #              - micrographs      - a list of micrographs and associated ctf data
    #              - starFileName     - name of the file to be created
    #
    @debug.capture(clear_output=True)
    def createStar(self, projectDirectory, gctfFolderName, jobFolder, micrographs, starFileName):

        #Create the Star file, write to disk.
        try:
            fOutput = open(projectDirectory + gctfFolderName + jobFolder + '/' + starFileName, "w")
            #write out data_, loop_ (column headers)
            fOutput.write('\ndata_\n\nloop_\n_rlnMicrographNameNoDW #1 \n_rlnMicrographName #2 \n_rlnCtfImage #3 \n_rlnDefocusU #4 \n_rlnDefocusV #5 \n_rlnDefocusAngle #6 \n_rlnVoltage #7 \n_rlnSphericalAberration #8 \n_rlnAmplitudeContrast #9 \n_rlnMagnification #10 \n_rlnDetectorPixelSize #11 \n_rlnCtfFigureOfMerit #12 \n_nbCtfMaxResolution #13\n')

            #Write out rows
            for j in range(len(micrographs)):
                fOutput.write(micrographs[j]['micrographNameNoDW'] + '    ' + micrographs[j]['micrographName'] + '    ' + micrographs[j]['ctfImage'] + '    ' + str(micrographs[j]['defocusU']) + '    ' + str(micrographs[j]['defocusV']) + '    ' + str(micrographs[j]['defocusAngle']) + '    ' + str(micrographs[j]['voltage']) + '    ' + str(micrographs[j]['sphericalAberration']) + '    ' + str(micrographs[j]['ampContrast']) + '    ' + str(micrographs[j]['magnification']) + '    ' + str(micrographs[j]['detectorPixelSize']) + '    ' + str(micrographs[j]['figOfMerit']) + '    ' + str(micrographs[j]['maxResolution']) +'\n')

        except OSError as err:
            self.errorText.value = "Error writing Job Output: {0}".format(err)
            self.errorText.layout = self.errorLayout
        else:
            fOutput.close()
            
    # runAllWorkflowJobs() - execute all jobs in the list. Only executed in 'workflow' mode
    #    Arguments:
    #        projectDirectory  - contains the home directory of the Relion project for all jobs.
    #        motionCorrFolder  - contains the motionCorr2 output folder
    #
    @debug.capture(clear_output=True)
    def runAllWorkflowJobs(self, projectDirectory, motionCorrFolder):
        #obtain the listedJobs
        listedJobs = self.jobsList.options
        listedJobsList = list(listedJobs)

        self.runProgress.max = len(listedJobsList)

        if  projectDirectory.endswith('/') == False:
            projectDirectory += '/'
        
        self.errorText.layout = self.basicLayout
        
        #Run each job, but not the Header row.
        for i in range(len(listedJobsList)):
            #setting progress bar to show job has started running.
            if  (str(listedJobsList[i]).startswith('Job#') == True):
                self.runProgress.value = i+1    

            if  (str(listedJobsList[i]).startswith('Job#') == False):
                #'Workflow' mode
                outputFolder = projectDirectory + listedJobsList[i]['outMrc'] + listedJobsList[i]['jobNumber'] + '/Micrographs/'
                try:
                    #mkdir -p path, if folder exists, that's OK
                    os.makedirs(outputFolder, exist_ok=True)
                        
                    #change working directory
                    os.chdir(outputFolder)
                        
                    #create symlinks to output *.mrc from motionCorr jobs
                    self.buildSymlinks(projectDirectory, motionCorrFolder)
                        
                except OSError as err:
                    self.errorText.value = "Unable to setup processing structure: {0}".format(err) + '\n' 
                    self.errorText.layout = self.errorLayout
                else:
                    #build arguments list, run program
                    self.callProgram(self.program, self.buildArgumentsList(listedJobsList[i]), outputFolder)
                    #create .star file
                    micrographData = self.buildStarFileData(projectDirectory, listedJobsList[i]['outMrc'], listedJobsList[i]['jobNumber'] + '/')
                    self.createStar(projectDirectory, listedJobsList[i]['outMrc'], listedJobsList[i]['jobNumber'], micrographData, self.starFileName)
                self.runProgress.value = i+1           
                
    # runAllJobs() - execute all jobs in the list.
    #    target - not used, exists to make to make the button call work.
    #
    @debug.capture(clear_output=True)
    def runAllJobs(self, target):
        #obtain the listedJobs
        listedJobs = self.jobsList.options
        listedJobsList = list(listedJobs)

        self.runProgress.max = len(listedJobsList)

        #Run each job, but not the Header row.
        for i in range(len(listedJobsList)):
            #setting progress bar to show job has started running.
            if  (str(listedJobsList[i]).startswith('Job#') == True):
                self.runProgress.value = i+1    

            if  (str(listedJobsList[i]).startswith('Job#') == False):
                self.callProgram(self.program, self.buildArgumentsList(listedJobsList[i]), listedJobsList[i]['outMrc'])
                self.runProgress.value = i+1    

    # selectJob() - update field values using the selected job in the job list
    #
    @debug.capture(clear_output=True)
    def selectJob(self, target):
        #obtain the selectedJobs
        selectedJobs = self.jobsList.value
        selectedJobsList = list(selectedJobs)

        #can only select a single job for updating.
        if  len(selectedJobsList) == 1:
            self.updateScreenFields(selectedJobsList[0])
    
    # updateJob() - update the job for the displayed job number
    #
    @debug.capture(clear_output=True)
    def updateJob(self, target):
        #obtain the listedJobs
        listedJobs = self.jobsList.options
        listedJobsList = list(listedJobs)
        #build updated job
        updatedJob = self.buildJob('', '')
        updateJobNo = updatedJob['jobNumber']

        for i in range(len(listedJobsList)):
            #skip checking the header
            if  (str(listedJobsList[i]).startswith('Job#') == False):
                listedJobNo = listedJobsList[i]["jobNumber"]
                if  listedJobNo == updateJobNo:
                    listedJobsList[i] = updatedJob

        #update screen field
        self.jobsList.options = listedJobsList
        self.jobNumber.value = ''
            
    # addJobs() - Adds multiple jobs, when the user has specified a range of values.
    #    Arguments:
    #        fieldName - name of the field that value range has been specified 
    #        values    - specified values, ';' separated.
    #
    @debug.capture(clear_output=True)
    def addJobs(self, fieldName, values):
        #obtaining currently listed jobs
        listedJobs = self.jobsList.options
        listedJobsList = list(listedJobs)

        newJobs = self.buildNewJobs(fieldName, values)

        for i in range(len(newJobs)):
            #converting to tuple
            newJobTuple = (newJobs[i],)
            listedJobsList.extend(newJobTuple)

        #Update jobsList and jobNumber
        self.jobsList.options = listedJobsList
        self.jobNumber.value = ''

    # buildAllWidgets() - display the jobs list and associated buttons.
    #
    @debug.capture(clear_output=True)
    def buildAllWidgets(self):
        #Add fuctions to buttons.
        self.addButton.on_click(self.addJob)
        self.deleteButton.on_click(self.deleteJob)
        self.selectButton.on_click(self.selectJob)
        self.updateButton.on_click(self.updateJob)
        self.runAllButton.on_click(self.runAllJobs)

        buttons = HBox([self.addButton, self.deleteButton, self.selectButton, self.updateButton, self.runAllButton, self.runProgress])
        selectableTable = VBox([self.jobsList, buttons, self.errorText])

        inputWidgets = self.buildInputWidgets()

        return VBox([inputWidgets, selectableTable])

    #  --end--
    ## Job Maintenance functions
    #      
        