import glob
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import ipywidgets as widgets
import threading
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
    errorLayout    = Layout(width='60%', border='2px solid red')

    #Input fields for Workflow
    projectDirectory = widgets.Text(
        description='Project Directory: ',
        placeholder='Relion project directory',
        value='',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    mode = widgets.ToggleButtons(
        options=['Single', 'Workflow'],
        value='Workflow',
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

    displayGraphs = widgets.RadioButtons(
            options=(['Disable', 'Enable']),
            description='Display graphs:',
            value='Enable',
            tooltip='Display graphs after job run',
            disabled=False,
            style=styleBasic)    

    graphBox = widgets.Output(
        layout={'border': '2px solid black'})
    
    ## AutoRun fields - thread control
    ## Start
    enableAutoRun = widgets.RadioButtons(
            options=(['Disable', 'Enable']),
            description='Auto run:',
            disabled=False,
            style=styleBasic)

    startAutoRun = widgets.Button(
        description='Start auto run',
        description_tooltip='Start auto execution',
        disabled=False,
        style=styleBasic)

    runDelay = widgets.IntText(
        value=5,
        description='Pause run (mins): ',
        description_tooltip='Auto run after a pause in minutes',
        disabled=False,
        style=styleBasic)

    stopAutoRun = widgets.Button(
        description='Stop auto run',
        description_tooltip='Stop auto execution',
        disabled=False,
        style=styleBasic)    

    #thread performing autoRun
    threadAutoRun  = None
    #thread event - controls running of the thread e.g. stop/start.
    threadAutoRun_stop = threading.Event()
    
    ## End
    
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
        #default to 'workflow' mode
        self.workflowProcess()
    
    #Load all jobs from file
    @debug.capture(clear_output=True)
    def loadJobs(self, target):
        
        if  self.projectDirectory.value.endswith('/') == False:
            self.projectDirectory.value += '/'
            
        self.errorText.layout = self.basicLayout
        #read the list, unpickle it.
        try:
            with open(self.projectDirectory.value + self.outputFilename, 'rb') as filehandle:
                # read the data as binary data stream
                allJobs = pickle.load(filehandle)
        except OSError as err:
                self.errorText.value = "OS error: {0}".format(err)
                self.errorText.layout = self.errorLayout
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
    @debug.capture(clear_output=True)
    def saveJobs(self, target):
        mcListedJobs = list(self.motionCorrection.jobsList.options)
        gctfListedJobs = list(self.gctf.jobsList.options)
        gautoListedJobs = list(self.gautomatch.jobsList.options)

        #add the three lists to a new list
        allJobs = []
        allJobs.append(mcListedJobs)
        allJobs.append(gctfListedJobs)
        allJobs.append(gautoListedJobs)

        if  self.projectDirectory.value.endswith('/') == False:
            self.projectDirectory.value += '/'        
        
        self.errorText.layout = self.basicLayout
        #saving the list - pickle it.
        try:
            with open(self.projectDirectory.value + self.outputFilename, 'wb') as filehandle:
                pickle.dump(allJobs, filehandle)
        except OSError as err:
                self.errorText.value = "OS error: {0}".format(err)
                self.errorText.layout = self.errorLayout
        else:
            filehandle.close()
            
    # singleProcess() - manage fields for single processing
    #
    @debug.capture(clear_output=True)
    def singleProcess(self):    
        #Motion Correction defaults
        self.motionCorrection.outMrc.disabled = False
        self.motionCorrection.outMrc.value = ''
        self.motionCorrection.runButton.disabled=False
        self.motionCorrection.runAllButton.disabled=False
        #CTF defaults
        self.gctf.inMrc.disabled = False
        self.gctf.inMrc.value = ''
        self.gctf.outMrc.disabled = False
        self.gctf.outMrc.value = ''        
        self.gctf.runButton.disabled=False
        self.gctf.runAllButton.disabled=False
        #Auto Piicking defaults
        self.gautomatch.inMrc.disabled = False
        self.gautomatch.inMrc.value = ''
        self.gautomatch.outMrc.disabled = False
        self.gautomatch.outMrc.value = ''        
        self.gautomatch.runButton.disabled=False
        self.gautomatch.runAllButton.disabled=False

        
    # workflowProcess() - manage fields for workflow processing
    #
    @debug.capture(clear_output=True)
    def workflowProcess(self):    
        self.errorText.layout = self.basicLayout
        #Motion Correction Defaults
        self.motionCorrection.outMrc.disabled = True
        self.motionCorrection.outMrc.value = self.motionCorrFolderName
        if  self.motionCorrection.frameDose.value == 0:
            self.errorText.value = "Motion Correction frame dose must be > 0"
            self.errorText.layout= self.errorLayout
        self.motionCorrection.runButton.disabled=True
        self.motionCorrection.runAllButton.disabled=True
        #CTF defaults
        self.gctf.inMrc.disabled = True
        self.gctf.inMrc.value = '*.mrc'
        self.gctf.outMrc.disabled = True
        self.gctf.outMrc.value = self.gctfFolderName
        if  self.gctf.doUnfinished.value == 0:
            self.errorText.value = "Contract Transfer Processing: Continue Processing must be 'Yes'"
            self.errorText.layout = self.errorLayout
        self.gctf.runButton.disabled=True
        self.gctf.runAllButton.disabled=True
        #Gautomatch defaults
        self.gautomatch.inMrc.disabled = True
        self.gautomatch.inMrc.value = '*.mrc'
        self.gautomatch.outMrc.disabled = True
        self.gautomatch.outMrc.value = self.gautomatchFolderName
        if  self.gautomatch.doUnfinished.value == 0:
            self.errorText.value = "Auto Match: Autopick unfinished mrcs must be 'Yes'"
            self.errorText.layout = self.errorLayout
        self.gautomatch.runButton.disabled=True
        self.gautomatch.runAllButton.disabled=True

    # runWorkflowJobs() - Execute MotionCorr, Gctf and Gautomatch as a workflow.
    #
    @debug.capture(clear_output=True)
    def runWorkflowJobs(self, target):
        
        dirExists = False
        self.errorText.value= ''
        self.errorText.layout = self.basicLayout

        #Is the Notebook in Workflow mode?
        if  self.mode.value == 'Workflow':
        
            #validate Project Directory. Does it exist?
            try:
                if  os.path.isdir(self.projectDirectory.value) == True:
                    dirExists = True
                else:
                    self.errorText.value = "Project directory is not valid"
                    self.errorText.layout = self.errorLayout
            except OSError as err:
                self.errorText.value = "OS error: {0}".format(err)        
                self.errorText.layout = self.errorLayout

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
                
                self.graphBox.clear_output()
                if  self.displayGraphs.value == 'Enable':
                    self.buildGraphs()
        else:
            self.errorText.value = "Must be in 'workflow' mode, ensure all jobs created in this mode"
            self.errorText.layout = self.errorLayout

    # buildGraphs() - display a histogram for each ctf job.
    #
    @debug.capture(clear_output=True)
    def buildGraphs(self):
        ctfStarFilePath = glob.glob(self.projectDirectory.value + self.gctfFolderName + '*/micrographs_ctf.star')
        
        if  len(ctfStarFilePath) > 0:
            rowItemMax = 2
            maxRows = math.ceil(len(ctfStarFilePath) / rowItemMax)

            plt.close('all')
            fig, axes = plt.subplots(nrows=maxRows, ncols=rowItemMax)

            for i in range(len(ctfStarFilePath)):
                split = ctfStarFilePath[i].rsplit('/', 2)
                #create a numpy array from .star file using col 12 MaxCtfResolution
                ctfData = np.loadtxt(ctfStarFilePath[i], skiprows=17, usecols=12)

                axes[i].set_title("Job: " + split[1])
                axes[i].set_ylabel('Probablity')
                axes[i].set_xlabel("Max CTF resolution (A)")
                axes[i].hist(ctfData, bins=50, density=True, histtype='bar',  facecolor='xkcd:nasty green', alpha=0.75)

            fig.tight_layout(pad=1, w_pad=1, h_pad=1)

            with self.graphBox:
                plt.show()
            
    ## AutoRun thread functions
    ##
    # buttonStartAutoRun() - start/restart auto run processing
    #    Argument - change - not used, exists to cater for ipywidget button actions.
    # 
    @debug.capture(clear_output=True)    
    def buttonStartAutoRun(self, change):
        #check for restart, if thread event flag is set, clear it so thread can be restarted
        if  self.threadAutoRun_stop.isSet():
            self.threadAutoRun_stop.clear()
        #allocate new thread and start it. 
        # When AutoRun is stopped, the thread completes processing and terminates, so a new one is required
        self.threadAutoRun  = threading.Thread(target=self.executeAutoRun, args=(1, self.threadAutoRun_stop)) 
        self.threadAutoRun.start()

    # buttonStopAutoRun() - stop auto run processing
    #    Argument - change - not used, exists to cater for ipywidget button actions.
    # 
    @debug.capture(clear_output=True)    
    def buttonStopAutoRun(self, change):
        #set Event flag to stop the looping in executeAutoRun()
        self.threadAutoRun_stop.set()

    # executeAutoRun() - execute runWorkflowJobs and then pause for runDelay
    #    Argument - change - not used, exists to cater for ipywidget button actions.
    # 
    @debug.capture(clear_output=True)    
    def executeAutoRun(self, arg, threadEvent):
        while not threadEvent.is_set():
            self.runWorkflowJobs('')
            threadEvent.wait(self.runDelay.value * 60)
    #End
            
    # on_click() - handle actions for the Mode button, enable/disable AutoRun  
    #
    @debug.capture(clear_output=True)
    def on_click(self, change):
        if  self.mode.value == 'Single Process':
            #protect and fill fields as needed.
            self.singleProcess()
            
        if  self.mode.value == 'Workflow':
            self.workflowProcess()
            
        if  self.enableAutoRun.value == 'Enable':
            self.startAutoRun.disabled = False
            self.stopAutoRun.disabled  = False
            self.runDelay.disabled     = False

        if  self.enableAutoRun.value == 'Disable':
            self.startAutoRun.disabled = True
            self.stopAutoRun.disabled  = True
            self.runDelay.disabled     = True
            #Disabling, so stop autoRun if running.
            self.buttonStopAutoRun('')            

    # on_click() - handle click actions for the displayGraphs radio button
    @debug.capture(clear_output=True)
    def on_click(self, change):
        if  self.displayGraphs.value == 'Disable':
            self.graphBox.clear_output()
    
    
    # buildInputWidgets() - write all the workflow fields to the screen.
    #
    @debug.capture(clear_output=True)
    def buildWidgets(self):
        #linking button on_click to function    
        self.loadButton.on_click(self.loadJobs)
        self.saveButton.on_click(self.saveJobs)
        self.runAllButton.on_click(self.runWorkflowJobs)
        self.startAutoRun.on_click(self.buttonStartAutoRun)
        self.stopAutoRun.on_click(self.buttonStopAutoRun)
        
        self.displayGraphs.observe(self.on_click, 'value')

        jobButtons = HBox([self.loadButton, self.saveButton, self.errorText])
        runBox     = HBox([self.runAllButton, self.runProgress])
        autoRunBox = HBox([self.enableAutoRun, self.startAutoRun, self.runDelay, self.stopAutoRun])
        
        self.mode.observe(self.on_click, 'value')    
        self.enableAutoRun.observe(self.on_click, 'value')
        #Disable AutoRun fields at startup
        self.on_click('Disable')
        
        if  self.showDebug:
            return VBox([self.debug, self.debugText, self.mode, self.projectDirectory, jobButtons, runBox, autoRunBox, self.displayGraphs, self.graphBox])
        else:
            return VBox([self.mode, self.projectDirectory, jobButtons, runBox, autoRunBox, self.displayGraphs, self.graphBox])
