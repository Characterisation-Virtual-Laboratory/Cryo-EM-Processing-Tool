import os
import glob
import ipywidgets as widgets
import jobMaintenance as jm
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
    basicLayout   = Layout(width='70%')
    advLayout     = Layout(width='100%')
    errorLayout   = Layout(width='60%', border='2px solid red')

    #Input fields for Motion Correction
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

    pixelSize = widgets.FloatSlider(
        value=1.34,
        min=0,
        max=4.0,
        step=0.01,
        description='Pixel size (A): ',
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

    particlePickingTemplatesMulti = widgets.Text(
        value='',
        placeholder='Use ";" as separator.',
        description='Particle pick templ list: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    particlePickingTemplatesMultiButton = widgets.Button(
        description='Add jobs',
        disabled=False,
        button_style='',
        tooltip='Add multiple jobs',
        icon='check')

    pixelSizeTemplate = widgets.FloatSlider(
        value=1.34,
        min=0,
        max=4.0,
        step=0.01,
        description='Pixel size template (A): ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.2f',
        style=styleBasic,
        layout=basicLayout)

    pixelSizeTemplateMulti = widgets.Text(
        value='',
        placeholder='Use ";" as separator.',
        description='Pixel size templ list: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    pixelSizeTemplateMultiButton = widgets.Button(
        description='Add jobs',
        disabled=False,
        button_style='',
        tooltip='Add multiple jobs',
        icon='check')

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
        description='Angular step size: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    speedLevel = widgets.Select(
        options=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')],
        description='Speed level: ',
        disabled=False,
        value='2',
        style=styleAdvanced,
        layout=advLayout)

    boxSize = widgets.IntText(
        description='Box size (pixel): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    minDistance = widgets.IntText(
        description='Minimum distance (A): ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    crossCorrelationCutoff = widgets.FloatSlider(
        value=0.1,
        min=0,
        max=1,
        step=0.1,
        description='Cross correlation cutoff: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)

    localSigmaDiameter = widgets.IntText(
        description='Local sigma diameter (A): ',
        value=200,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    localSigmaCutoff = widgets.FloatSlider(
        value=1.3,
        min=0,
        max=4,
        step=0.1,
        description='Local sigma cutoff: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleAdvanced,
        layout=advLayout)

    localAvgDiameter = widgets.IntText(
        description='Local avg diameter (A): ',
        value=400,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    localAvgMaxCutoff = widgets.FloatSlider(
        value=2.0,
        min=0,
        max=20,
        step=0.1,
        description='Local avg max cutoff: ',
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
        description='Local avg min cutoff: ',
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
        description='Low pass filter: ',
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
        description='High pass filter: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    doPreFilter = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Do pre filter: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    preFilterLowPass = widgets.IntSlider(
        value=8,
        min=0,
        max=100,
        step=1,
        description='Pre filter - low pass: ',
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
        description='Pre filter - high pass: ',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    detectIce = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='1',
        description='Detect ice: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    templateNormType = widgets.Select(
        options=[('1', '1'), ('2', '2'), ('3', '3')],
        value='1',
        description='Template norm. type: ',
        disabled=False,
        rows=3,
        style=styleAdvanced,
        layout=advLayout)

    doBandpassFilter = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='1',
        description='Do bandpass filter: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    #I/O Options
    writeCrossCorrelationMrcs = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Write cross correlation: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    writePhaseFlippedMrcs = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Write phase flipped: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    writePreFilteredMrcs = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Write pre filtered: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    writeEstBackgroundMrcs = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Write est background: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    writeBackgroundSubtractedMrcs = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Write background subtracted: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    writeLocalSigmaMrcs = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Write local sigma: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    writeAutoDetectedMask = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Write auto detected mask: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    pickByPreDefinedCoords = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Exclusive picking: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    excludedSuffixCoords = widgets.Text(
        placeholder='path for input Relion .star or EMAN .box file containing excluded suffix coordinates',
        description='Excluded suffix coords: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    maskExcludedCoords = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Mask excluded coords: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    globalExcludedCoords = widgets.Text(
        placeholder='path for .star or .box file containing coordinates to exclude from all mrcs',
        description='Global excluded coords: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    doUnfinished = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='1',
        description='Autopick unfinished mrcs: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    dontInvertTemplateContrast = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description="Don't invert template contrast: ",
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    extractRawParticle = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
        description='Extract particle from raw mrc: ',
        disabled=False,
        rows=2,
        style=styleAdvanced,
        layout=advLayout)

    extractPhaseFlipped = widgets.Select(
        options=[('No', '0'), ('Yes', '1')],
        value='0',
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
        self.jobMaint  = jm.jobMaintenance(self.header, self.jobNumber, self.buildJob, self.buildNewJobs,  self.buildArgumentsList, self.updateScreenFields, callProgramFunc, self.program)

    # runSingleJob() - execute single job
    #
    @debug.capture(clear_output=True)
    def runSingleJob(self, target):
        self.jobMaint.runProgress.max = 2
        self.jobMaint.runProgress.value = 1
        self.callProgram(self.program, self.buildArgumentsList(self.buildJob(self.jobNumber, '', '')), self.outMrc.value)
        self.jobMaint.runProgress.value = self.jobMaint.runProgress.max

    #Multi value field processing support
    # addParticlePickingTemplateJobs() - add new jobs for all 'Particle Picking Template' values entered
    #
    @debug.capture(clear_output=True)
    def addParticlePickingTemplateJobs(self, target):
        self.jobMaint.addJobs("particlePickingTemplates", self.particlePickingTemplatesMulti.value)

    # addPixelSizeTemplateJobs() - add new jobs for all 'Pixel Size Template' values entered.
    #
    @debug.capture(clear_output=True)
    def addPixelSizeTemplateJobs(self, target):
        self.jobMaint.addJobs("pixelSizeTemplate", self.pixelSizeTemplate.value)

    # buildInputWidgets() - write all the Auto Match input fields to the screen.
    #
    @debug.capture(clear_output=True)
    def buildInputWidgets(self):
        #linking button on_click to function
        self.runButton.on_click(self.runSingleJob)

        self.particlePickingTemplatesMultiButton.on_click(self.addParticlePickingTemplateJobs)
        self.pixelSizeTemplateMultiButton.on_click(self.addPixelSizeTemplateJobs)

        particlePickingTemplatesInputs = HBox([self.particlePickingTemplates, self.particlePickingTemplatesMulti, self.particlePickingTemplatesMultiButton])
        pixelSizeTemplateInputs = HBox([self.pixelSizeTemplate, self.pixelSizeTemplateMulti, self.pixelSizeTemplateMultiButton])

        basic      = VBox([self.jobNumber, self.inMrc, self.outMrc, self.pixelSize, self.diameter, particlePickingTemplatesInputs,
                           pixelSizeTemplateInputs, self.gpu])

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

        tab = widgets.Tab(children=[basic, additional, io1])
        tab.set_title(0, 'Basic')
        tab.set_title(1, 'Additional')
        tab.set_title(2, 'I/O')

        if  self.showDebug:
            return VBox([self.debug, self.debugText, tab, self.runButton])
        else:
            return VBox([self.debug, tab, self.runButton])

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
            newJob = self.buildJob(self.jobMaint.jobCounter, '', '')
            self.jobMaint.jobCounter += 1
            return newJob

        """Determine range values for gautomatch        """
        #Building multiple jobs
        if  fieldName == 'particlePickingTemplates':
            fieldList = self.particlePickingTemplatesMulti.value.split(";")
        if  fieldName == 'pixelSizeTemplate':
            fieldList = self.pixelSizeTemplateMulti.value.split(";")

        for i in range(len(fieldList)):
            fieldCleaned = fieldList[i].strip()

            if  fieldCleaned:
                if  fieldName == 'particlePickingTemplates':
                    newJob = self.buildJob(self.jobMaint.jobCounter, fieldCleaned, '')

                if  fieldName == 'pixelSizeTemplate':
                    newJob = self.buildJob(self.jobMaint.jobCounter, '', fieldCleaned)

                self.jobMaint.jobCounter += 1
                jobList.append(newJob)

        return jobList

    # buildJob() - construct a single job containing all arguments.
    #    Arguments:
    #        particlePickingTemplatesValue - use the value if specified, otherwise use screen value
    #        pixelSizeTemplateValue - use the value if specified, otherwise use screen value
    #        jobNo - the next job number to use
    #    Return:
    #        dict containing all arguments.
    #
    @debug.capture(clear_output=True)
    def buildJob(self,  jobNo='', particlePickingTemplatesValue='', pixelSizeTemplateValue=''):

        jobNoWithPrefix = self.jobPrefix + str(jobNo)
        if  jobNo:
            newJob = {'jobNumber':jobNoWithPrefix}
        else:
            newJob = {'jobNumber':self.jobNumber.value}

        newJob['inMrc']                         = self.inMrc.value
        newJob['outMrc']                        = self.outMrc.value
        newJob['pixelSize']                     = self.pixelSize.value
        newJob['diameter']                      = self.diameter.value

        if  particlePickingTemplatesValue:
            newJob['particlePickingTemplates']  = particlePickingTemplatesValue
        else:
            newJob['particlePickingTemplates']  = self.particlePickingTemplates.value

        if  pixelSizeTemplateValue:
            newJob['pixelSizeTemplate']         = pixelSizeTemplateValue
        else:
            newJob['pixelSizeTemplate']         = self.pixelSizeTemplate.value

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
    @debug.capture(clear_output=True)
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
    @debug.capture(clear_output=True)
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
        if  jobToProcess['doPreFilter']:
            args += " --do_pre_filter " + jobToProcess['doPreFilter']
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
        if  jobToProcess['writeCrossCorrelationMrcs']:
            args += " --write_ccmax_mic " + jobToProcess['writeCrossCorrelationMrcs']
        if  jobToProcess['writePhaseFlippedMrcs']:
            args += " --write_pf_mic " + jobToProcess['writePhaseFlippedMrcs']
        if  jobToProcess['writePreFilteredMrcs']:
            args += " --write_pref_mic " + jobToProcess['writePreFilteredMrcs']
        if  jobToProcess['writeEstBackgroundMrcs']:
            args += " --write_bg_mic " + jobToProcess['writeEstBackgroundMrcs']
        if  jobToProcess['writeBackgroundSubtractedMrcs']:
            args += " --write_bgfree_mic " + jobToProcess['writeBackgroundSubtractedMrcs']
        if  jobToProcess['writeLocalSigmaMrcs']:
            args += " --write_lsigma_mic " + jobToProcess['writeLocalSigmaMrcs']
        if  jobToProcess['writeAutoDetectedMask']:
            args += " --write_mic_mask " + jobToProcess['writeAutoDetectedMask']
        if  jobToProcess['pickByPreDefinedCoords']:
            args += " --exclusive_picking " + jobToProcess['pickByPreDefinedCoords']
        if  jobToProcess['excludedSuffixCoords']:
            args += " --excluded_suffix " + str(jobToProcess['excludedSuffixCoords'])
        if  jobToProcess['maskExcludedCoords']:
            args += " --mask_excluded " + jobToProcess['maskExcludedCoords']
        if  jobToProcess['globalExcludedCoords']:
            args += " --global_box_excluded" + str(jobToProcess['globalExcludedCoords'])
        if  jobToProcess['doUnfinished']:
            args += " --do_unfinished " + jobToProcess['doUnfinished']
        if  jobToProcess['dontInvertTemplateContrast']:
            args += " --dont_invertT " + jobToProcess['dontInvertTemplateContrast']
        if  jobToProcess['extractRawParticle']:
            args += " --extract_raw " + jobToProcess['extractRawParticle']
        if  jobToProcess['extractPhaseFlipped']:
            args += " --extract_pf " + jobToProcess['extractPhaseFlipped']
        if  jobToProcess['inMrc']:
            args += " " + jobToProcess['inMrc']
        return args

    # buildSymlinks() - used for 'Workflow' mode. Builds a list of symlinks to output
    #                   micrographs from motioncorr in preparation for gautomatch processing.
    #    Arguments:
    #        projectDirectory - contains the home directory of the Relion project for all jobs.
    #        motionCorrFolder - contains the output folder for motionCorr jobs. Used to build symlinks
    #                      for gautomatch input
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
    #        projectDirectory  - Contains the home directory of the Relion project for all jobs.
    #        motionCorrFolder  - contains the motionCorr2 output folder
    #
    @debug.capture(clear_output=True)
    def runAllWorkflowJobs(self, projectDirectory, motionCorrFolder):
        #obtain the listedJobs
        listedJobs = self.jobMaint.jobsList.options
        listedJobsList = list(listedJobs)

        self.jobMaint.runProgress.max = len(listedJobsList)

        if  projectDirectory.endswith('/') == False:
            projectDirectory += '/'

        self.errorText.layout = self.basicLayout

        #Run each job, but not the Header row.
        for i in range(len(listedJobsList)):
            #setting progress bar to show job has started running.
            if  (str(listedJobsList[i]).startswith('Job#') == True):
                self.jobMaint.runProgress.value = i+1

            if  (str(listedJobsList[i]).startswith('Job#') == False):
                #'Workflow' mode
                outputFolder = projectDirectory + listedJobsList[i]['outMrc'] + listedJobsList[i]['jobNumber'] + '/Micrographs/'
                try:
                    #mkdir -p path, if folder exists, that's OK
                    os.makedirs(outputFolder, exist_ok=True)

                    #change working directory
                    os.chdir(outputFolder)

                    #create symlinks to output *.mrc from motionCorr jobs
                    #these are then used as input to gautomatch
                    self.buildSymlinks(projectDirectory, motionCorrFolder)

                except OSError as err:
                    self.errorText.value = "Unable to setup processing structure: {0}".format(err) + '\n'
                    self.errorText.layout = self.errorLayout
                else:
                    #build arguments list, run program
                    self.callProgram(self.program, self.buildArgumentsList(listedJobsList[i]), outputFolder)
                self.jobMaint.runProgress.value = i+1

    # buildAllWidgets() - display the jobs list and associated buttons.
    #
    @debug.capture(clear_output=True)
    def buildAllWidgets(self):
        selectableTable = VBox([self.jobMaint.buildJobWidgets(), self.errorText])
        inputWidgets = self.buildInputWidgets()

        return VBox([inputWidgets, selectableTable])
