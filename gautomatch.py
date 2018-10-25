import subprocess as subp
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Box, Label, Layout

#Automatic Particle Picking (gautomatch) input fields and functions to execute jobs

class autoPicking:
    #Settings:
    program = 'Gautomatch_v0.56_sm20_cu8.0'
    jobPrefix = 'pick'
    header = [("Job# | inMrc | outMrc | pixelSize | diameter | particlePickingTemplates | pixelSizeTemplate | angularStepSize | speedLevel | boxSize | minDistance | crossCorrelationCutoff | localSigmaDiameter | localSigmaCutoff | localAvgDiameter | localAvgMaxCutoff | localAvgMinCutoff | lowPassFilter | highPassFilter | doPreFilter | preFilterLowPass | preFilterHighPass | detectIce | templateNormType | doBandpassFilter |     writeCrossCorrelationMrcs | writePhaseFlippedMrcs | writePreFilteredMrcs | writeEstBackgroundMrcs | writeBackgroundSubtractedMrcs | writeLocalSigmaMrcs | writeAutoDetectedMask | pickByPreDefinedCoords | excludedSuffixCoords | maskExcludedCoords | globalExcludedCoords | doUnfinished | dontInvertTemplateContrast | extractRawParticle | extractPhaseFlipped | gpu |")]
    
    #style and Layout
    styleBasic    = {'description_width': '160px'}
    styleAdvanced = {'description_width': '160px'}
    basicLayout   = Layout(width='80%')
    advLayout     = Layout(width='100%')

    #Input fields for Motion Correction
    jobNumber = widgets.Text(
        description='Job No: ',
        disabled=True,
        style=styleBasic,
        layout=basicLayout)

    inMrc = widgets.Text(
        value='',
        placeholder='path for input MCR file or folder containing MRC files',
        description='Input: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    outMrc = widgets.Text(
        value='',
        placeholder='path for output MCR file',
        description='Output: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    pixelSize = widgets.FloatSlider(
        value=1.34,
        min=0,
        max=4.0,
        step=0.01,
        description='Pixel Size (A): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.2f',
        style=styleBasic,
        layout=basicLayout)

    diameter = widgets.IntText(
        value=400,
        description='Diameter (A): ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    particlePickingTemplates = widgets.Text(
        value='',
        placeholder='Particle picking templates in 2D MRC stack',
        description='Particle Picking Template: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    pixelSizeTemplate = widgets.FloatSlider(
        value=1.34,
        min=0,
        max=4.0,
        step=0.01,
        description='Pixel Size Template (A): ',
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

    #Additional Options
    angularStepSize = widgets.IntSlider(
        value=5,
        min=0,
        max=20,
        step=1,
        description='Angular Step Size: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    speedLevel = widgets.Select(
        options=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],
        description='Speed Level: ',
        disabled=False,
        value='2',
        style=styleAdvanced,
        layout=advLayout)
    
    boxSize = widgets.IntText(
        description='Box Size (pixel): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    minDistance = widgets.IntText(
        description='Minimum Distance (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    crossCorrelationCutoff = widgets.FloatSlider(
        value=0.1,
        min=0,
        max=1,
        step=0.1,
        description='Cross Correlation Cutoff: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)

    localSigmaDiameter = widgets.IntText(
        description='Local Sigma Diameter (A): ',
        value=200,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    localSigmaCutoff = widgets.FloatSlider(
        value=1.3,
        min=0,
        max=4,
        step=0.1,
        description='Local Sigma Cutoff: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)

    localAvgDiameter = widgets.IntText(
        description='Local Avg Diameter (A): ',
        value=400,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    localAvgMaxCutoff = widgets.FloatSlider(
        value=2.0,
        min=0,
        max=20,
        step=0.1,
        description='Local Avg Max Cutoff: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)
    
    localAvgMinCutoff = widgets.FloatSlider(
        value=-1.0,
        min=-20,
        max=20,
        step=0.1,
        description='Local Avg Min Cutoff: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)
    
    lowPassFilter = widgets.IntSlider(
        value=30,
        min=0,
        max=100,
        step=1,
        description='Low Pass Filter: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)
    
    highPassFilter = widgets.IntSlider(
        value=1000,
        min=0,
        max=10000,
        step=1,
        description='High Pass Filter: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    doPreFilter = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Do Pre Filter: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    preFilterLowPass = widgets.IntSlider(
        value=8,
        min=0,
        max=100,
        step=1,
        description='Pre Filter - Low Pass: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)
    
    preFilterHighPass = widgets.IntSlider(
        value=1000,
        min=0,
        max=10000,
        step=1,
        description='Pre Filter - High Pass: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)
    
    detectIce = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='1',
        description='Detect Ice: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    templateNormType = widgets.Select(
        options=[('1', '1'), ('2', '2'), ('3', '3')],
        value='1',
        description='Template Norm. type: ',
        disabled=False,
        rows=3,
        style=styleAdvanced,
        layout=advLayout)    

    doBandpassFilter = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='1',
        description='Do Bandpass Filter: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    

    #I/O Options
    writeCrossCorrelationMrcs = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Write Cross Correlation: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    writePhaseFlippedMrcs = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Write Phase Flipped: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    writePreFilteredMrcs = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Write Pre Filtered: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    writeEstBackgroundMrcs = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Write Est Background: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    writeBackgroundSubtractedMrcs = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Write Background Subtracted: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    writeLocalSigmaMrcs = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Write Local Sigma: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    writeAutoDetectedMask = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Write Auto Detected Mask: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    pickByPreDefinedCoords = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Exclusive Picking: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    excludedSuffixCoords = widgets.Text(
        placeholder='path for input Relion .star or EMAN .box file containing excluded suffix coordinates',
        description='Excluded Suffix Coords: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout) 
    
    maskExcludedCoords = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Mask Excluded Coords: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    globalExcludedCoords = widgets.Text(
        placeholder='path for .star or .box file containing coordinates to exclude from all mrcs',
        description='Global Excluded Coords: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout) 
        
    doUnfinished = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='Yes',
        description='Autopick unfinished mrcs: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    dontInvertTemplateContrast = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description="Don't invert template contrast: ",
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    extractRawParticle = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Extract particle from raw mrc: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)    
    
    extractPhaseFlipped = widgets.Select(
        options=[('No', 'No'), ('Yes', 'Yes')],
        value='No',
        description='Extract particle from phase flipped mrc: ',
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

    ##Debug assistance
    debug = widgets.Textarea(
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
    
    #Single Job run support
    def runSingleJob(self, target):
        self.callProgram(self.program, self.buildArgumentsList(self.buildJob('', '', self.jobNumber)), self.outMrc.value) 

    """Determine range values for gautomatch        
    #Multi value field processing support
    # addPatchJobs() - add new jobs for all 'Patch' values entered
    def addPatchJobs(self, target):
        self.debug.value = self.debug.value + "Inside addPatchJobs\n"
        self.addJobs("patch", self.patchMulti.value)

    # addBFactorJobs() - add new jobs for all 'BFactor' values entered.
    def addBFactorJobs(self, target):
        self.debug.value = self.debug.value + "Inside addBFactorJobs\n"
        self.addJobs("bFactor", self.bFactorMulti.value)
    """

    # buildInputWidgets() - write all the Motion Correction input fields to the screen.
    #
    def buildInputWidgets(self):
        #linking button on_click to function    
        self.runButton.on_click(self.runSingleJob)

        """Determine range values for gautomatch        
        self.patchMultiButton.on_click(self.addPatchJobs)
        self.bFactorMultiButton.on_click(self.addBFactorJobs)        

        patchInputs = HBox([self.patch, self.patchMulti, self.patchMultiButton])
        bFactorInputs = HBox([self.bFactor, self.bFactorMulti, self.bFactorMultiButton])    
        """

        basic      = VBox([self.jobNumber, self.inMrc, self.outMrc, self.pixelSize, self.diameter, self.particlePickingTemplates,   
                           self.pixelSizeTemplate, self.gpu])

        add1 = VBox([self.angularStepSize, self.speedLevel, self.boxSize, self.minDistance, self.crossCorrelationCutoff,
                     self.localSigmaDiameter, self.localSigmaCutoff, self.localAvgDiameter, self.localAvgMaxCutoff,
                     self.localAvgMinCutoff])
        add2 = VBox([self.lowPassFilter, self.highPassFilter, self.doPreFilter, self.preFilterLowPass, self.preFilterHighPass,
                           self.detectIce, self.templateNormType, self.doBandpassFilter])
        addBoxLayout = Layout(display='flex',
                            flex_flow='row',
                            align_items='stretch',
                            border='none',
                            width='150%')
        additional = Box(children=[add1, add2], layout=addBoxLayout)        
        
        
        io1 = VBox([HBox([self.writeCrossCorrelationMrcs, self.writePhaseFlippedMrcs]), 
                    HBox([self.writePreFilteredMrcs, self.writeEstBackgroundMrcs]),
                    HBox([self.writeBackgroundSubtractedMrcs, self.writeLocalSigmaMrcs]),
                    HBox([self.writeAutoDetectedMask]),
                    HBox([self.pickByPreDefinedCoords, self.excludedSuffixCoords]),
                    HBox([self.maskExcludedCoords, self.globalExcludedCoords]),
                    HBox([self.doUnfinished, self.dontInvertTemplateContrast]),
                    HBox([self.extractRawParticle, self.extractPhaseFlipped])])
        ioBoxLayout = Layout(display='flex',
                            flex_flow='row',
                            align_items='stretch',
                            border='none',
                            width='150%')
        #ioOptions = Box(children=[io1, io2], layout=ioBoxLayout)        
        
        tab = widgets.Tab(children=[basic, additional, io1])
        tab.set_title(0, 'Basic')
        tab.set_title(1, 'Additional')
        tab.set_title(2, 'I/O')
        
        if  self.showDebug:
            return VBox([self.debug, tab, self.runButton])
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
    def buildNewJobs(self, fieldName, values):
        fieldList = []
        jobList = []

        #Building a single job
        if  not fieldName and not values:
            newJob = self.buildJob('', '', self.jobCounter)
            self.jobCounter = self.jobCounter + 1
            return newJob

        """Determine range values for gautomatch        """
        #Building multiple jobs
        if  fieldName == 'patch':
            fieldList = self.patchMulti.value.split(";")
        if  fieldName == 'bFactor':
            fieldList = self.bFactorMulti.value.split(";")

        self.debug.value = self.debug.value + "fieldList: " + str(fieldList) + "\n"            
            
        for i in range(len(fieldList)):
            fieldCleaned = fieldList[i].strip()
            
            self.debug.value = self.debug.value + "fieldCleaned: " + str(fieldCleaned) + "\n"  
            
            if  fieldCleaned:
                if  fieldName == 'patch':
                    newJob = self.buildJob(fieldCleaned, '', self.jobCounter)

                if  fieldName == 'bFactor':
                    newJob = self.buildJob('', fieldCleaned, self.jobCounter)

                self.debug.value = self.debug.value + "newJob: " + str(newJob) + "\n"
                
                self.jobCounter = self.jobCounter + 1
                jobList.append(newJob)                    

        self.debug.value = self.debug.value + "jobList: " + str(jobList) + "\n"                
        return jobList
        
    # buildJob() - construct a single job containing all arguments.
    #    Arguments:
    #        patchValue - use the patchValue is specified, otherwise use screen value
    #        bFactorValue - use the bFactorValue if specified, otherwise use screen value
    #        jobNo - the next job number to use
    #    Return:
    #        dict containing all arguments.
    #
    def buildJob(self, patchValue, bFactorValue, jobNo):

        jobNoWithPrefix = self.jobPrefix + str(jobNo)
        if  jobNo:
            newJob = {'jobNumber':jobNoWithPrefix}
        else:
            newJob = {'jobNumber':self.jobNumber.value}

        newJob['inMrc']                          = self.inMrc.value
        newJob['outMrc']                         = self.outMrc.value
        newJob['pixelSize']                      = self.pixelSize.value

        """Determine range values for gautomatch        """     
        #if  patchValue:
        #    newJob['patch']     = patchValue
        #else:    
        #    newJob['patch']     = self.patch.value

        #if  bFactorValue:
        #    newJob['bFactor']   = bFactorValue 
        #else:
        #    newJob['bFactor']   = self.bFactor.value 

        newJob['diameter']                      = self.diameter.value   
        newJob['particlePickingTemplates']      = self.particlePickingTemplates.value
        newJob['pixelSizeTemplate']             = self.pixelSizeTemplate.value
        newJob['gpu']                           = self.gpu.value
        newJob['angularStepSize']               = self.angularStepSize.value
        newJob['speedLevel']                    = self.speedLevel.value
        newJob['boxSize']                       = self.boxSize.value
        newJob['minDistance']                   = self.minDistance.value
        newJob['crossCorrelationCutoff']        = self.crossCorrelationCutoff.value
        newJob['localSigmaDiameter']            = self.localSigmaDiameter.value   
        newJob['localSigmaCutoff']              = self.localSigmaCutoff.value
        newJob['localAvgDiameter']              = self.localAvgDiameter.value   
        newJob['localAvgMaxCutoff']             = self.localAvgMaxCutoff.value   
        newJob['localAvgMinCutoff']             = self.localAvgMinCutoff.value
        newJob['lowPassFilter']                 = self.lowPassFilter.value   
        newJob['highPassFilter']                = self.highPassFilter.value   
        newJob['doPreFilter']                   = self.doPreFilter.value   
        newJob['preFilterLowPass']              = self.preFilterLowPass.value
        newJob['preFilterHighPass']             = self.preFilterHighPass.value   
        newJob['detectIce']                     = self.detectIce.value
        newJob['templateNormType']              = self.templateNormType.value
        newJob['doBandpassFilter']              = self.doBandpassFilter.value
        newJob['writeCrossCorrelationMrcs']     = self.writeCrossCorrelationMrcs.value
        newJob['writePhaseFlippedMrcs']         = self.writePhaseFlippedMrcs.value
        newJob['writePreFilteredMrcs']          = self.writePreFilteredMrcs.value
        newJob['writeEstBackgroundMrcs']        = self.writeEstBackgroundMrcs.value
        newJob['writeBackgroundSubtractedMrcs'] = self.writeBackgroundSubtractedMrcs.value
        newJob['writeLocalSigmaMrcs']           = self.writeLocalSigmaMrcs.value
        newJob['writeAutoDetectedMask']         = self.writeAutoDetectedMask.value
        newJob['pickByPreDefinedCoords']        = self.pickByPreDefinedCoords.value
        newJob['excludedSuffixCoords']          = self.excludedSuffixCoords.value
        newJob['maskExcludedCoords']            = self.maskExcludedCoords.value
        newJob['globalExcludedCoords']          = self.globalExcludedCoords.value
        newJob['doUnfinished']                  = self.doUnfinished.value
        newJob['dontInvertTemplateContrast']    = self.dontInvertTemplateContrast.value
        newJob['extractRawParticle']            = self.extractRawParticle.value
        newJob['extractPhaseFlipped']           = self.extractPhaseFlipped.value
        return newJob

    # updateScreenFields() - updates screen fields using supplied dict.
    #    Arguments:
    #        selectedJob - a dict containing all screen values.
    #
    def updateScreenFields(self, selectedJob):
        self.jobNumber.value                     = selectedJob['jobNumber']
        self.inMrc.value                         = selectedJob['inMrc']
        self.outMrc.value                        = selectedJob['outMrc']
        self.pixelSize.value                     = selectedJob['pixelSize']
        self.diameter.value                      = selectedJob['diameter']
        self.particlePickingTemplates.value      = selectedJob['particlePickingTemplates']
        self.pixelSizeTemplate.value             = selectedJob['pixelSizeTemplate']
        self.gpu.value                           = selectedJob['gpu']
        self.angularStepSize.value               = selectedJob['angularStepSize']
        self.speedLevel.value                    = selectedJob['speedLevel']
        self.boxSize.value                       = selectedJob['boxSize']
        self.minDistance.value                   = selectedJob['minDistance']
        self.crossCorrelationCutoff.value        = selectedJob['crossCorrelationCutoff']
        self.localSigmaDiameter.value            = selectedJob['localSigmaDiameter']
        self.localSigmaCutoff.value              = selectedJob['localSigmaCutoff']
        self.localAvgDiameter.value              = selectedJob['localAvgDiameter']    
        self.localAvgMaxCutoff.value             = selectedJob['localAvgMaxCutoff']    
        self.localAvgMinCutoff.value             = selectedJob['localAvgMinCutoff'] 
        self.lowPassFilter.value                 = selectedJob['lowPassFilter']  
        self.highPassFilter.value                = selectedJob['highPassFilter']
        self.doPreFilter.value                   = selectedJob['doPreFilter']    
        self.preFilterLowPass.value              = selectedJob['preFilterLowPass']
        self.preFilterHighPass.value             = selectedJob['preFilterHighPass']  
        self.detectIce.value                     = selectedJob['detectIce']
        self.templateNormType.value              = selectedJob['templateNormType'] 
        self.doBandpassFilter.value              = selectedJob['doBandpassFilter']
        self.writeCrossCorrelationMrcs.value     = selectedJob['writeCrossCorrelationMrcs']
        self.writePhaseFlippedMrcs.value         = selectedJob['writePhaseFlippedMrcs'] 
        self.writePreFilteredMrcs.value          = selectedJob['writePreFilteredMrcs']
        self.writeEstBackgroundMrcs.value        = selectedJob['writeEstBackgroundMrcs'] 
        self.writeBackgroundSubtractedMrcs.value = selectedJob['writeBackgroundSubtractedMrcs']
        self.writeLocalSigmaMrcs.value           = selectedJob['writeLocalSigmaMrcs']
        self.writeAutoDetectedMask.value         = selectedJob['writeAutoDetectedMask'] 
        self.pickByPreDefinedCoords.value        = selectedJob['pickByPreDefinedCoords']
        self.excludedSuffixCoords.value          = selectedJob['excludedSuffixCoords']
        self.maskExcludedCoords.value            = selectedJob['maskExcludedCoords']
        self.globalExcludedCoords.value          = selectedJob['globalExcludedCoords']
        self.doUnfinished.value                  = selectedJob['doUnfinished']
        self.dontInvertTemplateContrast.value    = selectedJob['dontInvertTemplateContrast']
        self.extractRawParticle.value            = selectedJob['extractRawParticle']
        self.extractPhaseFlipped.value           = selectedJob['extractPhaseFlipped']        
        
    # buildArgumentsList() - builds a string of arguments for calling Motion Correction.
    #    Arguments:
    #        jobToProcess - a dict containing all screen values.
    #
    def buildArgumentsList(self, jobToProcess):
        args = ''

        if  jobToProcess['pixelSize']:
            args += " --apixM " + str(jobToProcess['pixelSize'])
        if  jobToProcess['diameter']:
            args += " --diameter " + str(jobToProcess['diameter'])
        if  jobToProcess['particlePickingTemplates']:
            args += " --T " + str(jobToProcess['particlePickingTemplates'])
        if  jobToProcess['pixelSizeTemplate']:
            args += " --apixT " + str(jobToProcess['pixelSizeTemplate'])
        if  jobToProcess['gpu']:
            args += " --gid " + str(jobToProcess['gpu'])
        if  jobToProcess['angularStepSize']:
            args += " --ang_step " + str(jobToProcess['angularStepSize'])
        if  jobToProcess['speedLevel']:
            args += " --speed " + str(jobToProcess['speedLevel'])
        if  jobToProcess['boxSize']:
            args += " --boxsize " + str(jobToProcess['boxSize'])
        if  jobToProcess['minDistance']:
            args += " --min_dist " + str(jobToProcess['minDistance'])
        if  jobToProcess['crossCorrelationCutoff']:
            args += " --cc_cutoff " + str(jobToProcess['crossCorrelationCutoff'])
        if  jobToProcess['localSigmaDiameter']:
            args += " --lsigma_D " + str(jobToProcess['localSigmaDiameter'])
        if  jobToProcess['localSigmaCutoff']:
            args += " --lsigma_cutoff " + str(jobToProcess['localSigmaCutoff'])
        if  jobToProcess['localAvgDiameter']:
            args += " --lave_D " + str(jobToProcess['localAvgDiameter'])
        if  jobToProcess['localAvgMaxCutoff']:
            args += " --lave_max " + str(jobToProcess['localAvgMaxCutoff'])
        if  jobToProcess['localAvgMinCutoff']:
            args += " --lave_min " + str(jobToProcess['localAvgMinCutoff'])
        if  jobToProcess['lowPassFilter']:
            args += " --lp " + str(jobToProcess['lowPassFilter'])
        if  jobToProcess['highPassFilter']:
            args += " --hp " + str(jobToProcess['highPassFilter'])
        if  jobToProcess['doPreFilter'] == 'Yes':
            args += " --do_pre_filter"
        if  jobToProcess['preFilterLowPass']:
            args += " --pre_lp " + str(jobToProcess['preFilterLowPass'])
        if  jobToProcess['preFilterHighPass']:
            args += " --pre_hp " + str(jobToProcess['preFilterHighPass'])
        if  jobToProcess['detectIce']:
            args += " --detect_ice " + str(jobToProcess['detectIce'])
        if  jobToProcess['templateNormType']:
            args += " --T_norm_type " + str(jobToProcess['templateNormType'])
        if  jobToProcess['doBandpassFilter']:
            args += " --do_bandpass " + str(jobToProcess['doBandpassFilter'])
        if  jobToProcess['writeCrossCorrelationMrcs'] == 'Yes':
            args += " --write_ccmax_mic"
        if  jobToProcess['writePhaseFlippedMrcs'] == 'Yes':
            args += " --write_pf_mic"
        if  jobToProcess['writePreFilteredMrcs'] == 'Yes':
            args += " --write_pref_mic"
        if  jobToProcess['writeEstBackgroundMrcs'] == 'Yes':
            args += " --write_bg_mic"
        if  jobToProcess['writeBackgroundSubtractedMrcs'] == 'Yes':
            args += " --write_bgfree_mic"
        if  jobToProcess['writeLocalSigmaMrcs'] == 'Yes':
            args += " --write_lsigma_mic"
        if  jobToProcess['writeAutoDetectedMask'] == 'Yes':
            args += " --write_mic_mask"
        if  jobToProcess['pickByPreDefinedCoords'] == 'Yes':
            args += " --exclusive_picking"
        if  jobToProcess['excludedSuffixCoords']:
            args += " --excluded_suffix " + str(jobToProcess['excludedSuffixCoords'])
        if  jobToProcess['maskExcludedCoords'] == 'Yes':
            args += " --mask_excluded"
        if  jobToProcess['globalExcludedCoords']:
            args += " --global_box_excluded" + str(jobToProcess['globalExcludedCoords'])
        if  jobToProcess['doUnfinished'] == 'Yes':
            args += " --do_unfinished"
        if  jobToProcess['dontInvertTemplateContrast'] == 'Yes':
            args += " --dont_invertT"
        if  jobToProcess['extractRawParticle'] == 'Yes':
            args += " --extract_raw"
        if  jobToProcess['extractPhaseFlipped'] == 'Yes':
            args += " --extract_pf"
        if  jobToProcess['inMrc']:
            args += " " + jobToProcess['inMrc']
        return args
    
    #
    ## Job Maintenance functions
    #  --start--    
    
    # addJob() - builds the new job from the input variables and updates the job list.
    #
    def addJob(self, target):
        listedJobs = self.jobsList.options
        listedJobsList = list(listedJobs)
        newJob = self.buildJob("", "", self.jobCounter)
        #converting to tuple, update jobsList, jobNumber
        newJobTuple = (newJob,)
        listedJobsList.extend(newJobTuple)
        self.jobsList.options = listedJobsList
        self.jobCounter = self.jobCounter + 1
        self.jobNumber.value = ''

    # deleteJob() - delete selected jobs from the job list.
    #
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

    # runAllJobs() - execute all jobs in the list.
    #
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
    def selectJob(self, target):
        #obtain the selectedJobs
        selectedJobs = self.jobsList.value
        selectedJobsList = list(selectedJobs)

        #can only select a single job for updating.
        if  len(selectedJobsList) == 1:
            self.updateScreenFields(selectedJobsList[0])
    
    # updateJob() - update the job for the displayed job number
    #
    def updateJob(self, target):
        #obtain the listedJobs
        listedJobs = self.jobsList.options
        listedJobsList = list(listedJobs)
        #build updated job
        updatedJob = self.buildJob('', '', '')
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
    def buildAllWidgets(self):
        #Add fuctions to buttons.
        self.addButton.on_click(self.addJob)
        self.deleteButton.on_click(self.deleteJob)
        self.selectButton.on_click(self.selectJob)
        self.updateButton.on_click(self.updateJob)
        self.runAllButton.on_click(self.runAllJobs)

        buttons = HBox([self.addButton, self.deleteButton, self.selectButton, self.updateButton, self.runAllButton, self.runProgress])
        selectableTable = VBox([self.jobsList, buttons])

        inputWidgets = self.buildInputWidgets()

        return VBox([inputWidgets, selectableTable])

    #  --end--
    ## Job Maintenance functions
    #      
        