import os
import pickle
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Box, Label, Layout

#Workflow processing for all programs and jobs.

class workFlow:
    #Settings:
    outputFilename = 'workflowJobs.data'
    motionCorrFolderName = 'NBMotionCorr/'
    gctfFolderName       = 'NBCtfFind/'
    gautomatchFolderName = 'NBAutoPick/'
    
    #style and Layout
    styleBasic    = {'description_width': '120px'}
    styleAdvanced = {'description_width': '130px'}
    basicLayout   = Layout(width='60%')

    #Input fields for Motion Correction
    projectDirectory = widgets.Text(
        description='Project Directory: ',
        placeholder='Relion project directory',
        value='',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    mode = widgets.ToggleButtons(
        options=['Single Process', 'Workflow'],
        description='Mode:',
        disabled=False,
        button_style='',
        tooltips=['Run a separate processes', 'Run in workflow mode']
    )    
    
    loadButton = widgets.Button(
        description='Load jobs',
        disabled=False,
        button_style='',
        tooltip='Load all jobs',
        icon='check')

    saveButton = widgets.Button(
        description='Save jobs',
        disabled=False,
        button_style='',
        tooltip='Save all jobs',
        icon='check')

    errorText = widgets.Text(
        description='',
        placeholder='Errors',
        disabled=True,
        style=styleBasic,
        layout=basicLayout)    

    runAllButton = widgets.Button(
        description='Run all jobs',
        disabled=False,
        button_style='',
        tooltip='Run all workflow jobs',
        icon='check')

    runProgress = widgets.IntProgress(
        value=0, 
        min=0, 
        max=10, 
        step=1, 
        description='Progress:', 
        bar_style='', 
        orientation='horizontal')    
    #
    ## Job Maintenance fields
    #  --start--
    
    ##Debug assistance
    debug = widgets.Textarea(
        description='Debugging:',
        description_tooltip='Standard output',
        disabled=False,
        rows=10,
        style=styleBasic,
        layout=Layout(width='90%')) 
    
    motionCorrection = None
    gctf = None
    gautomatch = None
    
    # __init__() - initialise the class jobMaintenance
    #    Arguments:
    #        motionCorrection - an instance of the motionCorrection class
    #        ctf              - an instance of the gctf class
    #        gautomatch       - an instance of the gautomatch class
    #        showDebug        - display debug fields
    #    
    def __init__(self, motionCorrection, gctf, gautomatch, showDebug):
        self.motionCorrection = motionCorrection
        self.gctf = gctf
        self.gautomatch = gautomatch
        self.showDebug = showDebug
    
    #Load all jobs from file
    def loadJobs(self, target):
        #read the list, unpickle it.
        try:
            with open(self.projectDirectory.value + self.outputFilename, 'rb') as filehandle:
                # read the data as binary data stream
                allJobs = pickle.load(filehandle)
        except OSError as err:
                self.errorText.value = "OS error: {0}".format(err)
        else:
            filehandle.close()

            #extract each jobs list from allJobs.    
            self.motionCorrection.jobsList.options = list(allJobs[0])
            self.gctf.jobsList.options = list(allJobs[1])
            self.gautomatch.jobsList.options = list(allJobs[2])

            ##updating the JobNo as the notebook may have been restarted. ##
            #obtain the latest jobNumber
            lenMotionCorrJobs = len(allJobs[0])
            maxMotionCorrJobNo = allJobs[0][lenMotionCorrJobs -1]['jobNumber']
            #left strip the jobNumber by removing the jobPrefix, convert to int, add 1, assign to jobCounter.
            self.motionCorrection.jobCounter = int(maxMotionCorrJobNo.lstrip(self.motionCorrection.jobPrefix)) + 1

            #obtain the latest jobNumber
            lenGctfJobs = len(allJobs[1])
            maxGctfJobNo = allJobs[1][lenGctfJobs -1]['jobNumber']
            #left strip the jobNumber by removing the jobPrefix, convert to int, add 1, assign to jobCounter.
            self.gctf.jobCounter = int(maxGctfJobNo.lstrip(self.gctf.jobPrefix)) + 1

            #obtain the latest jobNumber
            lenGautomatchJobs = len(allJobs[2])
            maxGautomatchJobNo = allJobs[2][lenGautomatchJobs -1]['jobNumber']
            #left strip the jobNumber by removing the jobPrefix, convert to int, add 1, assign to jobCounter.
            self.gautomatch.jobCounter = int(maxGautomatchJobNo.lstrip(self.gautomatch.jobPrefix)) + 1
        
    #Save all jobs to file
    def saveJobs(self, target):
        mcListedJobs = list(self.motionCorrection.jobsList.options)
        gctfListedJobs = list(self.gctf.jobsList.options)
        gautoListedJobs = list(self.gautomatch.jobsList.options)

        #add the three lists to a new list
        allJobs = []
        allJobs.append(mcListedJobs)
        allJobs.append(gctfListedJobs)
        allJobs.append(gautoListedJobs)
                
        #saving the list - pickle it.
        try:
            with open(self.projectDirectory.value + self.outputFilename, 'wb') as filehandle:
                pickle.dump(allJobs, filehandle)
        except OSError as err:
                self.errorText.value = "OS error: {0}".format(err)
        else:
            filehandle.close()
            
    # singleProcess() - manage fields for single processing
    #
    def singleProcess(self):    
        #Motion Correction defaults
        self.motionCorrection.outMrc.disabled = False
        self.motionCorrection.outMrc.value = ''
        #CTF defaults
        self.gctf.inMrc.disabled = False
        self.gctf.inMrc.value = ''
        self.gctf.outMrc.disabled = False
        self.gctf.outMrc.value = ''        
        #Auto Piicking defaults
        self.gautomatch.inMrc.disabled = False
        self.gautomatch.inMrc.value = ''
        self.gautomatch.outMrc.disabled = False
        self.gautomatch.outMrc.value = ''        
        
    # workflowProcess() - manage fields for workflow processing
    #
    def workflowProcess(self):    
        #Motion Correction Defaults
        self.motionCorrection.outMrc.disabled = True
        self.motionCorrection.outMrc.value = self.motionCorrFolderName
        if  self.motionCorrection.frameDose.value == 0:
            self.errorText.value = "Motion Correction frame dose must be > 0"
        #CTF defaults
        self.gctf.inMrc.disabled = True
        self.gctf.inMrc.value = '*.mrc'
        self.gctf.outMrc.disabled = True
        self.gctf.outMrc.value = self.gctfFolderName
        if  self.gctf.doUnfinished.value == 0:
            self.errorText.value = "Contract Transfer Processing: Continue Processing must be 'Yes'"
        #Gautomatch defaults
        self.gautomatch.inMrc.disabled = True
        self.gautomatch.inMrc.value = '*.mrc'
        self.gautomatch.outMrc.disabled = True
        self.gautomatch.outMrc.value = self.gautomatchFolderName
        if  self.gautomatch.doUnfinished.value == 0:
            self.errorText.value = "Auto Match: Autopick unfinished mrcs must be 'Yes'"        

    # runWorkflowJobs() - Execute MotionCorr, Gctf and Gautomatch as a workflow.
    #
    def runWorkflowJobs(self, target):
        
        dirExists = False
        self.errorText.value= ''

        #Is the Notebook in Workflow mode?
        if  self.mode.value == 'Workflow':
        
            #validate Project Directory. Does it exist?
            try:
                if  os.path.isdir(self.projectDirectory.value) == True:
                    dirExists = True
                else:
                    self.errorText.value = "Project directory is not valid"
            except OSError as err:
                self.errorText.value = "OS error: {0}".format(err)        

            if  dirExists == True:

                #reset runProgress
                self.motionCorrection.runProgress.value = 0
                self.gctf.runProgress.value = 0
                self.gautomatch.runProgress.value = 0
                
                self.runProgress.max = 4
                self.runProgress.value = 1
                
                #runAllJobs for motionCorrection
                self.motionCorrection.runAllWorkflowJobs(self.projectDirectory.value)
                self.runProgress.value = 2
                
                #runAllJobs for Gctf
                self.gctf.runAllWorkflowJobs(self.projectDirectory.value, self.motionCorrFolderName)
                self.runProgress.value = 3
                
                #runAllJobs for Gautomatch
                #gautomatch uses motionCorr output for processing
                self.gautomatch.runAllWorkflowJobs(self.projectDirectory.value, self.motionCorrFolderName)
                self.runProgress.value = 4    
        else:
            self.errorText.value = "Must be in 'workflow' mode, ensure all jobs created in this mode"
        
    # on_click() - handle actions for the Mode button    
    #
    def on_click(self, change):
        if  self.mode.value == 'Single Process':
            #protect and fill fields as needed.
            self.singleProcess()
            
        if  self.mode.value == 'Workflow':
            self.workflowProcess()
            
    # buildInputWidgets() - write all the workflow fields to the screen.
    #
    def buildWidgets(self):
        #linking button on_click to function    
        self.loadButton.on_click(self.loadJobs)
        self.saveButton.on_click(self.saveJobs)
        self.runAllButton.on_click(self.runWorkflowJobs)

        self.mode.observe(self.on_click, 'value')    
        
        jobButtons = HBox([self.loadButton, self.saveButton, self.errorText])
        runBox = HBox([self.runAllButton, self.runProgress])
        
        advBoxLayout = Layout(display='flex',
                            flex_flow='row',
                            align_items='stretch',
                            border='none',
                            width='100%')
        
        if  self.showDebug:
            return VBox([self.debug, self.mode, self.projectDirectory, jobButtons, runBox])
        else:
            return VBox([self.mode, self.projectDirectory, jobButtons, runBox])
