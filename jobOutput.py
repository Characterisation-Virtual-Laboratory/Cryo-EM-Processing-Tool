import os
import subprocess as subp
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Box, Label, Layout

#Output Widgets

class jobOutput:
    #style and Layout
    styleBasic    = {'description_width': '120px'}
    outputLayout  = Layout(width='90%')

    #screen fields
    argsOutput = widgets.Textarea(
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
    
    def __init__(self, showDebug):
        #instance variables unique to each instance
        self.showDebug = showDebug

    # saveOutput() - write to disk the stdout, stderr and args values used in
    #                 calling the 'program'.
    #                 Files are written to in append mode. This caters for both 'single' and 'workflow' modes
    #    Arguments:
    #        program   - the executable
    #        folder    - destination of output
    #
    @debug.capture(clear_output=True)
    def saveOutput(self, program, folder):
        outputFilename = program + "-output.txt"
        argsFilename   = program + "-arguments.txt"
        errorFilename  = program + "-error.txt"
        
        try:
            fOutput = open(folder + outputFilename, "a")
            fOutput.write(self.stdout.value + '\n\n')
        except OSError as err:
            self.stderr.value = "Error writing Job Output: {0}".format(err)
        else:
            fOutput.close()

        try:
            fArgs = open(folder + argsFilename, "a")
            fArgs.write(self.argsOutput.value + '\n\n')
        except OSError as err:
            self.stderr.value = "Error writing Job Arguments: {0}".format(err)
        else:
            fArgs.close()

        try:
            fError = open(folder + errorFilename, "a")
            fError.write(self.stderr.value + '\n\n')
        except OSError as err:
            self.stderr.value = "Error writing Job Errors: {0}".format(err)
        else:
            fError.close()
            
            
    # call_program() - executes the 'program', populates stdout, stderr and args 
    #                   screen fields.
    #    Arguments:
    #        program      - the executable
    #        arguments    - string of arguments
    #        outputFolder - destination for saved job output
    #
    @debug.capture(clear_output=True)
    def call_program(self, program, arguments, outputFolder):
        #Clear output from previous run
        self.stdout.value = ''
        self.stderr.value = ''
        self.argsOutput.value = ''
        
        if  program is not None:

            #Calling program
            #Note: shell=True. There are security implications for this. This was enabled as the arguments were not
            #being passed in.
            try:
                response = subp.Popen(program + arguments, shell=True, stdout=subp.PIPE, stderr=subp.PIPE)
                
            except subp.SubprocessError as err:
                self.stderr.value += 'Subprocess error: {0}'.format(err) + '\n'

            while True:
                output = response.stdout.readline().decode()
                if  output == '' and response.poll() is not None:
                    break
                if  output:
                    self.stdout.value = self.stdout.value + output

            while True:
                error = response.stderr.readline().decode()
                if  error == '' and response.poll() is not None:
                    break
                if  error:
                    self.stderr.value = self.stderr.value + error

            #Add return code to stderr as Gctf and Gautomatch do not finsh cleanly when files not found
            self.stderr.value += "ReturnCode: " + str(response.returncode) + '\n'
            
            self.argsOutput.value = arguments
            
            if  outputFolder:
                self.saveOutput(program, outputFolder)
            
    # buildOutputWidgets() - write all output fields to the screen.
    @debug.capture(clear_output=True)
    def buildOutputWidgets(self):

        if  self.showDebug:
            return VBox([self.debug, self.debugText, self.stdout, self.stderr, self.argsOutput])
        else:
            return VBox([self.debug, self.stdout, self.stderr, self.argsOutput])
