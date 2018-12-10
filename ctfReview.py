import glob
import ipywidgets as widgets
import mrcfile
import numpy as np
import os
import pandas as pd
import warnings
from io import BytesIO
from ipywidgets import HBox, VBox, Box, Label, Layout
from PIL import Image, ImageEnhance
from traitlets import traitlets

#Review CTF output to determine data quality.

class ctfReview:
    #Settings:
    thumbNailSize = (256, 256)
    rawThumbNailSize = (256, 256)
    starFileName  = 'selected_micrographs_ctf.star'

    #style and Layout
    styleBasic    = {'description_width': '120px'}
    styleAdvanced = {'description_width': '160px'}
    basicLayout   = Layout(width='60%')
    ctfLayout     = Layout(width='95%')
    advLayout     = Layout(width='50%')
    errorLayout   = Layout(width='60%', border='2px solid red')

    startButton = widgets.Button(
        description='Start review',
        disabled=False,
        button_style='',
        tooltip='Start CTF review',
        icon='')

    applyFilterButton = widgets.Button(
        description='Apply',
        disabled=False,
        button_style='',
        tooltip='Apply',
        icon='')

    reviewButton = widgets.Button(
        description='Review',
        disabled=False,
        button_style='',
        tooltip='Display filtered CTF mrcs',
        icon='')

    saveButton = widgets.Button(
        description='Save',
        disabled=False,
        button_style='',
        tooltip='Save filtered mrcs to .star file',
        icon='check')

    projectDirectory = widgets.Text(
        description='Project directory: ',
        placeholder='Relion project directory',
        value='',
        disabled=True,
        style=styleBasic,
        layout=basicLayout)

    gctfFolderName = widgets.Text(
        description='Folder: ',
        value='',
        disabled=True,
        style=styleBasic,
        layout=basicLayout)

    errorText = widgets.Text(
        description='',
        placeholder='Errors',
        disabled=True,
        style=styleBasic,
        layout=basicLayout)

    jobSelection = widgets.RadioButtons(
        options='',
        description='Available jobs:',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    defocusUFrom = widgets.FloatText(
        description='Defocus U from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusUTo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusVFrom = widgets.FloatText(
        description='Defocus V from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusVTo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusAFrom = widgets.FloatText(
        description='Defocus angle from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    defocusATo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    voltageFrom = widgets.FloatText(
        description='Voltage from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    voltageTo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    sphericalAberrationFrom = widgets.FloatText(
        description='Spherical aberration from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    sphericalAberrationTo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ampContrastFrom = widgets.FloatText(
        description='Amplitude contrast from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ampContrastTo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    magnificationFrom = widgets.FloatText(
        description='Magnification from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    magnificationTo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    detectPixSizeFrom = widgets.FloatText(
        description='Detector pix size from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    detectPixSizeTo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ctfFigMeritFrom = widgets.FloatText(
        description='Ctf figure of merit from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ctfFigMeritTo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ctfMaxResFrom = widgets.FloatText(
        description='Ctf max resolution from: ',
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    ctfMaxResTo = widgets.FloatText(
        description='to: ',
        value=99999999,
        disabled=False,
        style=styleAdvanced,
        layout=advLayout)

    orderBy = widgets.RadioButtons(
        options=['Defocus U', 'Figure of merit', 'Ctf max resolution'],
        description='Order by:',
        disabled=False,
        style=styleBasic,
        layout=basicLayout)

    totalMicrographs = widgets.Textarea(
        description='Total micrographs',
        value='',
        disabled=True,
        style=styleBasic,
        layout=basicLayout)

    totalFilteredMicrographs = widgets.IntText(
        description='Total filtered: ',
        value=0,
        disabled=True,
        style=styleBasic,
        layout=basicLayout)

    jobsBox = widgets.Output(
        layout={'border': '2px solid black'})

    reviewBox = widgets.Output(
        layout={'border': '2px solid black'})

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

    workFlow = None
    contrastTransfer = None
    ctfReviewList = []
    filteredCtfReviewList = []

    # __init__() - initialise the class jobMaintenance
    #    Arguments:
    #        workFlow         - an instance of the workFlow class
    #        contrastTransfer - an instance of the contrastTransfer class e.g. gctf_106
    #        showDebug        - display debug fields
    #
    def __init__(self, workFlow, contrastTransfer, showDebug):
        self.workFlow = workFlow
        self.contrastTransfer = contrastTransfer
        self.showDebug = showDebug

    # convertToPNG() - convert the Image object to a PNG image
    #     Arguments - im - image object
    #
    @debug.capture(clear_output=True)
    def convertToPNG(self, im):
        with BytesIO() as f:
            im.save(f, format='PNG')
            return f.getvalue()

    # dynamicOnClick() - handles button actions for displayed CTF micrographs.
    #     Arguments - ctfData - a list containing the data created by gctf for a single micrograph
    #               - button - the button that was clicked
    #
    @debug.capture(clear_output=True)
    def dynamicOnClick(self, ctfData, button):

        if hasattr(button,'showData'):
            button.showData.clear_output()
            with button.showData:
                print('Defocus U:            ' + str(ctfData['defocusU']) + '\n' +  \
                      'Defocus V:            ' + str(ctfData['defocusV']) + '\n' + \
                      'Defocus Angle:        ' + str(ctfData['defocusAngle']) + '\n' + \
                      'Voltage:              ' + str(ctfData['voltage']) + '\n' + \
                      'Spherical Aberration: ' + str(ctfData['sphericalAberration']) + '\n' + \
                      'Amplitude Contrast:   ' + str(ctfData['ampContrast']) + '\n' + \
                      'Magnification:        ' + str(ctfData['magnification']) + '\n' + \
                      'Detector Pixel Size:  ' + str(ctfData['detectorPixelSize']) + '\n' + \
                      'Figure of Merit:      ' + str(ctfData['figOfMerit']) + '\n' + \
                      'Ctf Max Resolution:   ' + str(ctfData['maxResolution']))
                
        if hasattr(button,'showMrc'):
            button.showMrc.clear_output()
            with button.showMrc:
                fileName = ctfData['micrographNameNoDW']
                #Problem, MotionCorr2 created mrcs have an issue with the MAP ID string in the header, it should be 'MAP ' but MotionCorr ones have 'MAP'.
                #Opening in permissive mode and catching the warning, we can get around this.
                try:
                    with warnings.catch_warnings(record=True) as w:
                        mrc = mrcfile.mmap(self.projectDirectory.value + fileName, permissive=True)

                except FileNotFoundError as err:
                    self.errorText.value = "Unable to load Micrograph: {0}".format(err)
                    self.errorText.layout = self.errorLayout
                else:
                    mrcArray = np.array(mrc.data)
                    #extract data, convert values to 0 - 255 int8 format
                    formatted = (mrcArray * 255 / np.max(mrcArray)).astype('uint8')
                    img = Image.fromarray(formatted)
                    img.thumbnail(self.rawThumbNailSize)

                    #increase contast to aid visibility
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(6)

                    imagePng = self.convertToPNG(img)
                    mrc.close()

                    img = widgets.Image(value=imagePng, format='PNG', width=self.rawThumbNailSize[0], height=self.rawThumbNailSize[1])
                    display(img)

    #  showCtfMicrographs() - builds a list of CTF micrographs with accompanying buttons to display data and raw the micrograph
    #      Arguments - projectDirectory, relion project folder - full path
    #                - ctfs - a list of dicts containing CTF values generated by gctf.
    #      Returns a list of VBox objects containing the micrograph image, with accompanying buttons to display data and the raw micrograph.
    #
    @debug.capture(clear_output=True)
    def showCtfMicrographs(self, projectDirectory, ctfs):

        allMicrographs = []

        for i in range(len(ctfs)):
            fileName = ctfs[i]['ctfImage'].replace(':mrc', '')
            
            try:
                mrc = mrcfile.mmap(projectDirectory + fileName)
            except (FileNotFoundError, ValueError) as err:
                self.errorText.value = "Unable to load Micrograph: {0}".format(err)
                self.errorText.layout = self.errorLayout
            else:
                #extract data, convert values to 0 - 255 int8 format
                formatted = (mrc.data[0] * 255 / np.max(mrc.data)).astype('uint8')
                img = Image.fromarray(formatted)
                img.thumbnail(self.thumbNailSize)

                imagePng = self.convertToPNG(img)

                mrc.close()

            #Dynamically build the Ctf mrcs and buttons.
            img = widgets.Image(value=imagePng, format='PNG', width=self.thumbNailSize[0], height=self.thumbNailSize[1])
            dataButton = widgets.Button(description='Data', disabled=False, button_style='', tooltip='Show data', icon='check')
            mrcButton = widgets.Button(description='Raw mrc', disabled=False, button_style='', tooltip='Show micrograph', icon='check')
            buttonOutput = widgets.Output(layout={'border': '2px solid black'})

            dataButton.add_traits(showData = traitlets.Any(buttonOutput))
            mrcButton.add_traits(showMrc = traitlets.Any(buttonOutput))

            #adding on_click actions to buttons dynamically, lambda is an anonymous function
            #lambda arguments: function
            dataButton.on_click(lambda dataButton,num=i: self.dynamicOnClick(ctfs[num], dataButton))
            mrcButton.on_click(lambda mrcButton,num=i: self.dynamicOnClick(ctfs[num], mrcButton))

            micrograph = VBox([img, HBox([dataButton, mrcButton]), buttonOutput])
            allMicrographs.append(micrograph)

        return allMicrographs

    # buildReviewJobs() - obtains a list of folders (jobs), then uses these to build a list
    #    of radio buttons
    #    @debug.capture causes any exceptions to be displayed in the debug field
    #
    @debug.capture(clear_output=True)
    def buildReviewJobs(self):
        folders = glob.glob(self.projectDirectory.value + self.gctfFolderName.value + '*')

        jobs = []
        for i in range(len(folders)):
            split = folders[i].rsplit('/', 1)
            jobs.append(split[1])

        self.totalMicrographs.value = ''
        self.errorText.layout = self.basicLayout

        #Determine total count of Ctf micrographs for review for each job.
        for j in range(len(jobs)):
            mrcCount = len(glob.glob(self.projectDirectory.value + self.gctfFolderName.value + jobs[j] + '/Micrographs/*.ctf'))
            self.totalMicrographs.value += jobs[j] + ':  ' + str(mrcCount) + '\n'
            #initialise filter count at start of review
            if  j == 0:
                self.totalFilteredMicrographs.value = mrcCount

        if  not jobs:
            self.errorText.value = "No jobs found: Check project directory"
            self.errorText.layout = self.errorLayout
            return HBox([])
        else:
            self.jobSelection.options = jobs
            return HBox([self.jobSelection, self.totalMicrographs])

    # buildFilters() - contruct the filters tab
    #    returns a VBox containing the filter fields.
    @debug.capture(clear_output=True)
    def buildFilters(self):
        filters = VBox([HBox([self.defocusUFrom, self.defocusUTo]),
                        HBox([self.defocusVFrom, self.defocusVTo]),
                        HBox([self.defocusAFrom, self.defocusATo]),
                        HBox([self.voltageFrom, self.voltageTo]),
                        HBox([self.sphericalAberrationFrom, self.sphericalAberrationTo]),
                        HBox([self.ampContrastFrom, self.ampContrastTo]),
                        HBox([self.magnificationFrom, self.magnificationTo]),
                        HBox([self.detectPixSizeFrom, self.detectPixSizeTo]),
                        HBox([self.ctfFigMeritFrom, self.ctfFigMeritTo]),
                        HBox([self.ctfMaxResFrom, self.ctfMaxResTo]),
                        HBox([self.orderBy, self.totalFilteredMicrographs]),
                        self.applyFilterButton])

        tab = widgets.Tab(children=[filters])
        tab.set_title(0, 'Filters')

        return VBox([tab])

    # startReview() - when clicked builds a list of jobs for review.
    #    @debug.capture causes any exceptions to be displayed in the debug field
    #
    @debug.capture(clear_output=True)
    def startReview(self, target):
        self.errorText.layout = self.basicLayout
        if  self.workFlow.projectDirectory.value == '':
            self.errorText.value = "Workflow Project Directory required"
            self.errorText.layout = self.errorLayout
        else:
            if  self.workFlow.projectDirectory.value.endswith('/') == False:
                self.workFlow.projectDirectory.value += '/'

            self.projectDirectory.value = self.workFlow.projectDirectory.value
            self.gctfFolderName.value = self.workFlow.gctfFolderName

            with self.jobsBox:
                display(HBox([self.projectDirectory, self.gctfFolderName]),
                        self.buildReviewJobs(), self.buildFilters(), HBox([self.reviewButton, self.saveButton]))

    # applyFilter() - apply filters to knockout micrographs for review
    #     Returns a list of filtered micrographs
    #
    @debug.capture(clear_output=True)
    def applyFilter(self, target):

        df = pd.DataFrame(self.ctfReviewList)

        #apply selected order by, ascending
        if  self.orderBy.value == 'Defocus U':
            df.sort_values(by='defocusU', inplace=True)
        if  self.orderBy.value == 'Figure of Merit':
            df.sort_values(by='figOfMerit', inplace=True)
        if  self.orderBy.value == 'Ctf Max Resolution':
            df.sort_values(by='defocusU', inplace=True)

        filtered = df.loc[(df['defocusU']     >= self.defocusUFrom.value)     & (df['defocusU']    <= self.defocusUTo.value) &
                          (df['defocusV']     >= self.defocusVFrom.value)     & (df['defocusV']    <= self.defocusVTo.value) &
                          (df['defocusAngle'] >= self.defocusAFrom.value)     & (df['defocusAngle']<= self.defocusATo.value) &
                          (df['voltage']      >= self.voltageFrom.value)      & (df['voltage']     <= self.voltageTo.value)  &
                          (df['sphericalAberration'] >= self.sphericalAberrationFrom.value) & (df['sphericalAberration'] <= self.sphericalAberrationTo.value) &
                          (df['ampContrast']  >= self.ampContrastFrom.value)  & (df['ampContrast'] <= self.ampContrastTo.value) &
                          (df['magnification']>= self.magnificationFrom.value) &(df['magnification']<= self.magnificationTo.value)&
                          (df['detectorPixelSize']   >= self.detectPixSizeFrom.value) & (df['detectorPixelSize'] <= self.detectPixSizeTo.value) &
                          (df['figOfMerit']   >= self.ctfFigMeritFrom.value)  & (df['figOfMerit']   <= self.ctfFigMeritTo.value) &
                          (df['maxResolution']>= self.ctfMaxResFrom.value)    & (df['maxResolution']<= self.ctfMaxResTo.value)].to_dict('records')

        self.filteredCtfReviewList = filtered
        self.totalFilteredMicrographs.value = len(self.filteredCtfReviewList)
        return filtered


    # reviewCtfs() - when clicked builds a list of jobs for review.
    #    @debug.capture causes any exceptions to be displayed in the debug field
    #
    @debug.capture(clear_output=True)
    def reviewCtfs(self, target):

        allMicrographs = self.showCtfMicrographs(self.workFlow.projectDirectory.value, self.filteredCtfReviewList)

        hBoxes = []

        rowItemCnt = 0
        rowItemMax = 5
        row = []

        #Construct a grid layout to display the Ctf Micrographs - max 5 per row.
        for i in range(len(allMicrographs)):

            if  rowItemCnt < rowItemMax:
                row.append(allMicrographs[i])
                rowItemCnt += 1

            if  (len(row) == rowItemMax) or (i == len(allMicrographs)-1):
                hBoxes.append(HBox(row))
                row = []
                rowItemCnt = 0

        self.reviewBox.clear_output()
        with self.reviewBox:
            display(VBox(hBoxes))

    # saveSelected() - create a star file containing the selected CTFs
    #
    @debug.capture(clear_output=True)
    def saveSelected(self, target):
        self.contrastTransfer.createStar(self.projectDirectory.value, self.gctfFolderName.value, self.jobSelection.value, self.filteredCtfReviewList, self.starFileName)

    # on_click() - handle click actions for the jobSelection radio button
    @debug.capture(clear_output=True)
    def on_click(self, change):
        #build the list of Micrograph images for selected job
        self.ctfReviewList = self.contrastTransfer.buildStarFileData(self.workFlow.projectDirectory.value, self.workFlow.gctfFolderName, self.jobSelection.value + '/')
        #update total of filtered micrographs
        self.totalFilteredMicrographs.value = len(self.ctfReviewList)
        self.filteredCtfReviewList = self.ctfReviewList

    # buildInputWidgets() - write all the workflow fields to the screen.
    #
    @debug.capture(clear_output=True)
    def buildWidgets(self):
        #linking button on_click to function
        self.startButton.on_click(self.startReview)
        self.reviewButton.on_click(self.reviewCtfs)
        self.applyFilterButton.on_click(self.applyFilter)
        self.saveButton.on_click(self.saveSelected)

        self.jobSelection.observe(self.on_click, 'value')

        advBoxLayout = Layout(display='flex',
                            flex_flow='row',
                            align_items='stretch',
                            border='none',
                            width='100%')

        if  self.showDebug:
            return VBox([self.debug, self.debugText, HBox([self.startButton, self.errorText]), self.jobsBox, self.reviewBox])
        else:
            return VBox([HBox([self.startButton, self.errorText]), self.jobsBox, self.reviewBox])
