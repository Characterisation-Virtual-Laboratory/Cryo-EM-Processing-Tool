import os
import subprocess as subp
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Box, Label, Layout

#Output Widgets

class jobOutput:
    #style and Layout
    styleBasic    = {'description_width': '100px'}
    outputLayout = Layout(width='90%')

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

    debug = widgets.Textarea(
        description='Debugging:',
        description_tooltip='Standard output',
        disabled=False,
        rows=10,
        style=styleBasic,
        layout=outputLayout)    
    
    def __init__(self, showDebug):
        #instance variables unique to each instance
        self.showDebug = showDebug

    # saveOutput() - write to disk the stdout, stderr and args values used in
    #                 calling the 'program'.
    #    Arguments:
    #        program   - the executable
    #        folder    - destination of output
    #
    def saveOutput(self, program, folder):
        outputFilename = program + "-output.txt"
        argsFilename   = program + "-arguments.txt"
        errorFilename  = program + "-error.txt"

        fOutput = open(folder + outputFilename, "w")
        fOutput.write(self.stdout.value)
        fOutput.close()

        fArgs = open(folder + argsFilename, "w")
        fArgs.write(self.argsOutput.value)
        fArgs.close()

        fError = open(folder + errorFilename, "w")
        fError.write(self.stderr.value)
        fError.close()

    # call_program() - executes the 'program', populates stdout, stderr and args 
    #                   screen fields.
    #    Arguments:
    #        program      - the executable
    #        arguments    - string of arguments
    #        outputFolder - destination for saved job output
    #
    def call_program(self, program, arguments, outputFolder):
        #Clear output from previous run
        self.stdout.value = ''
        self.stderr.value = ''
        self.argsOutput.value = ''

        if  program is not None:
            #clear stdout, args , stderr
            self.stdout.value = ""
            self.argsOutput.value = ""

            #Calling program
            #Note: shell=True. There are security implications for this. This was enabled as the arguments were not
            #being passed in.

            #try:
            response = subp.Popen(program + arguments, shell=True, stdout=subp.PIPE, stderr=subp.PIPE)
            #except sp.TimeoutExpired:
            #    stderr.value = 'Call timed out!'

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
                    
            self.argsOutput.value = arguments
            self.saveOutput(program, outputFolder)
            
    # buildOutputWidgets() - write all output fields to the screen.
    def buildOutputWidgets(self):

        if  self.showDebug:
            display(self.debug)

        organiseOutputs = VBox([self.stdout, self.stderr, self.argsOutput])
        display(organiseOutputs)