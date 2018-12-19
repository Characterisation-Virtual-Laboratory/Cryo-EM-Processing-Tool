import ipywidgets as widgets
from ipywidgets import HBox, VBox, Box, Label, Layout

class jobMaintenance:

    ##Debug assistance
    debug = widgets.Output(
        style={'description_width': '120px'}, 
        layout=Layout(width='90%'))
    
    def __init__(self, header, jobNumberField, buildJobFunc, buildNewJobsFunc, buildArgumentsListFunc, updateScreenFieldsFunc, callProgramFunc, program):
        self.existingJobs = []
        self.jobCounter = 1
        
        self.jobNumber = jobNumberField
        self.program = program
        #the buildJob function as implemented by the consuming class
        self.buildJob = buildJobFunc
        #the buildNewJobs function as implemented by the consuming class
        self.buildNewJobs = buildNewJobsFunc
        #the buildArgumentsList function as implemented by the consuming class
        self.buildArgumentsList = buildArgumentsListFunc
        #the updateScreenFields function as implemented by the consuming class
        self.updateScreenFields = updateScreenFieldsFunc
        #the callProgram function as implemented by the consuming class
        self.callProgram = callProgramFunc
        
        self.jobsList = widgets.SelectMultiple(description='Jobs: ', options=header,
            disabled=False, style={'description_width': 'initial'},
            rows=10, layout=Layout(width='90%'))

        self.addButton = widgets.Button(description='Add', disabled=False, button_style='',
            tooltip='Add job')

        self.deleteButton = widgets.Button(description='Delete', disabled=False,
            button_style='', tooltip='Delete job(s)')

        self.selectButton = widgets.Button(description='Select', disabled=False, 
            button_style='', tooltip='Select job for editing.')

        self.updateButton = widgets.Button(description='Update', disabled=False,
            button_style='', tooltip='Update job.')

        self.runAllButton = widgets.Button(description='Run All', disabled=False, 
            button_style='', tooltip='Run all jobs')

        self.runProgress = widgets.IntProgress(value=0, min=0, max=10, step=1, 
            description='Progress:', bar_style='', orientation='horizontal')
        
    # addJob() - builds the new job from the input variables and updates the job list.
    #
    @debug.capture(clear_output=True)
    def addJob(self, target):
        listedJobs = self.jobsList.options
        listedJobsList = list(listedJobs)
        newJob = self.buildJob(self.jobCounter)
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
        updatedJob = self.buildJob()
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
                self.callProgram(self.program, self.buildArgumentsList(jobToProcess=listedJobsList[i]), listedJobsList[i]['outMrc'])
                self.runProgress.value = i+1                
            
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
        
    # buildJobWidgets()
    #
    def buildJobWidgets(self):
        #Add fuctions to buttons.
        self.addButton.on_click(self.addJob)
        self.deleteButton.on_click(self.deleteJob)
        self.selectButton.on_click(self.selectJob)
        self.updateButton.on_click(self.updateJob)
        self.runAllButton.on_click(self.runAllJobs)        
        
        buttons = HBox([self.addButton, self.deleteButton, self.selectButton, self.updateButton, self.runAllButton, self.runProgress])
        
        return VBox([self.debug, self.jobsList, buttons])