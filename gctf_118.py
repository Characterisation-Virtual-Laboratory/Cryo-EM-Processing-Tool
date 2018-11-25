import os
import glob
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Box, Label, Layout

#Gctf  input fields and functions to execute jobs

class contrastTransFunc:
    #Settings:
    program = 'Gctf-v1.18_sm_30_cu8.0_x86_64'
    jobPrefix = 'ctf'
    header = [("Job# | inMrc | outMrc | spherAberration | voltage | ampContrast | pixelSize | phaseShiftLow | phaseShiftHigh | phaseShiftStep | phaseShiftTarget | phaseShiftRefine | phaseShiftRefineType | detectorSize | defocusLow | defocusHigh | defocusStep | estAstigmation | bfac | resLowest | resHighest | boxSize | doEquiPhaseAvg | oversampFactorEPA | overlap | convsize | smoothingLowRes | doHighResRefinement | highResRefinement_lowRes | highResRefinement_highRes | highResRefinement_bfac | ctfDiag_lowRes | ctfDiag_highRes | ctfDiag_Bfact | inputCTFstar | outputCTFstar | logSuffix | doUnfinished | skipMRCcheck | skipGPUcheck | gpu")]
    
    #style and Layout
    styleBasic    = {'description_width': '160px'}
    styleAdvanced = {'description_width': '200px'}
    basicLayout   = Layout(width='60%')
    advLayout     = Layout(width='40%')
    errorLayout   = Layout(width='60%', border='2px solid red')
    
    #Input fields for Gctf
    jobNumber = widgets.Text(
        description='Job No: ',
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
        description='Spherical Aberration (mm): ',
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
        description='Amplitutde Contrast: ',
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
        description='Pixel Size (A): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.2f',
        style=styleBasic,
        layout=basicLayout)

    gpu = widgets.Text(
        value='',
        placeholder='indicate the GPUs to use',
        description='GPU Usage: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    ##Phase plate options
    phaseShiftLow = widgets.FloatSlider(
        value=0.0,
        min=0.0,
        max=360,
        step=0.1,
        description='Phase Shift - Lowest (degrees): ',
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
        description='Phase Shift - Highest (degrees): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.01f',
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftStep = widgets.FloatSlider(
        value=3.0,
        min=0.0,
        max=10,
        step=0.1,
        description='Phase Shift - Step: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftTarget = widgets.Select(
        options=[('CCC', '1'), ('Resolution limit', '2')],
        description='Phase Shift Target ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftTargetMulti = widgets.SelectMultiple(
        options=[('CCC', '1'), ('Resolution limit', '2')],
        description='Phase Shift Target ',
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
    
    phaseShiftRefine = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        description='Phase Shift Refine: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftRefineMulti = widgets.SelectMultiple(
        options=[('No', '0'), ('Yes', '1')],
        description='Phase Shift Refine: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftRefineMultiButton = widgets.Button(
        description='Add jobs',
        disabled=False,
        button_style='',
        tooltip='Add multiple jobs',
        icon='check')    
    
    phaseShiftRefineType = widgets.Select(
        options=[('1', '1'), ('2', '2'), ('3', '3')],
        description='Phase Shift Refine Type: ',
        disabled=False,
        rows=3,
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftRefineTypeMulti = widgets.SelectMultiple(
        options=[('1', '1'), ('2', '2'), ('3', '3')],
        description='Phase Shift Refine Type: ',
        disabled=False,
        rows=3,
        style=styleAdvanced,
        layout=advLayout)

    phaseShiftRefineTypeMultiButton = widgets.Button(
        description='Add jobs',
        disabled=False,
        button_style='',
        tooltip='Add multiple jobs',
        icon='check')    
    
    ##Additional options
    estAstigmation = widgets.IntText(
        value=1000,
        description='Est Astigmation (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    boxSize = widgets.IntText(
        value=1024,
        description='Box Size (pixel): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    resLowest = widgets.IntText(
        value=50,
        description='Lowest Resolution (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    resHighest = widgets.IntText(
        value=4,
        description='Highest Resolution (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusLow = widgets.IntText(
        value=5000,
        description='Lowest Defocus (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusHigh = widgets.IntText(
        value=90000,
        description='Highest Defocus (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusStep = widgets.IntText(
        value=500,
        description='Defocus Step (A): ',
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
        description='Do Equi Phase Average: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    oversampFactorEPA = widgets.IntSlider(
        value=4,
        min=0,
        max=20,
        step=1,
        description='EPA - Oversamp Factor: ',
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
        description='Overlapping Factor: ',
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

    smoothingLowRes = widgets.IntSlider(
        value=0,
        min=0,
        max=100,
        step=1,
        description='Smoothing Low Res (A): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    doHighResRefinement = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='High Res Refinement: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    highResRefinement_lowRes = widgets.FloatText(
        value=15.0,
        description='High Res Refine-Low Res(A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    highResRefinement_highRes = widgets.FloatText(
        value=4.0,
        description='High Res Refine-High Res(A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    highResRefinement_bfac = widgets.IntText(
        value=50,
        description='High Res Refine-bfac(A^2): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ##CTF output file options
    ctfDiag_lowRes =  widgets.FloatText(
        value=100.0,
        description='CTF Diagnosis-Low Res: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ctfDiag_highRes = widgets.FloatText(
        value=2.8,
        description='CTF Diagnosis-High Res: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ctfDiag_Bfact = widgets.IntText(
        value=50,
        description='CTF Diagnosis - Bfactor: ',
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
        description='Log file Suffix:',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    doUnfinished  = widgets.Select(
        options=[('No', 0), ('Yes', 1)],
        description='Continue Processing: ',
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
        self.callProgram(self.program, self.buildArgumentsList(self.buildJob('', '', '', self.jobNumber)), self.outMrc.value)
        self.runProgress.value = self.runProgress.max
    
    #Multi value field processing support
    # addPhaseShiftTargetJobs() - add new jobs for all 'phaseShiftTarget' values entered
    #
    @debug.capture(clear_output=True)
    def addPhaseShiftTargetJobs(self, target):
        self.addJobs("phaseShiftTarget", self.phaseShiftTargetMulti.value)

    # addPhaseShiftRefineJobs() - add new jobs for all 'phaseShiftRefine' values entered
    #
    @debug.capture(clear_output=True)
    def addPhaseShiftRefineJobs(self, target):
        self.addJobs("phaseShiftRefine", self.phaseShiftRefineMulti.value)

    # addPhaseShiftRefineTypeJobs() - add new jobs for all 'phaseShiftRefineType' values entered
    #
    @debug.capture(clear_output=True)
    def addPhaseShiftRefineTypeJobs(self, target):
        self.addJobs("phaseShiftRefineType", self.phaseShiftRefineTypeMulti.value)

    # buildInputWidgets() - write all the Gctf input fields to the screen.
    #
    @debug.capture(clear_output=True)
    def buildInputWidgets(self):
        #linking button on_click to function    
        self.runButton.on_click(self.runSingleJob)
        self.phaseShiftTargetMultiButton.on_click(self.addPhaseShiftTargetJobs)
        self.phaseShiftRefineMultiButton.on_click(self.addPhaseShiftRefineJobs)
        self.phaseShiftRefineTypeMultiButton.on_click(self.addPhaseShiftRefineTypeJobs)        
        
        phaseShiftTargetInputs = HBox([self.phaseShiftTarget, self.phaseShiftTargetMulti, self.phaseShiftTargetMultiButton])
        phaseShiftRefineInputs = HBox([self.phaseShiftRefine, self.phaseShiftRefineMulti, self.phaseShiftRefineMultiButton])    
        phaseShiftRefineTypeInputs = HBox([self.phaseShiftRefineType, self.phaseShiftRefineTypeMulti, self.phaseShiftRefineTypeMultiButton])    

        normal     = VBox([self.jobNumber, self.inMrc, self.outMrc, self.spherAberration, self.voltage, self.ampContrast,
                           self.pixelSize, self.gpu])
        phasePlate = VBox([self.phaseShiftLow, self.phaseShiftHigh, self.phaseShiftStep, phaseShiftTargetInputs, 
                           phaseShiftRefineInputs, phaseShiftRefineTypeInputs])
        additional = VBox([self.detectorSize, self.defocusLow, self.defocusHigh, self.defocusStep, self.estAstigmation, 
                           self.bfac, self.resLowest, self.resHighest, self.boxSize])
        advanced   = VBox([self.doEquiPhaseAvg, self.oversampFactorEPA, self.overlap, self.convsize, self.smoothingLowRes, 
                           self.doHighResRefinement, self.highResRefinement_lowRes, self.highResRefinement_highRes, 
                           self.highResRefinement_bfac])
        ctfIO      = VBox([self.ctfDiag_lowRes, self.ctfDiag_highRes, self.ctfDiag_Bfact, self.inputCTFstar, self.outputCTFstar, 
                           self.logSuffix, self.doUnfinished,self.skipMRCcheck, self.skipGPUcheck])

        tab = widgets.Tab(children=[normal, phasePlate, additional, advanced, ctfIO])
        tab.set_title(0, 'Normal')
        tab.set_title(1, 'Phase Plate Options')
        tab.set_title(2, 'Additional Options')
        tab.set_title(3, 'Advanced Additional Options')
        tab.set_title(4, 'CTF and IO')        

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
            newJob = self.buildJob('', '', self.jobCounter)
            self.jobCounter = self.jobCounter + 1
            return newJob
        
        #Building multiple jobs
        if  fieldName == 'phaseShiftTarget':
            fieldList = list(values)
        if  fieldName == 'phaseShiftRefine':
            fieldList = list(values)
        if  fieldName == 'phaseShiftRefineType':
            fieldList = list(values)

        for i in range(len(fieldList)):
            fieldCleaned = fieldList[i].strip()
        
            if  fieldCleaned:
                if  fieldName == 'phaseShiftTarget':
                    newJob = self.buildJob(fieldCleaned, '', '', self.jobCounter)

                if  fieldName == 'phaseShiftRefine':
                    newJob = self.buildJob('', fieldCleaned, '', self.jobCounter)

                if  fieldName == 'phaseShiftRefineType':
                    newJob = self.buildJob('', '', fieldCleaned, self.jobCounter)

                self.jobCounter = self.jobCounter + 1
                jobList.append(newJob)                    

        return jobList

    # buildJob() - construct a single job containing all arguments.
    #    Arguments:
    #        phaseShiftTargetValue - use the phaseShiftTarget is specified, otherwise use screen value
    #        phaseShiftRefineValue - use the phaseShiftRefine is specified, otherwise use screen value
    #        phaseShiftRefineTypeValue - use the phaseShiftRefineType if specified, otherwise use screen value
    #        jobNo - the next job number to use
    #    Return:
    #        dict containing all arguments.
    #
    @debug.capture(clear_output=True)
    def buildJob(self, phaseShiftTargetValue, phaseShiftRefineValue, phaseShiftRefineTypeValue, jobNo):
        
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
        newJob['phaseShiftLow']             = self.phaseShiftLow.value
        newJob['phaseShiftHigh']            = self.phaseShiftHigh.value
        newJob['phaseShiftStep']            = self.phaseShiftStep.value

        if  phaseShiftTargetValue:
            newJob['phaseShiftTarget']      = phaseShiftTargetValue
        else:    
            newJob['phaseShiftTarget']      = self.phaseShiftTarget.value

        if  phaseShiftRefineValue:
            newJob['phaseShiftRefine']      = phaseShiftRefineValue 
        else:
            newJob['phaseShiftRefine']      = self.phaseShiftRefine.value 

        if  phaseShiftRefineTypeValue:
            newJob['phaseShiftRefineType']  = phaseShiftRefineTypeValue 
        else:
            newJob['phaseShiftRefineType']  = self.phaseShiftRefineType.value 

        newJob['detectorSize']              = self.detectorSize.value
        newJob['defocusLow']                = self.defocusLow.value   
        newJob['defocusHigh']               = self.defocusHigh.value   
        newJob['defocusStep']               = self.defocusStep.value
        newJob['estAstigmation']            = self.estAstigmation.value   
        newJob['bfac']                      = self.bfac.value   
        newJob['resLowest']                 = self.resLowest.value   
        newJob['resHighest']                = self.resHighest.value   
        newJob['boxSize']                   = self.boxSize.value   
        newJob['doEquiPhaseAvg']            = self.doEquiPhaseAvg.value
        newJob['oversampFactorEPA']         = self.oversampFactorEPA.value   
        newJob['overlap']                   = self.overlap.value   
        newJob['convsize']                  = self.convsize.value   
        newJob['smoothingLowRes']           = self.smoothingLowRes.value   
        newJob['doHighResRefinement']       = self.doHighResRefinement.value
        newJob['highResRefinement_lowRes']  = self.highResRefinement_lowRes.value   
        newJob['highResRefinement_highRes'] = self.highResRefinement_highRes.value   
        newJob['highResRefinement_bfac']    = self.highResRefinement_bfac.value   
        newJob['ctfDiag_lowRes']            = self.ctfDiag_lowRes.value   
        newJob['ctfDiag_highRes']           = self.ctfDiag_highRes.value   
        newJob['ctfDiag_Bfact']             = self.ctfDiag_Bfact.value   
        newJob['inputCTFstar']              = self.inputCTFstar.value   
        newJob['outputCTFstar']             = self.outputCTFstar.value   
        newJob['logSuffix']                 = self.logSuffix.value   
        newJob['doUnfinished']              = self.doUnfinished.value
        newJob['skipMRCcheck']              = self.skipMRCcheck.value
        newJob['skipGPUcheck']              = self.skipGPUcheck.value
        newJob['gpu']                       = self.gpu.value 
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
        self.phaseShiftLow.value             = selectedJob['phaseShiftLow']
        self.phaseShiftHigh.value            = selectedJob['phaseShiftHigh']
        self.phaseShiftStep.value            = selectedJob['phaseShiftStep']
        self.phaseShiftTarget.value          = selectedJob['phaseShiftTarget']
        self.phaseShiftRefine.value          = selectedJob['phaseShiftRefine']
        self.phaseShiftRefineType.value      = selectedJob['phaseShiftRefineType']        
        self.detectorSize.value              = selectedJob['detectorSize']
        self.defocusLow.value                = selectedJob['defocusLow']
        self.defocusHigh.value               = selectedJob['defocusHigh']
        self.defocusStep.value               = selectedJob['defocusStep']
        self.estAstigmation.value            = selectedJob['estAstigmation']
        self.bfac.value                      = selectedJob['bfac']
        self.resLowest.value                 = selectedJob['resLowest']
        self.resHighest.value                = selectedJob['resHighest']
        self.boxSize.value                   = selectedJob['boxSize']
        self.doEquiPhaseAvg.value            = selectedJob['doEquiPhaseAvg']
        self.oversampFactorEPA.value         = selectedJob['oversampFactorEPA']
        self.overlap.value                   = selectedJob['overlap']
        self.convsize.value                  = selectedJob['convsize']
        self.smoothingLowRes.value           = selectedJob['smoothingLowRes']
        self.doHighResRefinement.value       = selectedJob['doHighResRefinement']
        self.highResRefinement_lowRes.value  = selectedJob['highResRefinement_lowRes']
        self.highResRefinement_highRes.value = selectedJob['highResRefinement_highRes']
        self.highResRefinement_bfac.value    = selectedJob['highResRefinement_bfac']
        self.ctfDiag_lowRes.value            = selectedJob['ctfDiag_lowRes']
        self.ctfDiag_highRes.value           = selectedJob['ctfDiag_highRes']
        self.ctfDiag_Bfact.value             = selectedJob['ctfDiag_Bfact']
        self.inputCTFstar.value              = selectedJob['inputCTFstar']
        self.outputCTFstar.value             = selectedJob['outputCTFstar']
        self.logSuffix.value                 = selectedJob['logSuffix']
        self.doUnfinished.value              = selectedJob['doUnfinished']
        self.skipMRCcheck.value              = selectedJob['skipMRCcheck']
        self.skipGPUcheck.value              = selectedJob['skipGPUcheck']
        self.gpu.value                       = selectedJob['gpu']

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
        if  jobToProcess['phaseShiftLow']:
            args += " --phase_shift_L " + str(jobToProcess['phaseShiftLow'])
        if  jobToProcess['phaseShiftHigh']:
            args += " --phase_shift_H " + str(jobToProcess['phaseShiftHigh'])
        if  jobToProcess['phaseShiftStep']:
            args += " --phase_shift_S " + str(jobToProcess['phaseShiftStep'])
        if  jobToProcess['phaseShiftTarget']:
            args += " --phase_shift_T " + str(jobToProcess['phaseShiftTarget'])
        if  jobToProcess['phaseShiftRefine'] == '1':
            args += " --cosearch_refine_ps "
        if  jobToProcess['phaseShiftRefineType']:
            args += " --refine_2d_T " + str(jobToProcess['phaseShiftRefineType'])
        if  jobToProcess['detectorSize']:
            args += " --dstep " + str(jobToProcess['detectorSize'])
        if  jobToProcess['defocusLow']:
            args += " --defL " + str(jobToProcess['defocusLow'])
        if  jobToProcess['defocusHigh']:
            args += " --defH " + str(jobToProcess['defocusHigh'])
        if  jobToProcess['defocusStep']:
            args += " --defS " + str(jobToProcess['defocusStep'])
        if  jobToProcess['estAstigmation']:
            args += " --astm " + str(jobToProcess['estAstigmation'])
        if  jobToProcess['bfac']:
            args += " --bfac " + str(jobToProcess['bfac'])
        if  jobToProcess['resLowest']:
            args += " --resL " + str(jobToProcess['resLowest'])
        if  jobToProcess['resHighest']:
            args += " --resH " + str(jobToProcess['resHighest'])
        if  jobToProcess['boxSize']:
            args += " --boxsize " + str(jobToProcess['boxSize'])
        if  jobToProcess['doEquiPhaseAvg']:
            args += " --do_EPA " + str(jobToProcess['doEquiPhaseAvg'])
        if  jobToProcess['oversampFactorEPA']:
            args += " --EPA_oversmp " + str(jobToProcess['oversampFactorEPA'])
        if  jobToProcess['overlap']:
            args += " --overlap " + str(jobToProcess['overlap'])
        if  jobToProcess['convsize']:
            args += " --convsize " + str(jobToProcess['convsize'])
        if  jobToProcess['smoothingLowRes']:
            args += " --smooth_resL " + str(jobToProcess['smoothingLowRes'])
        if  jobToProcess['doHighResRefinement']:
            args += " --do_Hres_ref " + str(jobToProcess['doHighResRefinement'])
        if  jobToProcess['highResRefinement_lowRes']:
            args += " --Href_resL " + str(jobToProcess['highResRefinement_lowRes'])
        if  jobToProcess['highResRefinement_highRes']:
            args += " --Href_resH " + str(jobToProcess['highResRefinement_highRes'])
        if  jobToProcess['highResRefinement_bfac']:
            args += " --Href_bfac " + str(jobToProcess['highResRefinement_bfac'])
        if  jobToProcess['ctfDiag_lowRes']:
            args += " --ctfout_resL " + str(jobToProcess['ctfDiag_lowRes'])
        if  jobToProcess['ctfDiag_highRes']:
            args += " --ctfout_resH " + str(jobToProcess['ctfDiag_highRes'])
        if  jobToProcess['ctfDiag_Bfact']:
            args += " --ctfout_bfac " + str(jobToProcess['ctfDiag_Bfact'])
        if  jobToProcess['inputCTFstar']:
            args += " --input_ctfstar " + jobToProcess['inputCTFstar']
        if  jobToProcess['outputCTFstar']:
            args += " --ctfstar " + jobToProcess['outputCTFstar']
        if  jobToProcess['logSuffix']:
            args += " --logsuffix " + jobToProcess['logSuffix']
        if  jobToProcess['doUnfinished']:
            args += " --do_unfinished " + str(jobToProcess['doUnfinished'])
        if  jobToProcess['skipMRCcheck']:
            args += " --skip_check_mrc " + str(jobToProcess['skipMRCcheck'])
        if  jobToProcess['skipGPUcheck']:
            args += " --skip_check_gpu " + str(jobToProcess['skipGPUcheck'])
        if  jobToProcess['gpu']:
            args += " --gid " + jobToProcess['gpu']
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
        newJob = self.buildJob("", "", "", self.jobCounter)
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
        updatedJob = self.buildJob('', '', '', '')
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
        