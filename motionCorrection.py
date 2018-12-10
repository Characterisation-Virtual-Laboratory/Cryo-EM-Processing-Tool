import os
import glob
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Box, Label, Layout

#Motion Correction input fields and functions to execute jobs

class motionCorrection:
    #Settings:
    program = 'motioncor2'
    jobPrefix = 'mc'
    #used to strip the micrograph filename to build output filename prefix
    stripOutputName = ['Micrographs/', '_movies.mrcs']
    header = [("Job# | inMrc | outMrc | pixelSize | patch | bFactor | voltage | gainFile |  gpu | inTiff | fullSum | defectFile | processing | iteration | tolerance | stack | binningFactor | initDose | frameDose | throw | trunc | group | fmRef | tilt | rotGain | flipGain |")]    
    
    #style and Layout
    styleBasic    = {'description_width': '120px'}
    styleAdvanced = {'description_width': '130px'}
    basicLayout   = Layout(width='60%')
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
        placeholder='mrc file, folder containing mrc files or .star file',
        description='Input: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    outMrc = widgets.Text(
        value='',
        placeholder='path for output mrc file',
        description='Output: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    gainFile = widgets.Text(
        placeholder='path for mrc file that stores the gain reference',
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

    patchMulti = widgets.Text(
        placeholder='Use ";" as separator. e.g. 3 3; 5 5; ',
        description='Patch list: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    patchMultiButton = widgets.Button(
        description='Add jobs',
        disabled=False,
        button_style='',
        tooltip='Add multiple jobs',
        icon='check')

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

    bFactorMulti = widgets.Text(
        placeholder='Use ";" as separator. e.g. 100; 235; 350',
        description='bFactor list: ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    bFactorMultiButton = widgets.Button(
        description='Add jobs',
        disabled=False,
        button_style='',
        tooltip='Add multiple jobs',
        icon='check')

    pixelSize = widgets.FloatSlider(
        value=0.5,
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

    voltage = widgets.IntText(
        value=300,
        description='Voltage (kV): ',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    gpu = widgets.Text(
        value='',
        placeholder='indicate the GPUs to use',
        description='GPU usage: ',
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
        description='Defect file: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    processing = widgets.Select(
        options=[('Serial', 1), ('Single', 0)],
        description='Processing type: ',
        disabled=False,
        style=styleAdvanced,
        rows=2,
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
        description='Binning factor',
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
        description='Initial dose (e/A2)',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d',
        style=styleAdvanced,
        layout=advLayout)

    frameDose = widgets.FloatSlider(
        value=1.0,
        min=0,
        max=3.0,
        step=0.1,
        description='Frame dose (e/A2):',
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style=styleBasic,
        layout=basicLayout)

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
        options=[('Central', 1), ('First', 0)],
        description='Reference frame: ',
        disabled=False,
        style=styleAdvanced,
        rows=2,
        layout=advLayout)

    tilt = widgets.Text(
        value='',
        placeholder='specify the starting angle followed by the tilt step. e.g. 0 2',
        description='Tilt angle and step: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    rotGain = widgets.Select(
        options=[('No rotation - default', 0), ('Rotate 90', 1), ('Rotate 180', 2), ('Rotate 270', 3)],
        description='Rotate gain: ',
        disabled=False,
        rows=4,
        style=styleAdvanced,
        layout=advLayout)

    flipGain = widgets.Select(
        options=[('No flip - default', 0), ('upside down - horizontal axis', 1), ('left right - vertical axis', 2)],
        description='Flip gain ',
        disabled=False,
        rows=3,
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
        description='Run all',
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
    
    # __init__() - initialise the class motionCorrection
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
        self.callProgram(self.program, self.buildArgumentsList(self.buildJob('', '', self.jobNumber), '', ''), self.outMrc.value) 
        self.runProgress.value = self.runProgress.max
    
    #Multi value field processing support
    # addPatchJobs() - add new jobs for all 'Patch' values entered
    #
    @debug.capture(clear_output=True)
    def addPatchJobs(self, target):
        self.addJobs("patch", self.patchMulti.value)

    # addBFactorJobs() - add new jobs for all 'BFactor' values entered.
    #
    @debug.capture(clear_output=True)
    def addBFactorJobs(self, target):
        self.addJobs("bFactor", self.bFactorMulti.value)

    # buildInputWidgets() - write all the Motion Correction input fields to the screen.
    #
    @debug.capture(clear_output=True)
    def buildInputWidgets(self):
        #linking button on_click to function    
        self.runButton.on_click(self.runSingleJob)
        self.patchMultiButton.on_click(self.addPatchJobs)
        self.bFactorMultiButton.on_click(self.addBFactorJobs)        
        
        patchInputs = HBox([self.patch, self.patchMulti, self.patchMultiButton])
        bFactorInputs = HBox([self.bFactor, self.bFactorMulti, self.bFactorMultiButton])    

        basic = VBox([self.jobNumber, self.inMrc, self.outMrc, self.pixelSize, patchInputs, bFactorInputs, self.voltage, self.gainFile, self.gpu, self.frameDose])
        advanced1 = VBox([self.inTiff, self.fullSum, self.defectFile, self.iteration, self.tolerance, self.stack, self.binningFactor, self.initDose, self.throw, self.trunc, self.group])
        advanced2 = VBox([self.processing, self.fmRef, self.tilt, self.rotGain, self.flipGain])

        advBoxLayout = Layout(display='flex',
                            flex_flow='row',
                            align_items='stretch',
                            border='none',
                            width='100%')
        advanced = Box(children=[advanced1, advanced2], layout=advBoxLayout)
        tab = widgets.Tab(children=[basic, advanced])
        tab.set_title(0, 'Basic')
        tab.set_title(1, 'Advanced')
        
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
        if  fieldName == 'patch':
            fieldList = self.patchMulti.value.split(";")
        if  fieldName == 'bFactor':
            fieldList = self.bFactorMulti.value.split(";")
            
        for i in range(len(fieldList)):
            fieldCleaned = fieldList[i].strip()
            
            if  fieldCleaned:
                if  fieldName == 'patch':
                    newJob = self.buildJob(fieldCleaned, '', self.jobCounter)

                if  fieldName == 'bFactor':
                    newJob = self.buildJob('', fieldCleaned, self.jobCounter)

                self.jobCounter = self.jobCounter + 1
                jobList.append(newJob)                    

        return jobList
        
    # buildJob() - construct a single job containing all arguments.
    #    Arguments:
    #        patchValue - use the patchValue is specified, otherwise use screen value
    #        bFactorValue - use the bFactorValue if specified, otherwise use screen value
    #        jobNo - the next job number to use
    #    Return:
    #        dict containing all arguments.
    #
    @debug.capture(clear_output=True)
    def buildJob(self, patchValue, bFactorValue, jobNo):
        
        jobNoWithPrefix = self.jobPrefix + str(jobNo)
        if  jobNo:
            newJob = {'jobNumber':jobNoWithPrefix}
        else:
            newJob = {'jobNumber':self.jobNumber.value}

        newJob['inMrc']         = self.inMrc.value
        newJob['outMrc']        = self.outMrc.value
        newJob['pixelSize']     = self.pixelSize.value

        if  patchValue:
            newJob['patch']     = patchValue
        else:    
            newJob['patch']     = self.patch.value

        if  bFactorValue:
            newJob['bFactor']   = bFactorValue 
        else:
            newJob['bFactor']   = self.bFactor.value 

        newJob['voltage']       = self.voltage.value   
        newJob['gainFile']      = self.gainFile.value
        newJob['gpu']           = self.gpu.value
        newJob['inTiff']        = self.inTiff.value
        newJob['fullSum']       = self.fullSum.value
        newJob['defectFile']    = self.defectFile.value
        newJob['processing']    = self.processing.value
        newJob['iteration']     = self.iteration.value
        newJob['tolerance']     = self.tolerance.value   
        newJob['stack']         = self.stack.value
        newJob['binningFactor'] = self.binningFactor.value   
        newJob['initDose']      = self.initDose.value   
        newJob['frameDose']     = self.frameDose.value
        newJob['throw']         = self.throw.value   
        newJob['trunc']         = self.trunc.value   
        newJob['group']         = self.group.value   
        newJob['fmRef']         = self.fmRef.value
        newJob['tilt']          = self.tilt.value   
        newJob['rotGain']       = self.rotGain.value
        newJob['flipGain']      = self.flipGain.value
        return newJob

    # updateScreenFields() - updates screen fields using supplied dict.
    #    Arguments:
    #        selectedJob - a dict containing all screen values.
    #
    @debug.capture(clear_output=True)
    def updateScreenFields(self, selectedJob):
        self.jobNumber.value     = selectedJob['jobNumber']
        self.inMrc.value         = selectedJob['inMrc']
        self.outMrc.value        = selectedJob['outMrc']
        self.pixelSize.value     = selectedJob['pixelSize']
        self.patch.value         = selectedJob['patch']
        self.bFactor.value       = selectedJob['bFactor']
        self.voltage.value       = selectedJob['voltage']
        self.gainFile.value      = selectedJob['gainFile']
        self.gpu.value           = selectedJob['gpu']
        self.inTiff.value        = selectedJob['inTiff']
        self.fullSum.value       = selectedJob['fullSum']
        self.defectFile.value    = selectedJob['defectFile']
        self.processing.value    = selectedJob['processing']
        self.iteration.value     = selectedJob['iteration']
        self.tolerance.value     = selectedJob['tolerance']
        self.stack.value         = selectedJob['stack']
        self.binningFactor.value = selectedJob['binningFactor']
        self.initDose.value      = selectedJob['initDose']
        self.frameDose.value     = selectedJob['frameDose']
        self.throw.value         = selectedJob['throw']
        self.trunc.value         = selectedJob['trunc']
        self.group.value         = selectedJob['group']
        self.fmRef.value         = selectedJob['fmRef']
        self.tilt.value          = selectedJob['tilt']
        self.rotGain.value       = selectedJob['rotGain']
        self.flipGain.value      = selectedJob['flipGain']

    # buildArgumentsList() - builds a string of arguments for calling Motion Correction.
    #    Arguments:
    #        jobToProcess - a dict containing all screen values.
    #        inputFile - full path for file to process. Required when processing 
    #                    *.star file in 'Workflow' mode
    #        prefixName - prefix used to create the output file. Required for 'Workflow'
    #                     mode.
    @debug.capture(clear_output=True)
    def buildArgumentsList(self, jobToProcess, inputFile, prefixName):
        args = ''

        if  inputFile:
            args += " -InMrc " + inputFile
        elif jobToProcess['inMrc'] is not '':
            args += " -InMrc " + jobToProcess['inMrc']

        if  jobToProcess['inTiff'] is not '':
            args += " -InTiff " + jobToProcess['inTiff']

        #inputFile is populated, so we are in 'Workflow' mode
        if  inputFile:
            args += " -OutMrc " + jobToProcess['outMrc'] + jobToProcess['jobNumber'] + '/Micrographs/' + prefixName
        elif  jobToProcess['outMrc'] is not '':
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
            args += " -Serial " + str(jobToProcess['processing'])
        if  jobToProcess['fmRef'] is not '':
            args += " -FmRef " + str(jobToProcess['fmRef'])
        if  jobToProcess['rotGain'] is not '':
            args += " -RotGain " + str(jobToProcess['rotGain'])
        if  jobToProcess['flipGain'] is not '':
            args += " -FlipGain " + str(jobToProcess['flipGain'])
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
    
    #
    ## Job Maintenance functions
    #  --start--    
    
    # addJob() - builds the new job from the input variables and updates the job list.
    #
    @debug.capture(clear_output=True)
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

    # loadMicrographs() - read the star file to obtain a list of micrographs
    #                      processing
    #    Arguments:
    #         projectDirectory - contains the home directory for the Relion project
    #         starFilePath     - the relative path to the star file
    #    Return:
    #         a list of micrographs.
    #
    @debug.capture(clear_output=True)
    def loadMicrographs(self, projectDirectory, starFilePath):
        foundDataBlock = False
        foundLoopBlock = False
        foundColumns   = False
        micrographs = []
        
        #open *.star file and read micrographs into list.
        fileFullPath = projectDirectory + starFilePath
        
        self.errorText.layout = self.basicLayout
        
        try:
            with open(fileFullPath, 'r') as filehandle: 
                for line in filehandle:
                    if  line.startswith('data_'):
                        foundDataBlock = True
                    elif line.startswith('loop_'):
                        foundLoopBlock = True
                    elif line.startswith('_rln'):
                        foundColumns = True
                    elif foundDataBlock and foundLoopBlock and foundColumns:
                        #right strip newlines chars then add to list.
                        micrographs.append(line.rstrip())
        except OSError as err:
            self.errorText.value += "Unable to load Micrographs: {0}".format(err) + '\n'
            self.errorText.layout = self.errorLayout
        else:
            filehandle.close()            

        return micrographs
    
    # runAllWorkflowJobs() - execute all jobs in the list. Only executed in 'workflow' mode
    #    Arguments:
    #        projectDirectory  - contains the home directory of the Relion project for all jobs.
    #
    @debug.capture(clear_output=True)
    def runAllWorkflowJobs(self, projectDirectory):
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
                micrographs = self.loadMicrographs(projectDirectory, listedJobsList[i]['inMrc'])

                outputFolder = projectDirectory + listedJobsList[i]['outMrc'] + listedJobsList[i]['jobNumber'] + '/Micrographs/'
                try:
                    #mkdir -p path, if folder exists, that's OK
                    os.makedirs(outputFolder, exist_ok=True)

                    #change working directory
                    os.chdir(projectDirectory)
                except OSError as err:
                    self.errorText.value += "Unable to build folder: {0}".format(err) + '\n'
                    self.errorText.layout = self.errorLayout
                else:    
                    #run for each micrograph in .star file
                    for j in range(len(micrographs)):
                        #determine output filename prefix.
                        prefix = micrographs[j].rstrip(self.stripOutputName[1])
                        prefix = prefix.lstrip(self.stripOutputName[0])

                        #already processed ?
                        if  glob.glob(outputFolder + '/' + prefix + '*'): 
                            continue
                        else:
                            #build arguments list, run program
                            self.callProgram(self.program, self.buildArgumentsList(listedJobsList[i], micrographs[j], prefix), 
                                             outputFolder)

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
                self.callProgram(self.program, self.buildArgumentsList(listedJobsList[i], '', ''), listedJobsList[i]['outMrc'])
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
        